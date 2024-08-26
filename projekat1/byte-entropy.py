import math
import sys
import os
import mmap

_UTF8_DISTINCT_VALUES = 256

def byte_entropy(object):
    """
    Return entropy value of object in [0 .. 1] range
    0 means no entropy, 1 is very high randomness

    object can be either a filename (will look at the file contents)
    or a string (will look at the string value directly)

    Examples:
        $ byte-entropy aaaaaaaaaaaaaaaaaa
        0

        $ byte-entropy asjkhdakjfhdslkghf
        0.385756

        # Well compressed file with gzip -9 (should have high entropy):
        $ byte-entropy xx.gz
        0.976236
    """
    fh = None

    if os.path.exists(object):
        fh = open(object)
        object = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)

    counts = [0] * _UTF8_DISTINCT_VALUES
    total_count = 0
    for b in object:
        counts[b if isinstance(b, int) else ord(b)] += 1
        total_count += 1

    if fh:
        object.close()
        fh.close()

    entropy = 0.0

    for count in counts:
        if count == 0:
            continue

        p = 1.0 * count / total_count
        entropy -= p * math.log2(p)
    
    max_entropy = math.log2(_UTF8_DISTINCT_VALUES)
    normalized_entropy = entropy / max_entropy

    return normalized_entropy




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("File not provided! Closing..")
        sys.exit(1)

    for object in sys.argv[1:]:
        entropy = byte_entropy(object)
        print(f"Entropy of the given file: {entropy}")
