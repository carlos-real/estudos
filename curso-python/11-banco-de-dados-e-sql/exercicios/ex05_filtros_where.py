"""
Exercício 11.05 — Filtros com WHERE
Nível: ★☆☆

Contexto: o PCP pede listas rápidas: as OPs de uma linha num período, os
ensaios que ainda não foram medidos e os produtos que contêm um trecho no nome.

Tarefa: use o banco do laboratório. Implemente três funções (com parâmetros):
  1. ops_da_linha_no_periodo(conexao, linha, inicio, fim): números das OPs da
     linha com emissão entre inicio e fim (datas 'AAAA-MM-DD', inclusive),
     ordenados por emissão e depois por número.
  2. ensaios_pendentes(conexao): tuplas (op, bobina, caracteristica) dos ensaios
     sem valor, ordenadas por op, bobina, caracteristica.
  3. buscar_produtos(conexao, trecho): nomes de produto, SEM repetição e em
     ordem alfabética, que contêm o trecho (maiúsculas e minúsculas tanto faz).

Exemplos:
    >>> ops_da_linha_no_periodo(conexao, "A", "2026-10-20", "2026-10-20")
    [24518, 24519]
    >>> ensaios_pendentes(conexao)
    [(24534, 2, 'cof')]
    >>> buscar_produtos(conexao, "laminado")
    ['Laminado BOPP/PE 55 µm', 'Laminado PET/PE 62 µm']

Dica: BETWEEN, IS NULL (nunca "= NULL"), LIKE com '%' || ? || '%', DISTINCT.

Teste com:  python curso.py testar 11 ex05
"""

import sqlite3


def ops_da_linha_no_periodo(
    conexao: sqlite3.Connection, linha: str, inicio: str, fim: str
) -> list[int]:
    """Números das OPs da linha emitidas no período (inclusive)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ensaios_pendentes(conexao: sqlite3.Connection) -> list[tuple[int, int, str]]:
    """Ensaios ainda sem valor."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def buscar_produtos(conexao: sqlite3.Connection, trecho: str) -> list[str]:
    """Produtos (sem repetição) que contêm o trecho."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
