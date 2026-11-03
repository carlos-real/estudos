"""Exemplo 03 — Corpo da requisição com Pydantic: validação e modelo de resposta.

Rode com:
    python exemplos/03_corpo_pydantic.py             # demonstração
    python exemplos/03_corpo_pydantic.py --servir    # e teste o POST em /docs
"""

import sys
from typing import Literal

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, ValidationError, field_validator

app = FastAPI(title="Corpo com Pydantic")

FAIXAS = {
    ("A", "espessura"): (18.0, 22.0),
    ("A", "cof"): (0.2, 0.3),
    ("B", "espessura"): (38.0, 42.0),
}


class Medicao(BaseModel):
    """O que o cliente ENVIA. Cada campo diz o tipo e as regras."""

    op: str = Field(pattern=r"^\d{6}$", examples=["123456"])
    linha: Literal["A", "B", "C", "D"]
    ensaio: str = Field(min_length=2)
    valor: float = Field(gt=0)
    unidade: str = "µm"  # valor padrão: o campo vira opcional

    @field_validator("ensaio")
    @classmethod
    def padronizar_ensaio(cls, valor: str) -> str:
        # Roda DEPOIS da validação de tipo: aqui valor já é str.
        return valor.strip().lower()


class Resultado(BaseModel):
    """O que a API DEVOLVE. Campos fora deste modelo não saem na resposta."""

    op: str
    ensaio: str
    valor: float
    minimo: float
    maximo: float
    aprovado: bool


@app.post("/medicoes/avaliar")
def avaliar(medicao: Medicao) -> Resultado:
    minimo, maximo = FAIXAS.get((medicao.linha, medicao.ensaio), (0.0, float("inf")))
    return {
        **medicao.model_dump(include={"op", "ensaio", "valor"}),
        "minimo": minimo,
        "maximo": maximo,
        "aprovado": minimo <= medicao.valor <= maximo,
        "uso_interno": "este campo some: não está em Resultado",
    }


def demonstrar() -> None:
    print("1) O modelo funciona sozinho, sem API:")
    m = Medicao(op="123456", linha="A", ensaio="  Espessura ", valor="20.4")
    print("  ", repr(m))
    print("   model_dump():", m.model_dump())
    try:
        Medicao(op="12345", linha="E", ensaio="cof", valor=-1)
    except ValidationError as erro:
        print(f"   ValidationError com {erro.error_count()} erros:")
        for detalhe in erro.errors():
            print("    -", detalhe["loc"], detalhe["msg"])

    print("2) Pela API:")
    cliente = TestClient(app)
    corpo = {"op": "123456", "linha": "A", "ensaio": "COF", "valor": 0.31}
    resposta = cliente.post("/medicoes/avaliar", json=corpo)
    print("  ", resposta.status_code, resposta.json())

    resposta = cliente.post("/medicoes/avaliar", json={"op": "123456", "linha": "A"})
    print("  ", resposta.status_code, [erro["loc"] for erro in resposta.json()["detail"]])


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
