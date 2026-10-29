"""Rotas de consulta às tolerâncias."""

from fastapi import APIRouter

from ..banco import Conexao
from ..modelos import Linha, Tolerancia
from ..regras import limites

router = APIRouter(prefix="/linhas", tags=["tolerâncias"])


@router.get("/{linha}/tolerancias", summary="Tolerâncias de uma linha")
def listar_tolerancias(linha: Linha, con: Conexao) -> list[Tolerancia]:
    """Devolve a faixa (mínimo e máximo) de cada ensaio da linha.

    Tolerâncias do tipo nominal ± % já vêm convertidas em mínimo e máximo.
    """
    linhas = con.execute(
        "SELECT * FROM tolerancias WHERE linha = ? ORDER BY ensaio", (linha,)
    ).fetchall()
    resultado = []
    for t in linhas:
        minimo, maximo = limites(t["tipo"], t["minimo"], t["maximo"], t["nominal"], t["percentual"])
        resultado.append(
            Tolerancia(linha=linha, ensaio=t["ensaio"], tipo=t["tipo"], minimo=minimo, maximo=maximo)
        )
    return resultado
