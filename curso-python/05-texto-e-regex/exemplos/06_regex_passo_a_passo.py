"""Exemplo 06 — Construindo uma regex aos poucos (seções 9 a 11).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/06_regex_passo_a_passo.py
"""

import re

EXEMPLOS = [
    "OP 123456",  # devem casar...
    "OP-123456",
    "OP123456",
    "op 123456",
    "OP 12345",  # ...e estes NÃO
    "OP 1234567",
    "OS 123456",
]


def testar(padrao, exemplos, flags=0):
    """Mostra ✔/✘ para cada exemplo: o texto inteiro casa com o padrão?"""
    for texto in exemplos:
        casou = re.fullmatch(padrao, texto, flags)
        print("  ✔" if casou else "  ✘", repr(texto))


passos = [
    ("Passo 1: OP, espaço, dígitos", r"OP \d+", 0),
    ("Passo 2: exatamente 6 dígitos", r"OP \d{6}", 0),
    ("Passo 3: separador opcional", r"OP[ -]?\d{6}", 0),
    ("Passo 4: ignorar maiúsculas", r"OP[ -]?\d{6}", re.IGNORECASE),
]
for titulo, padrao, flags in passos:
    print(f"{titulo}  ->  {padrao}")
    testar(padrao, EXEMPLOS, flags)

print("\nsearch x match x fullmatch em 'Liberar OP 123456 hoje':")
texto = "Liberar OP 123456 hoje"
print("  search   :", re.search(r"OP \d{6}", texto))
print("  match    :", re.match(r"OP \d{6}", texto))
print("  fullmatch:", re.fullmatch(r"OP \d{6}", texto))

print("\nfindall sem e com \\b:")
texto = "OP 123456, OP 7654321, op 111111"
print("  ", re.findall(r"OP \d{6}", texto))
print("  ", re.findall(r"\bOP \d{6}\b", texto, re.IGNORECASE))
