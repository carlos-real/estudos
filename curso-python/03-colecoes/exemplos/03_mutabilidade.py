"""Exemplo 03 — Mutabilidade: cópia x referência.

Rode na pasta 03-colecoes:  python exemplos/03_mutabilidade.py
Dica: cole este código em https://pythontutor.com para VER as setas.
"""

import copy

print("--- 1. Atribuir NÃO copia ---")
a = [50.2, 49.8]
b = a  # b é outra etiqueta para a MESMA lista
b.append(51.0)
print("a:", a)
print("b:", b)
print("a is b?", a is b)

print("\n--- 2. Copiando de verdade ---")
original = [50.2, 49.8]
copia = original.copy()  # também: original[:] ou list(original)
copia.append(51.0)
print("original:", original)
print("copia:   ", copia)
print("original == copia?", original == copia, "| original is copia?", original is copia)

print("\n--- 3. Imutáveis: 'mudar' cria outro objeto ---")
x = 10
y = x
x += 1
print("x:", x, "| y:", y)

print("\n--- 4. Cópia rasa x cópia profunda ---")
por_linha = {"A": [50.2, 49.8], "B": [20.1]}
rasa = por_linha.copy()
profunda = copy.deepcopy(por_linha)
rasa["A"].append(99.9)  # mexe na lista INTERNA, que é compartilhada
print("original:", por_linha)
print("rasa:    ", rasa)
print("profunda:", profunda)

print("\n--- 5. A armadilha da grade [[0] * 3] * 3 ---")
grade_errada = [[0] * 3] * 3
grade_errada[0][0] = 1
print("errada:", grade_errada)
grade_certa = [[0] * 3 for _ in range(3)]
grade_certa[0][0] = 1
print("certa: ", grade_certa)

print("\n--- 6. Funções recebem o MESMO objeto ---")


def zerar_negativos_no_lugar(valores):
    for i in range(len(valores)):
        if valores[i] < 0:
            valores[i] = 0.0


def sem_negativos(valores):
    return [max(valor, 0.0) for valor in valores]


leituras = [0.5, -0.2, 0.3]
nova = sem_negativos(leituras)
print("sem_negativos devolveu", nova, "e leituras continua", leituras)
zerar_negativos_no_lugar(leituras)
print("depois de zerar_negativos_no_lugar, leituras virou", leituras)
