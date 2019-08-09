"""
Huffman Compression and Decompression Program

Created 08/08/19
Developed by Fraser Love

This program compresses and decompresses any text based files using huffman compression and huffman trees.For compression the prgram generates a frequency dictionary based
on the frequency of characters in the text file. A heap is then created and is used to calculate codes to for each character. The text is then encoded
with these codes and extra padding applied. Also the program stores the codes within the .bin file so that for decomression no extra input is needed.
The .bin file is then created and the bits are written to the file. For decompression the program uses the codes stored within the .bin file to decode the binary
and then it removes the padding and then writes the text to a file with the same file extention as before.

Usage - The program is run via the command line. The arguments are as follows:

-c (file_path) or --compress (file_path)        Compress file
-d (file_path) pr --decompress (file_path)      Decompress file
-r or --remove                                  Removes the original input file
"""
import heapq, os, sys, time

class Node:
    """ Heap node object for generating huffman tree """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if isinstance(other, Node) == False or other == None:
            return False
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.freq_dict = {}

    """ Compression Functions """

    def gen_freq_dict(self, text):
        """ Creating a dictionary to store the frequency of each character in the text file """
        for char in text:
            if char not in self.freq_dict:
                self.freq_dict[char] = 0
            self.freq_dict[char] += 1
        return self.freq_dict

    def gen_heap(self):
        for key in self.freq_dict:
            node = Node(key, self.freq_dict[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """ Merging nodes together to create our huffman tree """
        while len(self.heap) > 1:
            node_1 = heapq.heappop(self.heap)
            node_2 = heapq.heappop(self.heap)
            merged = Node(None, node_1.freq + node_2.freq)
            merged.left = node_1
            merged.right = node_2
            heapq.heappush(self.heap, merged)

    def find_codes(self, root, code):
        """ Calculates the specific code of each object based on its position in the huffman tree """
        if root == None:
            return
        if root.char != None:
            self.codes[root.char] = code
            return
        self.find_codes(root.left, code + "0")
        self.find_codes(root.right, code + "1")

    def gen_codes(self):
        root = heapq.heappop(self.heap)
        code = ""
        self.find_codes(root, code)

    def encode_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def store_tree(self, encoded_text):
        """ Storing the codes generated with the encoded text so that it can be decoded without needing to keep the tree in memory """
        tree_length = "{:016b}".format(len(self.codes))
        for key, val in self.codes.items():
            encoded_text = "{:08b}".format(ord(key)) + val.rjust(16, '0') + "{:016b}".format(len(val)) + encoded_text
        encoded_text = tree_length + encoded_text
        return encoded_text

    def store_file_extention(self, encoded_text):
        """Stores the file extention with the encoded text so that it can be decompressed back to its original file format """
        file_extention = os.path.splitext(self.path)[1]
        extention_length = "{:016b}".format(len(file_extention))
        for char in file_extention:
            encoded_text = "{:08b}".format(ord(char)) + encoded_text
        encoded_text = extention_length + encoded_text
        return encoded_text

    def padding_text(self, encoded_text):
        padding = 8 - (len(encoded_text) % 8)
        padding_length = "{:08b}".format(padding)
        for i in range(padding):
            encoded_text += "0"
        encoded_text = padding_length + encoded_text
        return encoded_text

    def gen_bytes(self, encoded_text):
        """ Converting out encoded text into bytes to store in a .bin file """
        binary = bytearray()
        for i in range(0,len(encoded_text),8):
            binary.append(int(encoded_text[i:i+8], 2))
        return binary

    def compress(self):
        start_time = time.time()
        """ Opening the file and running through all functions to compress the text then writing the encoded text to a .bin file """
        filename = os.path.splitext(self.path)[0]
        output_path = filename + ".bin"
        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text = file.read()
            self.gen_freq_dict(text)
            self.gen_heap()
            self.merge_nodes()
            self.gen_codes()
            encoded_text = self.padding_text(self.store_file_extention(self.store_tree(self.encode_text(text))))
            binary = self.gen_bytes(encoded_text)
            output.write(bytes(binary))
        original_size = os.path.getsize(self.path)
        new_size = os.path.getsize(output_path)
        prefixes = ["B", "KB", "MB", "GB"]
        prefix_index = 0
        while original_size > 1000:
            original_size /= 1000
            new_size /= 1000
            prefix_index += 1
        print("\nCompressed: {} in {:.3f}s".format(self.path, time.time()-start_time))
        print("\nOriginal Filesize: {:.2f} {}\nNew Filesize: {:.2f} {}\nCompression Ratio: {:.2f}%".format(original_size, prefixes[prefix_index], new_size, prefixes[prefix_index], 100 - (os.path.getsize(output_path)/os.path.getsize(self.path)*100)))

    """ Decompression Functions """

    def remove_padding(self, encoded_text):
        padding_length = int(encoded_text[:8],2)
        encoded_text = encoded_text[8:]
        encoded_text = encoded_text[:-1*padding_length]
        return encoded_text

    def reconstruct_file_extention(self, encoded_text):
        """ Reconstructing the stored file extention to maintain the original file type """
        extention = []
        extention_length = int(encoded_text[:16],2)
        encoded_text = encoded_text[16:]
        for i in range(0, extention_length*8, 8):
            extention.append(chr(int(encoded_text[i:i+8],2)))
        extention = "".join(extention[::-1])
        encoded_text = encoded_text[8*extention_length:]
        return encoded_text, extention

    def reconstruct_tree(self, encoded_text):
        """ Using the stored codes in the .bin file to reconstruct the code table to decode the text """
        self.codes = {}
        keys = []
        vals = []
        lengths = []
        tree_length = int(encoded_text[:16],2)
        encoded_text = encoded_text[16:]
        for i in range(0,tree_length*40,40):
            keys.append(int(encoded_text[i:i+8],2))
            vals.append(str(encoded_text[i+8:i+24]))
            lengths.append(int(encoded_text[i+24:i+40],2))
        keys, vals, lengths = keys[::-1], vals[::-1], lengths[::-1]
        for i in range(len(keys)):
            while len(vals[i]) > lengths[i]:
                vals[i] = vals[i][1:]
            self.codes[vals[i]] = chr(keys[i])
        encoded_text = encoded_text[40*tree_length:]
        return encoded_text

    def decode_text(self, encoded_text):
        code = ""
        decoded_text = ""
        for bit in encoded_text:
            code += bit
            if code in self.codes:
                char = self.codes[code]
                decoded_text += char
                code = ""
        return decoded_text

    def decompress(self):
        start_time = time.time()
        """ Opening the .bin file then decoding the binary into text and finally outputting the result to a new file """
        filename = os.path.splitext(self.path)[0]
        with open(self.path, "rb") as file:
            bits = ""
            byte = file.read(1)
            while byte != b"":
                byte = ord(byte)
                bits += "{:08b}".format(byte)
                byte = file.read(1)
            encoded_text = self.remove_padding(bits)
            encoded_text, file_extention = self.reconstruct_file_extention(encoded_text)
            encoded_text = self.reconstruct_tree(encoded_text)
            text = self.decode_text(encoded_text)
        with open(filename + file_extention, "w") as output:
            output.write(text)
        print("\nDecompressed: {} in {:.3f}s".format(filename + file_extention, time.time()-start_time))


def main():
    try:
        if sys.argv[1] == "-c" or sys.argv[1] == "--compress":
            try:
                if sys.argv[2] != "":
                    coding = HuffmanCoding(sys.argv[2])
                    coding.compress()
                    if "-r" in sys.argv or "--remove" in sys.argv:
                        os.remove(sys.argv[2])
                else:
                    print("Error: Please provide a path to the file to compress")
            except:
                print("Error: invalid path")

        elif sys.argv[1] == "-d" or sys.argv[1] == "--decompress":
            try:
                if sys.argv[2] != "":
                    coding = HuffmanCoding(sys.argv[2])
                    coding.decompress()
                    if "-r" in sys.argv or "--remove" in sys.argv:
                        os.remove(sys.argv[2])
                else:
                    print("Error: Please provide a path to the .bin file to decompress")
            except:
                print("Error: invalid path")
        else:
            print("Error: invalid path")
    except:
        if len(sys.argv) < 2:
            print("Error: please provide an argument to compress or decompress")

if __name__ == "__main__":
    main()
