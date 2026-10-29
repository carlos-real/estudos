"""
Exercício 10.13 — Revisão: e-mails da expedição viram tabela (SOLUÇÃO)

Divisão de trabalho que vale para qualquer projeto de dados:
  - Python puro (re, dict) cuida de UM item por vez: um e-mail -> um dicionário.
  - pandas cuida do CONJUNTO: lista de dicionários -> tabela -> resumo.
"""

import re

import pandas as pd

# Compilar fora da função: o padrão é montado uma vez só (módulo 05).
PADRAO_OP = re.compile(r"\bOP:\s*(\d+)", re.IGNORECASE)
PADRAO_NF = re.compile(r"\bNF:\s*(\d+)", re.IGNORECASE)
PADRAO_PESO = re.compile(r"\bPeso:\s*([\d.,]+)\s*kg", re.IGNORECASE)

COLUNAS = ["op", "nf", "peso_kg"]


def numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5 (tira o milhar, troca a vírgula decimal)."""
    return float(texto.replace(".", "").replace(",", "."))


def extrair_pedido(texto: str) -> dict | None:
    """Extrai OP, NF e peso de um e-mail (None se faltar algum)."""
    op = PADRAO_OP.search(texto)
    nf = PADRAO_NF.search(texto)
    peso = PADRAO_PESO.search(texto)
    if not (op and nf and peso):  # retorno antecipado (módulo 04)
        return None
    return {
        "op": int(op.group(1)),
        "nf": nf.group(1),  # NF é código: texto, para não perder zeros à esquerda
        "peso_kg": numero_br(peso.group(1)),
    }


def pedidos_para_tabela(emails: list[str]) -> pd.DataFrame:
    """Um pedido válido por linha, nas colunas op, nf e peso_kg."""
    # Compreensão com filtro (módulo 03): extrai e descarta os None.
    pedidos = [p for p in (extrair_pedido(e) for e in emails) if p is not None]
    # columns=... garante as colunas mesmo quando a lista está vazia.
    return pd.DataFrame(pedidos, columns=COLUNAS)


def peso_por_op(pedidos: pd.DataFrame) -> pd.DataFrame:
    """Quantidade de notas e peso total por OP."""
    resumo = pedidos.groupby("op", as_index=False).agg(
        notas=("nf", "count"),
        peso_total_kg=("peso_kg", "sum"),
    )
    return resumo.round({"peso_total_kg": 1})
