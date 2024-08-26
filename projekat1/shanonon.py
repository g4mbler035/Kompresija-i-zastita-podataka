import os
from pathlib import Path
from collections import Counter
from bitarray import bitarray

class Node:
    def __init__(self):
        self.sym = ''
        self.pro = 0.0
        self.arr = []
        self.top = -1

def shannon(l, h, p):
    if (l + 1) == h or l == h or l > h:
        if l == h or l > h:
            return
        p[h].top += 1
        p[h].arr.append(0)
        p[l].top += 1
        p[l].arr.append(1)
        return
    pack1 = pack2 = diff1 = diff2 = 0
    for i in range(l, h):
        pack1 += p[i].pro
    pack2 = p[h].pro
    diff1 = abs(pack1 - pack2)
    j = 2
    while j != h - l + 1:
        k = h - j
        pack1 = pack2 = 0
        for i in range(l, k + 1):
            pack1 += p[i].pro
        for i in range(h, k, -1):
            pack2 += p[i].pro
        diff2 = abs(pack1 - pack2)
        if diff2 >= diff1:
            break
        diff1 = diff2
        j += 1
    k += 1
    for i in range(l, k + 1):
        p[i].top += 1
        p[i].arr.append(1)
    for i in range(k + 1, h + 1):
        p[i].top += 1
        p[i].arr.append(0)
    shannon(l, k, p)
    shannon(k + 1, h, p)

def sort_by_probability(n, p):
    for j in range(1, n):
        for i in range(n - 1):
            if p[i].pro > p[i + 1].pro:
                p[i], p[i + 1] = p[i + 1], p[i]

def encode_text(text, nodes):
    encoded_text = bitarray()
    for char in text:
        for node in nodes:
            if node.sym == char:
                encoded_text.extend(node.arr)
                break
    return encoded_text

def decode_text(encoded_text, nodes):
    reverse_dict = {''.join(map(str, node.arr)): node.sym for node in nodes}
    decoded_text = ""
    code = ""
    for bit in encoded_text:
        code += '1' if bit else '0'
        if code in reverse_dict:
            decoded_text += reverse_dict[code]
            code = ""
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
    for i in range(len(nodes)):
        nodes[i].top = -1
    shannon(0, len(nodes) - 1, nodes)
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
