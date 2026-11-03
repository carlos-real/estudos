"""
Exercício 10.02 — Ler CSV brasileiro (SOLUÇÃO)

Cada parâmetro resolve um problema específico do CSV "à brasileira":
  sep=";"            -> o Excel BR separa colunas com ponto e vírgula
  decimal=","        -> 38,1 vira 38.1
  thousands="."      -> 1.558,5 vira 1558.5 (sem isso, a coluna fica como texto)
  encoding=...       -> como os bytes viram letras (ç, ã, é)
  dtype={"op": str}  -> OP é código: 024412 não pode virar o número 24412
"""

from pathlib import Path

import pandas as pd


def ler_medicoes(caminho: str | Path) -> pd.DataFrame:
    """Lê o CSV de medições no padrão do Excel brasileiro."""
    # "utf-8-sig" é o UTF-8 que aceita (e descarta) o BOM, a marca invisível que
    # o Excel põe no começo do arquivo quando você salva como "CSV UTF-8".
    return pd.read_csv(
        caminho,
        sep=";",
        decimal=",",
        thousands=".",
        encoding="utf-8-sig",
        dtype={"op": str},
    )


def ler_ops_erp(caminho: str | Path) -> pd.DataFrame:
    """Lê o CSV de OPs exportado do ERP (cp1252)."""
    # cp1252 é o encoding padrão do Windows em português. Ler esse arquivo como
    # UTF-8 dá UnicodeDecodeError no primeiro acento.
    return pd.read_csv(
        caminho,
        sep=";",
        decimal=",",
        thousands=".",
        encoding="cp1252",
        dtype={"op": str},
    )
