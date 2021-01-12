#!/usr/bin/env python
import sys


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

    for i in sorted(freq.keys()):
        print(i)

    freq_sorted = {k: v for k, v in sorted(
        freq.items(), key=lambda x: x[1], reverse=True)}

    # charlist in header -- first symbol is 0b, second 10b, third 100b etc.
    # duplicate symbol ends charlist
    # hardcoding base 2 at the moment
    charlist = []
    last = ''
    for i, char in enumerate(freq_sorted):
        print('assign %d with %s and %d' %
              (1 << i, char, freq_sorted[char]))
        freq_sorted[char] = 1 << i  # change frequency to value now it's sorted
        charlist.append(char)
        last = char
    charlist.append(last)

    encoded = []
    for char in file_string:
        encoded.append(freq_sorted[char])

    # todo: convert to ACTUAL binary representation and then base64

    # print("Compressed file: " + charlist + encoded)

    # print(f"Saving compressed file: {file_out}")
    # f = open(file_out, "x")
    # f.write(charlist + encoded)
    # f.close()
