def get_charlist_from_header(file_string):
    return (0, 0, 0)


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
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    print(f"Opening: {file_in} for decompression")

    f = open(file_in, "r")
    file_string = f.read()
    f.close()

    input_size = len(file_string.encode('utf-8'))

    (charlist, data_start_idx, final_idx) = get_charlist_from_header(file_string)

    decompressed_file = decompress_file(charlist, data_start_idx)
