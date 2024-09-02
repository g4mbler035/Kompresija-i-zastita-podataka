import numpy as np
import random
from itertools import combinations

def generate_H_matrix(n=15, n_minus_k=9, wr=5, wc=3, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    H = np.zeros((n_minus_k, n), dtype=int)

    for i in range(n_minus_k):
        ones_positions = np.random.choice(n, wr, replace=False)
        H[i, ones_positions] = 1

    return H

def generate_syndrome_table(H):
    n_minus_k, n = H.shape
    syndromes = {}
    for weight in range(1, n + 1):
        for error_pattern in combinations(range(n), weight):
            error_vector = np.zeros(n, dtype=int)
            for pos in error_pattern:
                error_vector[pos] = 1
            syndrome = tuple(np.dot(H, error_vector) % 2)
            if syndrome not in syndromes:
                syndromes[syndrome] = error_vector
    return syndromes

def code_distance(syndromes):
    return min(sum(error) for error in syndromes.values())

def gallager_b_algorithm(H, received_word, th0=0.5, th1=0.5, max_iter=100):
    n_minus_k, n = H.shape
    LLR = np.zeros(n)
    for iteration in range(max_iter):
        syndrome = np.dot(H, received_word) % 2
        if np.count_nonzero(syndrome) == 0:
            return received_word

        for i in range(n):
            LLR[i] = np.sum(H[:, i] * (1 - 2 * syndrome))

        received_word = np.where(LLR >= th1, 0, 1)
        received_word = np.where(LLR <= -th0, 1, received_word)
    
    return received_word

def find_uncorrectable_error(H, syndromes, th0=0.5, th1=0.5, max_iter=100):
    for syndrome, error_vector in syndromes.items():
        corrupted_word = (error_vector + np.random.randint(2, size=H.shape[1])) % 2
        decoded_word = gallager_b_algorithm(H, corrupted_word, th0, th1, max_iter)
        if not np.array_equal(decoded_word, np.zeros(H.shape[1], dtype=int)):
            return error_vector
    return None

if __name__ == "__main__":
    index_number = 12345

    H = generate_H_matrix(seed=index_number)
    print("H matrix:")
    print(H)

    syndromes = generate_syndrome_table(H)
    d_min = code_distance(syndromes)
    print(f"Code distance (d_min): {d_min}")

    uncorrectable_error = find_uncorrectable_error(H, syndromes)
    print("Uncorrectable error vector:")
    print(uncorrectable_error)
    print(f"Weight of the uncorrectable error vector: {np.sum(uncorrectable_error)}")
    print(f"Comparison with code distance: {d_min}")
