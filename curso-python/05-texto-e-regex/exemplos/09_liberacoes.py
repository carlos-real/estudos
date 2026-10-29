"""Exemplo 09 — No mundo real: lendo a observação de liberação da planilha.

Rode na pasta curso-python:
    python 05-texto-e-regex/exemplos/09_liberacoes.py
"""

import re
import unicodedata

PADRAO_ITEM = re.compile(
    r"""
    (?P<ensaio>[a-z ]+?)   # nome do ensaio (já sem acento e minúsculo)
    \s* [:-]? \s*          # separador opcional
    (?P<status>[a-z]+)     # a palavra do status
    $
    """,
    re.VERBOSE,
)


def normalizar(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join([c for c in decomposto if not unicodedata.combining(c)])
    return " ".join(sem_acento.casefold().split())


def ler_liberacoes(observacao):
    resultado = {}
    for pedaco in re.split(r"[;,]", observacao):
        pedaco = normalizar(pedaco)
        achado = PADRAO_ITEM.match(pedaco)
        if not achado:
            continue
        status = "liberado" if achado["status"].startswith("liberad") else achado["status"]
        resultado[achado["ensaio"].strip()] = status
    return resultado


observacoes = [
    "COF: liberado",
    "cof LIBERADO",
    "Tração: Liberada; COF: reprovado",
    "Selagem - PENDENTE, cof: liberado",
]
for obs in observacoes:
    liberacoes = ler_liberacoes(obs)
    pode_emitir = all(s == "liberado" for s in liberacoes.values())
    print(f"{obs:<36} -> {liberacoes} | emitir? {'sim' if pode_emitir else 'não'}")
