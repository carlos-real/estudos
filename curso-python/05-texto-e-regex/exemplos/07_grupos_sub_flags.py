"""Exemplo 07 — Grupos, re.sub, re.split e flags (seções 12 a 14).

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/07_grupos_sub_flags.py
"""

import re

# Grupos nomeados: o Match vira dicionário.
padrao = r"(?P<ensaio>[^:]+):\s*(?P<valor>[\d.,]+)\s*(?P<unidade>\S*)"
for linha in ["Espessura: 25,4 µm", "COF estático: 0,21", "Tração MD: 32 MPa"]:
    achado = re.fullmatch(padrao, linha)
    print(achado.groupdict())

# Guloso x preguiçoso
obs = 'Obs: "COF liberado" e "Selagem ok"'
print("guloso     :", re.findall(r'"(.*)"', obs))
print("preguiçoso :", re.findall(r'"(.*?)"', obs))

# re.sub com grupos e com função
print(re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", "Produzido em 05/03/2025"))
print(re.sub(r"\d+,\d+", lambda m: m.group().replace(",", "."), "Espessura 25,4 e 23,1"))

# re.split com vários separadores
print(re.split(r"\s*[|;]\s*", "OP: 123456 | NF: 98765; Peso: 980 kg"))

# MULTILINE: ^ vale para cada linha
email = "Assunto: carga\nOP 123456\nobs: a OP 999999 saiu\nOP 654321"
print("sem MULTILINE:", re.findall(r"^OP (\d{6})", email))
print("com MULTILINE:", re.findall(r"^OP (\d{6})", email, flags=re.MULTILINE))

# VERBOSE + compile: a regex "em pé", comentada
PADRAO_OP = re.compile(
    r"""
    \b OP        # a sigla, como palavra inteira
    [\s:-]*      # separador opcional
    (\d{6})      # 6 dígitos (grupo 1)
    \b           # nada colado depois
    """,
    re.VERBOSE | re.IGNORECASE,
)
print(PADRAO_OP.findall("Liberar OP: 123456, op-654321 e a TOP 111111"))
