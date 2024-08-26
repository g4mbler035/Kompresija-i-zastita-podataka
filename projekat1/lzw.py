import os
from struct import pack, unpack

def encoder(input_file: str, n: int):
    maximum_table_size = pow(2, int(n))      
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""
    compressed_data = []

    for symbol in data:                     
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if len(dictionary) < maximum_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    out = input_file.split(".")[0]
    with open(out + ".lzw", "wb") as output_file:
        for data in compressed_data:
            output_file.write(pack('>H', int(data)))

def decoder(input_file: str, n: int):
    maximum_table_size = pow(2, int(n))
    
    compressed_data = []
    with open(input_file, "rb") as file:
        while True:
            rec = file.read(2)
            if len(rec) != 2:
                break
            (data, ) = unpack('>H', rec)
            compressed_data.append(data)

    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    next_code = 256
    decompressed_data = ""
    string = ""

    for code in compressed_data:
        if code not in dictionary:
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if string:
            if len(dictionary) < maximum_table_size:
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
        string = dictionary[code]

    out = input_file.split(".")[0]
    with open(out + "_decoded.txt", "w", encoding='utf-8') as output_file:
        output_file.write(decompressed_data)


def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

if __name__ == "__main__":
    encoder(input_file="2.txt", n=12)
    decoder(input_file="2.lzw", n=12)

    print("Encoding and decoding completed successfully.")

    original_size = os.path.getsize("2.txt")
    compressed_size = os.path.getsize("2.lzw")
    
    ratio = calculate_compression_ratio(original_size, compressed_size)
    print(f"Compression Ratio: {ratio:.2f}")
