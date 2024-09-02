import math
import os
from pathlib import Path
from bitarray import bitarray

class LZ77Compressor:
    """
    A simplified implementation of the LZ77 Compression Algorithm
    """
    MAX_WINDOW_SIZE = 400

    def __init__(self, window_size=20):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = 15

    def compress(self, input_file_path, output_file_path=None, verbose=False):
        """
        Given the path of an input file, its content is compressed by applying a simple
        LZ77 compression algorithm.

        The compressed format is:
        0 bit followed by 8 bits (1 byte character) when there are no previous matches
        within window
        1 bit followed by 12 bits pointer (distance to the start of the match from the
        current position) and 4 bits (length of the match)
        
        If a path to the output file is provided, the compressed data is written into
        a binary file. Otherwise, it is returned as a bitarray

        if verbose is enabled, the compression description is printed to standard output
        """
        data = None
        i = 0
        output_buffer = bitarray(endian='big')

        try:
            with open(input_file_path, 'rb') as input_file:
                data = input_file.read()
        except IOError:
            print('Could not open input file ...')
            raise

        while i < len(data):
            match = self.findLongestMatch(data, i)

            if match:
                (bestMatchDistance, bestMatchLength) = match

                output_buffer.append(True)
                output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
                output_buffer.frombytes(bytes([((bestMatchDistance & 0xf) << 4) | bestMatchLength]))

                if verbose:
                    print("<1, %i, %i>" % (bestMatchDistance, bestMatchLength), end='')

                i = i + bestMatchLength

            else:
                output_buffer.append(False)
                output_buffer.frombytes(bytes([data[i]]))

                if verbose:
                    print("<0, %s>" % data[i], end='')

                i += 1

        output_buffer.fill()

        if output_file_path:
            try:
                Path("results/lz77").mkdir(parents=True, exist_ok=True)
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(output_buffer.tobytes())
                    print("File was compressed successfully and saved to output path ...")
                    return None
            except IOError:
                print('Could not write to output file path. Please check if the path is correct ...')
                raise

        return output_buffer

    def decompress(self, input_file_path, output_file_path=None):
        """
        Given a string of the compressed file path, the data is decompressed back to its
        original form, and written into the output file path if provided. If no output
        file path is provided, the decompressed data is returned as a string
        """
        data = bitarray(endian='big')
        output_buffer = []

        # read the input file
        try:
            with open(input_file_path, 'rb') as input_file:
                data.fromfile(input_file)
        except IOError:
            print('Could not open input file ...')
            raise

        while len(data) >= 9:
            flag = data.pop(0)

            if not flag:
                byte = data[:8].tobytes()
                output_buffer.append(byte)
                del data[:8]
            else:
                byte1 = int.from_bytes(data[:8].tobytes(), 'big')
                byte2 = int.from_bytes(data[8:16].tobytes(), 'big')

                del data[:16]
                distance = (byte1 << 4) | (byte2 >> 4)
                length = (byte2 & 0xf)

                for i in range(length):
                    output_buffer.append(output_buffer[-distance])
        out_data = b''.join(output_buffer)

        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(out_data)
                    print('File was decompressed successfully and saved to output path ...')
                    return None
            except IOError:
                print('Could not write to output file path. Please check if the path is correct ...')
                raise
        return out_data

    def findLongestMatch(self, data, current_position):
        """
        Finds the longest match to a substring starting at the current_position
        in the lookahead buffer from the history window
        """
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data) + 1)

        best_match_distance = -1
        best_match_length = -1

        for j in range(current_position + 2, end_of_buffer):
            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]

            for i in range(start_index, current_position):
                repetitions = len(substring) // (current_position - i)
                last = len(substring) % (current_position - i)
                matched_string = data[i:current_position] * repetitions + data[i:i + last]

                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = len(substring)

        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None

def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size

if __name__ == "__main__":

    input_file = "test/1.txt"
    encoded_file = "results/lz77/comp.txt"
    output_file = "results/lz77/decomp.txt"

    lz77 = LZ77Compressor()

    lz77.compress(input_file_path=input_file, output_file_path=encoded_file)

    lz77.decompress(input_file_path=encoded_file, output_file_path=output_file)

    print("Encoding and decoding completed successfully.")

    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    
    ratio = calculate_compression_ratio(original_size, compressed_size)
    print(f"Compression Ratio: {ratio:.2f}")