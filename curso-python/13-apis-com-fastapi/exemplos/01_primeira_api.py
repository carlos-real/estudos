"""Exemplo 01 — A primeira API com FastAPI.

Rode de dois jeitos:
    python exemplos/01_primeira_api.py            # demonstração, sem subir servidor
    python exemplos/01_primeira_api.py --servir   # servidor em http://127.0.0.1:8000

Ou, de dentro da pasta exemplos, com recarga automática ao salvar o arquivo:
    uvicorn 01_primeira_api:app --reload

Com o servidor no ar, abra http://127.0.0.1:8000/docs no navegador.
"""

import sys

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(title="API do Laboratório", version="0.1.0")


@app.get("/")
def raiz() -> dict:
    return {"mensagem": "API do laboratório no ar"}


@app.get("/saude")
def saude() -> dict:
    """Rota usada por monitoramento: responde rápido se a API está viva."""
    return {"status": "ok"}


def demonstrar() -> None:
    cliente = TestClient(app)  # um "navegador de mentira" que conversa com o app

    for metodo, caminho in [("GET", "/"), ("GET", "/saude"), ("GET", "/nada"), ("POST", "/")]:
        resposta = cliente.request(metodo, caminho)
        print(f"{metodo:<4} {caminho:<7} -> {resposta.status_code} {resposta.json()}")

    esquema = cliente.get("/openapi.json").json()
    print("Título na documentação:", esquema["info"]["title"], esquema["info"]["version"])
    print("Rotas documentadas:", list(esquema["paths"]))


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
