import os
from pathlib import Path
from collections import Counter
from bitarray import bitarray

class Node:
    def __init__(self):
        self.sym = ''
        self.pro = 0.0

def sort_by_probability(n, p):
    for j in range(1, n):
        for i in range(n - 1):
            if p[i].pro > p[i + 1].pro:
                p[i], p[i + 1] = p[i + 1], p[i]

def encode_text(text, nodes):
    char_to_bits = {node.sym: format(i, '08b') for i, node in enumerate(nodes)}
    
    encoded_text = bitarray()
    for char in text:
        encoded_text.extend(char_to_bits[char])
    return encoded_text

def decode_text(encoded_text, nodes):
    bits_to_char = {format(i, '08b'): node.sym for i, node in enumerate(nodes)}
    
    decoded_text = ""
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8].to01()
        decoded_text += bits_to_char[byte]
    return decoded_text

def read_text_from_file(input_file):
    with open(input_file, 'r') as f:
        return f.read()

def write_encoded_to_file(encoded_text, encoded_file):
    Path("results/shanoon").mkdir(parents=True, exist_ok=True)
    with open(encoded_file, 'wb') as f:
        encoded_text.tofile(f)

def read_encoded_from_file(encoded_file):
    encoded_text = bitarray()
    with open(encoded_file, 'rb') as f:
        encoded_text.fromfile(f)
    return encoded_text

def write_decoded_to_file(decoded_text, output_file):
    Path("results/shanoon").mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(decoded_text)

def create_nodes_from_text(text):
    frequencies = Counter(text)
    total_chars = sum(frequencies.values())
    nodes = [Node() for _ in range(len(frequencies))]
    for i, (sym, freq) in enumerate(frequencies.items()):
        nodes[i].sym = sym
        nodes[i].pro = freq / total_chars
    sort_by_probability(len(nodes), nodes)
    return nodes

def encode(input_file: str, encoded_file: str):
    text = read_text_from_file(input_file)
    nodes = create_nodes_from_text(text)
    encoded_text = encode_text(text, nodes)
    write_encoded_to_file(encoded_text, encoded_file)

    return nodes

def decode(encoded_file: str, output_file: str, nodes):
    encoded_text = read_encoded_from_file(encoded_file)
    decoded_text = decode_text(encoded_text, nodes)
    write_decoded_to_file(decoded_text, output_file)

def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

def main():
    input_file = "test/2.txt"
    encoded_file = "results/shanoon/encoded.bin"
    output_file = "results/shanoon/decoded.txt"

    nodes = encode(input_file, encoded_file)

    decode(encoded_file, output_file, nodes)

    print("Encoding and decoding completed successfully.")

    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(encoded_file)
    
    ratio = calculate_compression_ratio(original_size, compressed_size)
    print(f"Compression Ratio: {ratio:.2f}")

if __name__ == "__main__":
    main()
