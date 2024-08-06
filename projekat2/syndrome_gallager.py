from itertools import combinations
import numpy as np


def syndrome_table(H):
    m, n = H.shape
    syndrome_dict = {}
    
    for error_weight in range(1, n + 1):
        for error_positions in combinations(range(n), error_weight):
            e = np.zeros(n, dtype=int)
            e[list(error_positions)] = 1
            syndrome = np.dot(H, e) % 2
            syndrome_tuple = tuple(syndrome)
            
            if syndrome_tuple not in syndrome_dict:
                syndrome_dict[syndrome_tuple] = e
                
    return syndrome_dict

syndrome_dict = syndrome_table(H)

# Prikaz tabele sindroma i korektora
print("Tabela sindroma i korektora:")
for syndrome, correction in syndrome_dict.items():
    print(f"Sindrom: {syndrome}, Korektor: {correction}")

# Određivanje kodnog rastojanja
code_distance = min(sum(e) for e in syndrome_dict.values())
print(f"Kodno rastojanje: {code_distance}")


def gallager_b(H, received, max_iter=50, th0=0.5, th1=0.5):
    m, n = H.shape
    llr = np.zeros(n)
    decision = np.zeros(n, dtype=int)
    
    for iteration in range(max_iter):
        llr = np.dot(H, decision) % 2
        decision = (llr >= th1).astype(int)
        
        if np.all(np.dot(H, decision) % 2 == np.zeros(m)):
            break
            
    return decision

# Pronalaženje n-torke greške koju Gallager B ne može ispraviti
def find_failing_error(H, th0=0.5, th1=0.5):
    m, n = H.shape
    
    for error_weight in range(1, n + 1):
        for error_positions in combinations(range(n), error_weight):
            e = np.zeros(n, dtype=int)
            e[list(error_positions)] = 1
            received = (e + np.random.randint(0, 2, n)) % 2
            
            decoded = gallager_b(H, received, th0=th0, th1=th1)
            
            if not np.array_equal(decoded, np.zeros(n)):
                return e
                
    return None

failing_error = find_failing_error(H)
print(f"N-torka greške koju Gallager B ne može ispraviti: {failing_error}")
print(f"Broj jedinica u n-torci greške: {sum(failing_error)}")
print(f"Upoređenje sa kodnim rastojanjem: {sum(failing_error)} vs {code_distance}")
