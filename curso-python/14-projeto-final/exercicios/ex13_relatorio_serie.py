"""
Exercício 14.13 — Relatório da série (CSV para o Excel brasileiro)
Nível: ★☆☆

Contexto: No fim da série, a qualidade quer abrir um arquivo no Excel e ver cada
pedido: o que foi (ou seria) emitido, o que ficou bloqueado e por quê. O Excel em
português espera ";" como separador e vírgula decimal, e só reconhece acentos de um
CSV em UTF-8 se o arquivo tiver BOM (encoding "utf-8-sig").

Tarefa: implemente duas funções.
1. `resumir(itens)` devolve {situacao: quantidade}, com as chaves em ordem
   alfabética. Lista vazia -> {}.
2. `escrever_relatorio_csv(itens, caminho)` grava o CSV e devolve o caminho:
   - encoding "utf-8-sig", delimitador ";", newline="" no open;
   - crie a pasta do arquivo se ela não existir;
   - cabeçalho: COLUNAS (pronto abaixo);
   - uma linha por item, na ordem recebida: op, nf, peso com 2 casas e vírgula
     decimal ("1250,50"), especificacao, situacao em MAIÚSCULAS, motivos unidos por
     " | " e comprovante.

Exemplos:
    >>> resumir(itens)
    {'bloqueado': 4, 'ensaio': 2}
    >>> caminho = escrever_relatorio_csv(itens, Path("saida/serie.csv"))
    >>> print(caminho.read_text(encoding="utf-8-sig").splitlines()[1])
    24518;123456;1250,50;PADRAO-A;ENSAIO;;ENSAIO-24518-123456

Dica: collections.Counter conta para você; dict(sorted(contagem.items())) ordena.
csv.writer(arquivo, delimiter=";") e writerow([...]) escrevem cada linha.

Teste com:  python curso.py testar 14 ex13
"""

import csv  # noqa: F401 (você vai usar)
from collections import Counter  # noqa: F401 (você vai usar)
from dataclasses import dataclass, field
from pathlib import Path

# ============================================================================
# PEÇAS PRONTAS (etapas anteriores) — não precisa mexer
# ============================================================================

COLUNAS = ["OP", "NF", "Peso (kg)", "Especificação", "Situação", "Motivos", "Comprovante"]


@dataclass
class ItemFila:
    op: str
    nf: str
    peso_kg: float
    situacao: str
    especificacao: str = ""
    motivos: list[str] = field(default_factory=list)
    comprovante: str = ""


# ============================================================================
# SUA PARTE
# ============================================================================


def resumir(itens: list[ItemFila]) -> dict[str, int]:
    """Quantos itens em cada situação, com as chaves em ordem alfabética."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def escrever_relatorio_csv(itens: list[ItemFila], caminho: Path) -> Path:
    """Grava o relatório da série em CSV (padrão Excel brasileiro)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
