"""Histórico de certificados emitidos (para não emitir duas vezes a mesma OP/NF).

Fica num CSV simples (saida/emitidos.csv). Em modo ensaio ele é só LIDO: um ensaio
nunca muda o que a próxima execução vai fazer.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .modelos import ItemFila

CAMPOS = ["op", "nf", "data_hora", "comprovante"]


def carregar_emitidas(caminho: Path) -> set[tuple[str, str]]:
    """Conjunto de (OP, NF) já emitidos. Arquivo inexistente = nada emitido ainda."""
    caminho = Path(caminho)
    if not caminho.exists():
        return set()
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return {(linha["op"], linha["nf"]) for linha in csv.DictReader(arquivo, delimiter=";")}


def registrar_emitidas(caminho: Path, itens: list[ItemFila]) -> int:
    """Acrescenta ao histórico os itens com situação "emitido". Devolve quantos gravou."""
    emitidos = [item for item in itens if item.situacao == "emitido"]
    if not emitidos:
        return 0
    caminho = Path(caminho)
    novo = not caminho.exists()
    agora = datetime.now().isoformat(timespec="seconds")
    with caminho.open("a", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS, delimiter=";")
        if novo:
            escritor.writeheader()
        for item in emitidos:
            escritor.writerow(
                {
                    "op": item.op,
                    "nf": item.nf,
                    "data_hora": agora,
                    "comprovante": item.comprovante,
                }
            )
    return len(emitidos)
