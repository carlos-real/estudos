"""Rotas de medições: registrar (avaliando contra a tolerância) e situação da OP."""

from fastapi import APIRouter, HTTPException, status

from ..banco import Conexao
from ..modelos import MedicaoAvaliada, MedicaoEntrada, SituacaoOP
from ..regras import dentro, limites

router = APIRouter(tags=["medições"])


@router.post(
    "/medicoes",
    status_code=status.HTTP_201_CREATED,
    summary="Registra e avalia uma medição",
)
def registrar_medicao(entrada: MedicaoEntrada, con: Conexao) -> MedicaoAvaliada:
    tol = con.execute(
        "SELECT * FROM tolerancias WHERE linha = ? AND ensaio = ?",
        (entrada.linha, entrada.ensaio),
    ).fetchone()
    if tol is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Sem tolerância para linha {entrada.linha} / ensaio {entrada.ensaio}",
        )
    minimo, maximo = limites(tol["tipo"], tol["minimo"], tol["maximo"], tol["nominal"], tol["percentual"])
    aprovado = dentro(entrada.valor, minimo, maximo)
    with con:
        cursor = con.execute(
            "INSERT INTO medicoes (op, linha, ensaio, valor, aprovado) VALUES (?, ?, ?, ?, ?)",
            (entrada.op, entrada.linha, entrada.ensaio, entrada.valor, aprovado),
        )
    return MedicaoAvaliada(
        id=cursor.lastrowid,
        **entrada.model_dump(),
        minimo=minimo,
        maximo=maximo,
        aprovado=aprovado,
    )


@router.get("/ops/{op}/situacao", summary="Situação de uma OP")
def situacao_da_op(op: str, con: Conexao) -> SituacaoOP:
    total, reprovadas = con.execute(
        "SELECT COUNT(*), COALESCE(SUM(aprovado = 0), 0) FROM medicoes WHERE op = ?", (op,)
    ).fetchone()
    if total == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"OP {op} sem medições")
    return SituacaoOP(op=op, medicoes=total, reprovadas=reprovadas, liberada=reprovadas == 0)
