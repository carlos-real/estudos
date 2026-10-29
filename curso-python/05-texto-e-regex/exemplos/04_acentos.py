"""Exemplo 04 — Unicode, normalização e remoção de acentos (seção 7).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/04_acentos.py
"""

import unicodedata

composto = "ã"
decomposto = "ã"  # 'a' + til combinante
print("Iguais na tela, diferentes no Python:", composto == decomposto)
print("Depois de normalizar (NFC):", unicodedata.normalize("NFC", decomposto) == composto)

print("\nO que a NFD faz com 'ção':")
for c in unicodedata.normalize("NFD", "ção"):
    print(f"  U+{ord(c):04X} {unicodedata.name(c)} combining={unicodedata.combining(c)}")


def remover_acentos(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join([c for c in decomposto if not unicodedata.combining(c)])


def mesma_pessoa(nome1, nome2):
    """Compara ignorando acentos, maiúsculas e espaços repetidos."""

    def chave(nome):
        return " ".join(remover_acentos(nome).casefold().split())

    return chave(nome1) == chave(nome2)


print()
print(remover_acentos("Tração na ruptura - São Paulo"))
print("NFD  de 'g/m²':", unicodedata.normalize("NFD", "g/m²"))
print("NFKD de 'g/m²':", unicodedata.normalize("NFKD", "g/m²"))
print("'JOÃO  da Silva' e 'joao DA SILVA':", mesma_pessoa("JOÃO  da Silva", "joao DA SILVA"))
