"""
Exercício 11.13 — Revisão: importar a planilha da expedição (SOLUÇÃO)

Separação de responsabilidades:
  - converter_linha: Python puro, valida e converte UMA linha (ou levanta ValueError);
  - importar_expedicao: lê o arquivo, junta as válidas e grava tudo de uma vez.
"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path


def numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5 (módulo 05)."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def converter_linha(registro: dict, ops_existentes: set[int]) -> tuple[int, str, float, str]:
    """Valida um registro do CSV e devolve a tupla pronta para o INSERT."""
    op = int(registro["op"])  # "abc" -> ValueError
    if op not in ops_existentes:
        raise ValueError(f"OP {op} não cadastrada")
    nf = (registro["nf"] or "").strip()
    if not nf:
        raise ValueError("NF vazia")
    peso = numero_br(registro["peso"])
    if peso <= 0:
        raise ValueError("peso deve ser maior que zero")
    data = datetime.strptime(registro["data"].strip(), "%d/%m/%Y").date()  # 31/09 -> erro
    return op, nf, peso, data.isoformat()  # 'AAAA-MM-DD'


def importar_expedicao(
    conexao: sqlite3.Connection, caminho: str | Path
) -> tuple[int, list[int]]:
    """Importa as cargas válidas e devolve (inseridas, linhas com erro)."""
    # Um SELECT só, antes do laço: consultar o banco a cada linha seria lento.
    ops_existentes = {numero for (numero,) in conexao.execute("SELECT numero FROM op")}

    validas: list[tuple[int, str, float, str]] = []
    erros: list[int] = []
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for numero_linha, registro in enumerate(leitor, start=2):  # linha 1 = cabeçalho
            try:
                validas.append(converter_linha(registro, ops_existentes))
            except (ValueError, TypeError, AttributeError):
                # ValueError: número/data inválidos; TypeError/AttributeError: campo
                # faltando (o DictReader põe None quando a linha tem menos colunas).
                erros.append(numero_linha)

    with conexao:  # tudo ou nada
        conexao.executemany(
            "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)", validas
        )
    return len(validas), erros
