from pyldpc import make_ldpc, encode, decode, get_message
import numpy as np

# Parametri
n = 15
d_v = 3  # broj jedinica po koloni (wc)
d_c = 5  # broj jedinica po redu (wr)
seed = 12345  # zamenite svojim ID brojem

# Generisanje matrice H
H, G = make_ldpc(n, d_v, d_c, systematic=True, seed=seed)

print("Matrica H:")
print(H)
