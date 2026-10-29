"""
Exercício 10.05 — Todas as abas numa tabela só (SOLUÇÃO)

Raciocínio:
1. Primeiro descobrir os NOMES das abas (pd.ExcelFile(...).sheet_names) e
   escolher só as de linha. Por que não ler tudo com sheet_name=None? Porque
   header=1 vale para TODAS as abas, e uma aba de uma linha só ("Instruções")
   faz o read_excel falhar com ValueError. Escolher antes evita o problema.
2. Ler só essas abas: sheet_name=[lista] também devolve {nome: DataFrame}.
3. Percorrer o dicionário (módulo 03) acrescentando a coluna "linha".
4. Empilhar as partes com pd.concat e arrumar nomes e ordem das colunas.
"""

from pathlib import Path

import pandas as pd

NOMES = {"OP": "op", "Bobina": "bobina", "Espessura (µm)": "espessura_um"}


def ler_todas_as_abas(caminho: str | Path) -> pd.DataFrame:
    """Junta as abas 'Linha X' numa tabela com a coluna 'linha'."""
    with pd.ExcelFile(caminho) as arquivo:  # abre uma vez, lê os nomes das abas
        nomes = [nome for nome in arquivo.sheet_names if nome.startswith("Linha ")]
        if not nomes:
            raise ValueError("nenhuma aba 'Linha X' encontrada na planilha")
        # header=1: o cabeçalho está na SEGUNDA linha (a primeira é o título).
        # dtype vale para todas as abas e mantém a OP como texto.
        abas = pd.read_excel(arquivo, sheet_name=nomes, header=1, dtype={"OP": str})

    partes = []
    for nome, tabela in abas.items():  # o dicionário mantém a ordem das abas
        letra = nome.removeprefix("Linha ").strip()
        # assign devolve uma cópia com a coluna nova (não mexe em 'tabela')
        partes.append(tabela.assign(linha=letra))

    # ignore_index=True renumera 0, 1, 2... (sem ele, cada aba recomeçaria do 0)
    juntas = pd.concat(partes, ignore_index=True).rename(columns=NOMES)
    return juntas[["linha", "op", "bobina", "espessura_um"]]
