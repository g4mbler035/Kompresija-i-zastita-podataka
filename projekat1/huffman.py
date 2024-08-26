import heapq
from collections import Counter
import os
from bitarray import bitarray

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes

def read_file_and_calculate_frequencies(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    frequency_counter = Counter(text)
    chars = list(frequency_counter.keys())
    freq = list(frequency_counter.values())
    return chars, freq, text

def encode_data(data, huffman_codes):
    encoded_data = bitarray()
    encoded_dict = {char: bitarray(code) for char, code in huffman_codes.items()}
    encoded_data.encode(encoded_dict, data)
    return encoded_data

def save_encoded_file(output_filename, huffman_codes, encoded_data):
    with open(output_filename, 'wb') as file:
        # Save the Huffman codes
        for char, code in huffman_codes.items():
            file.write(char.encode('utf-8'))
            file.write(len(code).to_bytes(1, byteorder='big'))
            file.write(bitarray(code).tobytes())
        
        # Save a delimiter (e.g., '\0' byte) to separate codes from the encoded data
        file.write(b'\0')

        # Save the encoded data
        encoded_data.tofile(file)

def load_huffman_codes(file):
    huffman_codes = {}
    while True:
        char = file.read(1).decode('utf-8')
        if char == '\0':  # delimiter found
            break
        length = int.from_bytes(file.read(1), byteorder='big')
        code = bitarray()
        code.frombytes(file.read((length + 7) // 8))
        huffman_codes[code.to01()[:length]] = char
    return huffman_codes

def decode_data(encoded_data, huffman_codes):
    decoded_data = []
    code = bitarray()
    for bit in encoded_data:
        code.append(bit)
        code_str = code.to01()
        if code_str in huffman_codes:
            decoded_data.append(huffman_codes[code_str])
            code.clear()
    return ''.join(decoded_data)

def save_decoded_file(output_filename, decoded_data):
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(decoded_data)


def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

if __name__ == "__main__":
    filename = "2.txt"
    encoded_filename = "encoded_output.bin"
    decoded_filename = "decoded_output.txt"

    chars, freq, text = read_file_and_calculate_frequencies(filename)

    total_freq = sum(freq)
    probabilities = [f / total_freq for f in freq]

    root = build_huffman_tree(chars, probabilities)
    huffman_codes = generate_huffman_codes(root)

    encoded_data = encode_data(text, huffman_codes)

    save_encoded_file(encoded_filename, huffman_codes, encoded_data)

    with open(encoded_filename, 'rb') as file:
        loaded_huffman_codes = load_huffman_codes(file)
        encoded_data = bitarray()
        encoded_data.fromfile(file)
    
    decoded_data = decode_data(encoded_data, loaded_huffman_codes)

    save_decoded_file(decoded_filename, decoded_data)

    print("Encoding and decoding completed successfully.")

    original_size = os.path.getsize(filename)
    compressed_size = os.path.getsize(encoded_filename)
    
    ratio = calculate_compression_ratio(original_size, compressed_size)
    print(f"Compression Ratio: {ratio:.2f}")
