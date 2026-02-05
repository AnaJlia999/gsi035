import hashlib
from typing import List

Bits = List[int]

def GEN(seed: Bits) -> Bits:
    """
    Gera a chave K usando SHA-256 a partir da seed fornecida.
    """
    # 1) Converte a seed em string (ex: [1,0,1,1] -> "1011")
    seed_str = "".join(str(b) for b in seed)

    # 2) Gera o hash SHA-256 (resultado em hexadecimal)
    hash_hex = hashlib.sha256(seed_str.encode()).hexdigest()

    # 3) Converte o hash hexadecimal em bits
    hash_bits: Bits = []
    for c in hash_hex:
        # cada caractere hexadecimal vira 4 bits
        hash_bits.extend([int(b) for b in f"{int(c, 16):04b}"])

    # 4) Retorna apenas o número de bits necessário
    tamanho = 4 * len(seed)
    return hash_bits[:tamanho]


def ENC(K: Bits, M: Bits) -> Bits:
    """
    Criptografia (difusão forward + XOR com chave)

    1) Difusão forward (XOR em cadeia):
       x[i] = x[i] XOR x[i-1]
    2) Cifra:
       C[i] = x[i] XOR K[i]
    """
    # difusão forward
    x = M[:]
    for i in range(1, len(x)):
        x[i] ^= x[i - 1]

    # XOR com chave
    return [xi ^ ki for xi, ki in zip(x, K)]

def DEC(K: Bits, C: Bits) -> Bits:
    """
    Descriptografia

    1) Remove a chave:
       x[i] = C[i] XOR K[i]
    2) Desfaz a difusão forward (voltando da direita para esquerda):
       M[i] = M[i] XOR M[i-1]
    """
    # remove chave
    x = [ci ^ ki for ci, ki in zip(C, K)]

    # desfaz difusão forward (inverso)
    M = x[:]
    for i in range(len(M) - 1, 0, -1):
        M[i] ^= M[i - 1]

    return M

if __name__ == "__main__":
    # Seed (entrada)
    seed = [1, 0, 1, 1, 0, 1, 0, 0]   # 8 bits

    # Gera chave K com SHA-256
    K = GEN(seed)                     # tamanho = 4*8 = 32 bits

    # Mensagem precisa ter o mesmo tamanho da chave
    M = [
        0,1,0,1, 1,0,1,0,
        1,1,0,0, 0,0,1,1,
        1,0,0,1, 0,1,1,0,
        1,0,1,0, 0,1,0,1
    ]

    C = ENC(K, M)
    M2 = DEC(K, C)

    print("Seed:", seed)
    print("K:", K)
    print("M:", M)
    print("C:", C)
    print("DEC:", M2)
    print("OK?", M2 == M)
