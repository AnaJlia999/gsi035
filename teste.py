import random
import time

from crypto import GEN, ENC, DEC

# --------------------------------------------------
# Utils
# --------------------------------------------------

def random_bits(n):
    return [random.randint(0, 1) for _ in range(n)]

def flip_bit(bits, pos):
    new = bits[:]
    new[pos] ^= 1
    return new

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))


# --------------------------------------------------
# 1) Tempo
# --------------------------------------------------

def teste_tempo(seed_size=64, msg_size=256, rounds=1000):
    print("\n=== TESTE DE TEMPO ===")

    seed = random_bits(seed_size)
    M = random_bits(msg_size)
    K = GEN(seed)[:msg_size]

    inicio = time.perf_counter()

    for _ in range(rounds):
        C = ENC(K, M)
        _ = DEC(K, C)

    fim = time.perf_counter()

    print(f"Tempo médio: {(fim - inicio)/rounds:.6f}s")


# --------------------------------------------------
# 2) Chaves equivalentes
# --------------------------------------------------

def teste_chaves_equivalentes(seed_size=64, msg_size=256, testes=2000):
    print("\n=== TESTE CHAVES EQUIVALENTES ===")

    M = random_bits(msg_size)
    resultados = {}
    colisoes = 0

    for _ in range(testes):
        seed = random_bits(seed_size)
        K = GEN(seed)[:msg_size]
        C = tuple(ENC(K, M))

        if C in resultados:
            colisoes += 1
        else:
            resultados[C] = True

    print(f"Colisões: {colisoes}")


# --------------------------------------------------
# 3) Difusão
# --------------------------------------------------

def teste_difusao(seed_size=64, msg_size=256, testes=500):
    print("\n=== TESTE DIFUSÃO ===")

    seed = random_bits(seed_size)
    K = GEN(seed)[:msg_size]

    mudancas = []

    for _ in range(testes):
        M = random_bits(msg_size)
        C1 = ENC(K, M)

        pos = random.randint(0, msg_size - 1)
        M2 = flip_bit(M, pos)

        C2 = ENC(K, M2)

        mudancas.append(hamming_distance(C1, C2))

    media = sum(mudancas) / len(mudancas)
    print(f"Média bits alterados: {media:.2f} ({(media/msg_size)*100:.2f}%)")


# --------------------------------------------------
# 4) Confusão
# --------------------------------------------------

def teste_confusao(seed_size=64, msg_size=256, testes=500):
    print("\n=== TESTE CONFUSÃO ===")

    M = random_bits(msg_size)
    mudancas = []

    for _ in range(testes):
        seed = random_bits(seed_size)

        K1 = GEN(seed)[:msg_size]
        C1 = ENC(K1, M)

        pos = random.randint(0, seed_size - 1)
        seed2 = flip_bit(seed, pos)

        K2 = GEN(seed2)[:msg_size]
        C2 = ENC(K2, M)

        mudancas.append(hamming_distance(C1, C2))

    media = sum(mudancas) / len(mudancas)
    print(f"Média bits alterados: {media:.2f} ({(media/msg_size)*100:.2f}%)")


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    teste_tempo()
    teste_chaves_equivalentes()
    teste_difusao()
    teste_confusao()
