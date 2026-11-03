"""
Exercício 11.14 — Revisão: emitir certificados numa transação (SOLUÇÃO)

Plano:
1. Um SELECT descobre as cargas elegíveis (as regras de negócio ficam no SQL,
   onde estão os dados).
2. Um SELECT descobre o último número do ano.
3. Dentro de "with conexao:", um INSERT por carga. Se um falhar, o with desfaz
   todos (rollback) e a exceção sobe.
"""

import sqlite3
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Certificado:
    """Certificado emitido (já pronto, não precisa mexer)."""

    numero: str
    op: int
    nf: str
    peso_kg: float
    emitido_em: str


CARGAS_ELEGIVEIS = """
    SELECT x.id, x.op, x.nf, x.peso_kg
    FROM expedicao AS x
    JOIN op AS o ON o.numero = x.op
    WHERE o.status = 'LIBERADA'
      AND NOT EXISTS (SELECT 1 FROM certificado AS c WHERE c.expedicao_id = x.id)
      AND EXISTS (SELECT 1 FROM ensaio AS e WHERE e.op = x.op)
      AND NOT EXISTS (
          SELECT 1 FROM ensaio AS e
          WHERE e.op = x.op AND (e.resultado = 'FORA' OR e.valor IS NULL)
      )
    ORDER BY x.id
"""


def ultimo_sequencial(conexao: sqlite3.Connection, ano: int) -> int:
    """Maior NNNN já usado em 'CQ-ano-NNNN' (0 se nenhum)."""
    # Como NNNN tem sempre 4 dígitos, o MAX de texto é também o maior número.
    (maior,) = conexao.execute(
        "SELECT MAX(numero) FROM certificado WHERE numero LIKE ?", (f"CQ-{ano}-%",)
    ).fetchone()
    return int(maior[-4:]) if maior else 0


def emitir_certificados(conexao: sqlite3.Connection, data: date) -> list[Certificado]:
    """Emite os certificados pendentes e devolve a lista, em ordem de carga."""
    cargas = conexao.execute(CARGAS_ELEGIVEIS).fetchall()
    if not cargas:
        return []

    sequencial = ultimo_sequencial(conexao, data.year)
    emitido_em = data.isoformat()
    emitidos: list[Certificado] = []
    with conexao:  # tudo ou nada
        for expedicao_id, op, nf, peso in cargas:
            sequencial += 1
            numero = f"CQ-{data.year}-{sequencial:04d}"
            conexao.execute(
                "INSERT INTO certificado (numero, expedicao_id, emitido_em) VALUES (?, ?, ?)",
                (numero, expedicao_id, emitido_em),
            )
            emitidos.append(Certificado(numero, op, nf, peso, emitido_em))
    return emitidos
