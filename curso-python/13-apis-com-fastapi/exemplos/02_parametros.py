"""Exemplo 02 — Parâmetros de caminho e de consulta (com validação automática).

Rode com:
    python exemplos/02_parametros.py             # demonstração
    python exemplos/02_parametros.py --servir    # e abra http://127.0.0.1:8000/docs
"""

import sys
from enum import Enum
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI(title="Parâmetros")


class Linha(str, Enum):
    """Só estes valores são aceitos no caminho. O /docs mostra uma lista de escolha."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"


TOLERANCIAS = {
    "A": {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]},
    "B": {"espessura": [38.0, 42.0], "gramatura": [36.5, 39.5]},
    "C": {"tracao": [25.0, 40.0]},
    "D": {"selagem": [1.5, 3.0]},
}

BOBINAS = [
    {"numero": 1, "op": "123456", "linha": "A", "peso_kg": 412.5},
    {"numero": 2, "op": "123456", "linha": "A", "peso_kg": 398.0},
    {"numero": 3, "op": "123789", "linha": "B", "peso_kg": 640.0},
    {"numero": 4, "op": "124001", "linha": "C", "peso_kg": 1210.0},
    {"numero": 5, "op": "124001", "linha": "C", "peso_kg": 1100.0},
]


@app.get("/linhas/{linha}/tolerancias")
def tolerancias_da_linha(linha: Linha) -> dict:
    # linha chega como Linha.A, Linha.B...; .value é o texto "A", "B"...
    return {"linha": linha.value, "tolerancias": TOLERANCIAS[linha.value]}


@app.get("/bobinas/{numero}")
def ver_bobina(numero: int) -> dict:
    # numero chega como int: o FastAPI converte "3" -> 3 (ou responde 422)
    for bobina in BOBINAS:
        if bobina["numero"] == numero:
            return bobina
    return {"aviso": f"bobina {numero} não existe (no exemplo 04 isso vira um 404)"}


@app.get("/bobinas")
def listar_bobinas(
    linha: Linha | None = None,  # opcional: sem valor padrão obrigatório
    peso_min: Annotated[float, Query(ge=0)] = 0,  # ge = maior ou igual
    limite: Annotated[int, Query(ge=1, le=100)] = 10,  # entre 1 e 100
) -> list[dict]:
    resultado = [
        b
        for b in BOBINAS
        if (linha is None or b["linha"] == linha.value) and b["peso_kg"] >= peso_min
    ]
    return resultado[:limite]


def demonstrar() -> None:
    cliente = TestClient(app)
    pedidos = [
        "/linhas/B/tolerancias",
        "/linhas/E/tolerancias",
        "/bobinas/3",
        "/bobinas/tres",
        "/bobinas?linha=C",
        "/bobinas?peso_min=500&limite=2",
        "/bobinas?limite=0",
    ]
    for caminho in pedidos:
        resposta = cliente.get(caminho)
        print(f"GET {caminho}\n    {resposta.status_code} {resposta.json()}")


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
