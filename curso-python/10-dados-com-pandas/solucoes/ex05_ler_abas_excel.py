"""
Exercício 10.05 — Todas as abas numa tabela só (SOLUÇÃO)

Raciocínio:
1. Ler tudo de uma vez: sheet_name=None devolve {nome_da_aba: DataFrame}.
2. Percorrer o dicionário (módulo 03), guardando só as abas de linha e
   acrescentando a coluna "linha" em cada parte.
3. Empilhar as partes com pd.concat e arrumar nomes e ordem das colunas.
"""

from pathlib import Path

import pandas as pd

NOMES = {"OP": "op", "Bobina": "bobina", "Espessura (µm)": "espessura_um"}


def ler_todas_as_abas(caminho: str | Path) -> pd.DataFrame:
    """Junta as abas 'Linha X' numa tabela com a coluna 'linha'."""
    # header=1: o cabeçalho está na SEGUNDA linha (a primeira é o título).
    # dtype vale para todas as abas e mantém a OP como texto.
    abas = pd.read_excel(caminho, sheet_name=None, header=1, dtype={"OP": str})

    partes = []
    for nome, tabela in abas.items():  # o dicionário mantém a ordem das abas
        if not nome.startswith("Linha "):
            continue  # "Instruções", "Resumo" etc. ficam de fora
        letra = nome.removeprefix("Linha ").strip()
        # assign devolve uma cópia com a coluna nova (não mexe em 'tabela')
        partes.append(tabela.assign(linha=letra))

    if not partes:
        raise ValueError("nenhuma aba 'Linha X' encontrada na planilha")

    # ignore_index=True renumera 0, 1, 2... (sem ele, cada aba recomeçaria do 0)
    juntas = pd.concat(partes, ignore_index=True).rename(columns=NOMES)
    return juntas[["linha", "op", "bobina", "espessura_um"]]
