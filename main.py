#!/usr/bin/env python
import sys


def get_base(num_symbols):
    # TODO: Return the preferred base dependign on how many symbols they are and their
    #           frequency.
    return 2


if __name__ == "__main__":
    file_name = sys.argv[1]
    print(f"Opening: {file_name} for compression")

    f = open(file_name, "r")
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

    print(freq_sorted)

    use_base = get_base(len(freq))
