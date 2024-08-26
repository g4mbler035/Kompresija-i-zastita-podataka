import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message

# Parameters
n = 15
k = 9  # This should be inferred from G, but here it's set for clarity
d_v = 3  # Number of 1s in each column (variable nodes)
d_c = 5  # Number of 1s in each row (check nodes)
seed = 123  # Seed for random number generator
snr = 20  # Signal to Noise Ratio

# 1. Generate LDPC matrix
np.random.seed(seed)
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=False, seed=seed)
k = G.shape[1]

print("H matrix shape:", H.shape)
print("G matrix shape:", G.shape)

# 2. Generate syndrome table and correctors
def syndrome_table(H):
    m, n = H.shape
    syndrome_tbl = {}
    for i in range(2**m):
        e = np.zeros(n, dtype=int)
        for bit in range(m):
            e[bit] = (i >> bit) & 1
        syndrome = (H @ e) % 2
        syndrome_tuple = tuple(syndrome)
        if syndrome_tuple not in syndrome_tbl:
            syndrome_tbl[syndrome_tuple] = e
    return syndrome_tbl

syndrome_tbl = syndrome_table(H)

# Code distance determination (Hamming distance)
def code_distance(syndrome_tbl):
    distances = [np.sum(e) for e in syndrome_tbl.values()]
    return min(distances)

code_dist = code_distance(syndrome_tbl)

# 3. Implement Gallager B algorithm
def gallager_b_algorithm(H, y, max_iter=50, th0=0.5, th1=0.5):
    m, n = H.shape
    
    # Initialize messages
    LLR = np.random.rand(n) * 2 - 1
    LLR = np.concatenate([LLR, np.zeros(m)])

    for iteration in range(max_iter):
        # Update messages from variable nodes to check nodes
        for j in range(m):
            check_nodes = np.nonzero(H[j])[0]
            for i in check_nodes:
                LLR[j + n] += LLR[i]
        
        # Update messages from check nodes to variable nodes
        for i in range(n):
            variable_nodes = np.nonzero(H[:, i])[0]
            for j in variable_nodes:
                LLR[i] += LLR[j + n]
        
        # Hard decision
        decoded = (LLR[:n] > 0).astype(int)
        if np.all((H @ decoded) % 2 == 0):
            return decoded
        
    return decoded

# Encoding and Decoding Example
v = np.random.randint(2, size=k)
y = encode(G, v, snr)
decoded = decode(H, y, snr)
x = get_message(G, decoded)

# Check if encoding and decoding are successful
assert abs(x - v).sum() == 0

def find_min_error_vector(H, syndrome_table, th0, th1):
    min_error_vector = None
    min_errors = np.inf
    for syndrome, error_vector in syndrome_table.items():
        if np.sum(error_vector) < min_errors:
            min_errors = np.sum(error_vector)
            min_error_vector = error_vector
    return min_error_vector

def print_syndrome_table(syndrome_tbl):
    print("\nSyndrome Table:")
    for syndrome, error_vector in syndrome_tbl.items():
        syndrome_str = ''.join(map(str, syndrome))
        error_vector_str = ''.join(map(str, error_vector))
        print(f"Syndrome: {syndrome_str} -> Error Vector: {error_vector_str}")

error_vector = find_min_error_vector(H, syndrome_tbl, th0=0.5, th1=0.5)

print("LDPC Matrix H:\n", H)
print_syndrome_table(syndrome_table)
print("Code Distance:", code_dist)
print("Decoded Vector:\n", decoded)
print("Error Vector:\n", error_vector)
