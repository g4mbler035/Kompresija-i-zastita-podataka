def files_have_same_content(file_path1, file_path2):
    """Check if two files have the same content."""
    try:
        with open(file_path1, 'rb') as file1, open(file_path2, 'rb') as file2:
            while True:
                chunk1 = file1.read(8192)
                chunk2 = file2.read(8192)
                if chunk1 != chunk2:
                    return False
                if not chunk1:  # End of both files
                    return True
    except FileNotFoundError:
        print("One or both files not found.")
        return False
    except IOError as e:
        print(f"An I/O error occurred: {e}")
        return False
    
def calculate_compression_ratio(original_size, compressed_size):
    if compressed_size == 0:
        return float('inf')
    return original_size / compressed_size