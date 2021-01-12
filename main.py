#!/usr/bin/env python
import sys
import struct
import binascii
import array


def get_base(num_symbols):
    # TODO: Return the preferred base dependign on how many symbols they are and their
    #           frequency.
    return 2


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
        print('%s is now %s!' % (char, freq[char]))

    freq_sorted = {k: v for k, v in sorted(
        freq.items(), key=lambda x: x[1], reverse=True)}

    # charlist in header -- first symbol is 0b, second 10b, third 100b etc.
    # duplicate symbol ends charlist
    # hardcoding base 2 at the moment
    charlist = []
    last = ''
    byte_array_sz = 0
    for i, char in enumerate(freq_sorted):
        print('assign %d with %s and %d' %
              (1 << i, char, freq_sorted[char]))
        # change frequency to encoded value now it's sorted
        # (encoded value, size in bytes of encoded value)
        freq_sorted[char] = (1 << i, 1 + int(i/4))
        byte_array_sz += 1 + int(i/4)
        charlist.append(char)
        # increment for charlist
        byte_array_sz += 1
        last = char
    byte_array_sz += 1
    charlist.append(last)

    encoded = bytearray(byte_array_sz)
    # encoded = array.array('c', '\0' * byte_array_sz)
    for i, char in enumerate(file_string):
        (encoded_value, size_bytes) = freq_sorted[char]
        packing_string = 'B'*size_bytes
        i += (size_bytes - 1)  # ew
        print('pack_bytes: %s' % packing_string)

    # todo: convert to ACTUAL binary representation and then base64

    # print("Compressed file: " + charlist + encoded)

    # print(f"Saving compressed file: {file_out}")
    # f = open(file_out, "x")
    # f.write(charlist + encoded)
    # f.close()
