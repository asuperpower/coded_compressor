#!/usr/bin/env python
import sys
import struct
import binascii
import array
import base64
import gmpy
import numpy as np


def get_base(num_symbols):
    # TODO: Return the preferred base dependign on how many symbols they are and their
    #           frequency. Requires some math.
    return 2


def get_size_shift(shift_value):
    return 1 + int(shift_value/8)


def ffs(x):
    """Returns the index, counting from 0, of the
    least significant set bit in `x`.
    """
    return (x & -x).bit_length()-1


if __name__ == "__main__":
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    print(f"Opening: {file_in} for compression")

    f = open(file_in, "r")
    file_string = f.read()
    f.close()

    freq = {}

    for char in file_string:
        if char not in freq:
            freq[char] = 1
        else:
            freq[char] += 1
    freq_sorted = {k: v for k, v in sorted(
        freq.items(), key=lambda x: x[1], reverse=True)}

    # charlist in header -- first symbol is 0b, second 10b, third 100b etc.
    # duplicate symbol ends charlist
    # hardcoding base 2 at the moment
    charlist = []
    last = ''
    byte_array_sz = 0
    for i, char in enumerate(freq_sorted):
        # shift amount has to start at 1 not zero
        print('assign %d with %s and %d' %
              (1 << i, char, freq_sorted[char]))
        # change frequency to encoded value now it's sorted
        # (encoded value, size in bytes of encoded value)
        freq_sorted[char] = (1 << i, get_size_shift(i))
        byte_array_sz += get_size_shift(i)
        charlist.append(char)
        # increment for charlist
        byte_array_sz += 1
        last = char
    byte_array_sz += 1
    charlist.append(last)

    encoded = bytearray(0)
    carry = np.uint8(0)
    idx = 0
    print('')
    print('idx: %d' % (idx))
    print('')
    # encoded = array.array('c', '\0' * byte_array_sz)
    for i, char in enumerate(file_string):
        (encoded_value, size_bytes) = freq_sorted[char]
        # print('value is: %s' % (struct.unpack('B', carry)))
        print(np.unpackbits(carry.reshape(-1, 1), axis=1))
        carry = np.uint8((1 << 7 - idx) | (carry))
        idx += gmpy.scan1(encoded_value) + 1
        print('char: %c enc: %s, idx: %d, carry: %s' %
              (char, hex(encoded_value), idx, hex(int.from_bytes(carry, byteorder='big', signed=False))))

        # overflow
        while idx >= 8:
            idx -= 8
            encoded.append(carry)
            carry = np.uint8(0)
            print('encoded carry: %d' %
                  (int.from_bytes(carry, byteorder='big', signed=False)))
        print('encoded: %s', binascii.hexlify(encoded))
    # todo: make last char work by putting padding idx in header
    encoded.append(carry)
    print(binascii.hexlify(encoded))
    # first_set_byte = 0
    # for i, byte in enumerate(bt):
    #     if byte is b'\x00':
    #         first_set_byte = i
    #         break
    # print('fsb: %d' % first_set_byte)

    # todo: convert to ACTUAL binary representation and then base64

    # print("Compressed file: " + charlist + encoded)

    # print(f"Saving compressed file: {file_out}")
    # f = open(file_out, "x")
    # f.write(charlist + encoded)
    # f.close()
