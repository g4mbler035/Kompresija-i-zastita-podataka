import sys
from struct import pack, unpack

def encoder(input_file: str, n: int):
    maximum_table_size = pow(2, int(n))      
    with open(input_file, 'r') as file:                 
        data = file.read()                      

    # Building and initializing the dictionary.
    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             # String is null.
    compressed_data = []    # Variable to store the compressed data.

    # Iterating through the input symbols.
    # LZW Compression algorithm
    for symbol in data:                     
        string_plus_symbol = string + symbol # Get input symbol.
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

    # Storing the compressed string into a file (byte-wise).
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

    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    next_code = 256
    decompressed_data = ""
    string = ""

    # Iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if code not in dictionary:
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if string:
            if len(dictionary) < maximum_table_size:
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
        string = dictionary[code]

    # Storing the decompressed string into a file.
    out = input_file.split(".")[0]
    with open(out + "_decoded.txt", "w") as output_file:
        output_file.write(decompressed_data)
