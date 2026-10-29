"""
Exercício 13.06 — Rota que valida uma medição contra a tolerância (SOLUÇÃO)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

TOLERANCIAS = {
    "A": {"espessura": (18.0, 22.0), "cof": (0.2, 0.3)},
    "B": {"espessura": (38.0, 42.0), "gramatura": (36.5, 39.5)},
    "C": {"tracao": (25.0, 40.0)},
}


def avaliar(valor: float, minimo: float, maximo: float) -> tuple[bool, float]:
    """(aprovado, margem até o limite mais próximo)."""
    # A regra de negócio fica numa função PURA, fora da rota: dá para testar
    # sem FastAPI e reaproveitar em outro lugar (no robô, num relatório...).
    aprovado = minimo <= valor <= maximo
    # round(..., 4) evita lixo de float como 1.5999999999999979 (módulo 01).
    margem = round(min(valor - minimo, maximo - valor), 4)
    return aprovado, margem


class PedidoValidacao(BaseModel):
    """O que o cliente envia. Campos: linha, ensaio, valor (>= 0)."""

    linha: str
    ensaio: str
    valor: float = Field(ge=0)


class ResultadoValidacao(BaseModel):
    """O que a API devolve. Campos: linha, ensaio, valor, minimo, maximo, margem, aprovado."""

    linha: str
    ensaio: str
    valor: float
    minimo: float
    maximo: float
    margem: float
    aprovado: bool


app = FastAPI()


@app.post("/validar")
def validar(pedido: PedidoValidacao) -> ResultadoValidacao:
    # Um parâmetro do tipo BaseModel = o FastAPI lê o CORPO JSON da requisição.
    linha = pedido.linha.upper()
    ensaio = pedido.ensaio.strip().lower()

    # .get encadeado: {} quando a linha não existe, None quando o ensaio não existe.
    faixa = TOLERANCIAS.get(linha, {}).get(ensaio)
    if faixa is None:
        raise HTTPException(
            status_code=404, detail=f"Tolerância não cadastrada: linha {linha} / ensaio {ensaio}"
        )

    minimo, maximo = faixa
    aprovado, margem = avaliar(pedido.valor, minimo, maximo)
    return ResultadoValidacao(
        linha=linha,
        ensaio=ensaio,
        valor=pedido.valor,
        minimo=minimo,
        maximo=maximo,
        margem=margem,
        aprovado=aprovado,
    )
