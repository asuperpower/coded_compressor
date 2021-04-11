#!/usr/bin/env python
import sys
import struct
import binascii
import array
import base64
import gmpy
import numpy as np
import matplotlib.pyplot as plt
plt.rcdefaults()


def get_base(symbol):
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


def encode_charlist(file_string, base):
    # get character frequency
    freq = {}
    for char in file_string:
        if char not in freq:
            freq[char] = 1
        else:
            freq[char] += 1
    # sort characters by frequency (sort keys by value)
    freq_sorted = {k: v for k, v in sorted(
        freq.items(), key=lambda x: x[1], reverse=True)}

    # encode
    charlist = []
    last = ''
    for i, char in enumerate(freq_sorted):
        # shift amount has to start at 1 not zero
        print('assign %d with %s and %d' %
              (1 << i, char, freq_sorted[char]))
        # Change frequency to encoded value now it's sorted
        # (encoded value, size in bytes of encoded value)
        freq_sorted[char] = (1 << i, get_size_shift(i))
        charlist.append(char)
        last = char
    charlist.append(last)
    return (charlist, freq_sorted)


def compress(charlist, freq_sorted):
    encoded = bytearray(0)
    carry = np.uint8(0)
    idx = 0

    for i, char in enumerate(file_string):
        (encoded_value, size_bytes) = freq_sorted[char]
        carry = np.uint8((1 << 7 - idx) | (carry))
        idx += gmpy.scan1(encoded_value) + 1

        # overflow
        while idx >= 8:
            idx -= 8
            encoded.append(carry)
            carry = np.uint8(0)
    # todo: make last char work by putting padding idx in header
    encoded.append(carry)
    header = bytearray()
    # for bt in charlist:
    #     if bt not in range(0, 256):
    # print(hex(bt))
    header.extend(map(ord, charlist))
    header.append(np.uint8(idx))
    return (header, encoded, carry)


# FILE SPEC:
#   |##############################################################################|
#   | Header                                                                | Data |
#   | Character List | Duplicate last character (END) | Final IDX (1 byte)  | Data |
#   |##############################################################################|
#
#   Character List
#   List of symbols in order of occurence. First (most frequent) symbol gets mapped to
#   0x1, second 0x10, third 0x100 and so fourth.
#   Duplicate last character
#   The final character is duplicated to signal the end of the character list.
#   Final IDX
#   The file ending may not align on a (byte) bondary. It could end a few bits earlier, so
#   the
#   final index tells us where it ends.
#   All the rest in the file is data
if __name__ == "__main__":
    try:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
    except:
        print("Usage: encoder.py <INPUT FILE> <OUTPUT FILE>")
    print(f"Opening: {file_in} for compression")

    try:
        f = open(file_in, "r")
        file_string = f.read()
        f.close()
    except:
        print("Could not open file: {file_in}")

    input_size = len(file_string.encode('utf-8'))

    (charlist, freq_sorted) = encode_charlist(file_string, 2)

    (header, encoded, carry) = compress(charlist, freq_sorted)

    print('Compressed file\nHeader:\n%s\nData:\n%s' %
          (header, binascii.hexlify(encoded)))
    file = header + encoded

    f = open(file_out, 'wb')
    f.write(file)
    f.close()

    output_size = len(file)
    print('Compression ratio: %f' % ((input_size/output_size)))

    objects = ('Input File', 'Output File')
    y_pos = np.arange(len(objects))
    results = (input_size, output_size)

    plt.bar(y_pos, results, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Size (bytes)')
    plt.title('File size (input vs output file)')

    plt.show()
