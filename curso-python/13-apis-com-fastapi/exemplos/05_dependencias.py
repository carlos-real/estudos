"""Exemplo 05 — Dependências (Depends): chave de acesso e dados injetados.

Rode com:
    python exemplos/05_dependencias.py             # demonstração
    python exemplos/05_dependencias.py --servir

No /docs, clique em "Try it out": o campo x-chave aparece como cabeçalho.
"""

import sys
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient

app = FastAPI(title="Dependências")

# Na vida real as chaves ficam em variável de ambiente ou banco, nunca no código.
CHAVES = {"lab-123": "Ana (laboratório)", "exp-456": "Carla (expedição)"}

TOLERANCIAS = {"A": {"espessura": [18.0, 22.0]}, "B": {"espessura": [38.0, 42.0]}}


def usuario_atual(x_chave: Annotated[str | None, Header()] = None) -> str:
    """Lê o cabeçalho X-Chave (o FastAPI troca _ por -) e devolve o nome do usuário."""
    if x_chave not in CHAVES:
        raise HTTPException(status_code=401, detail="Chave de acesso inválida ou ausente")
    return CHAVES[x_chave]


def obter_tolerancias() -> dict:
    """Hoje devolve um dicionário; amanhã pode ler do banco. As rotas nem percebem."""
    return TOLERANCIAS


# Apelidos deixam as assinaturas curtas e legíveis.
Usuario = Annotated[str, Depends(usuario_atual)]
Tolerancias = Annotated[dict, Depends(obter_tolerancias)]


@app.get("/eu")
def quem_sou_eu(usuario: Usuario) -> dict:
    return {"usuario": usuario}


@app.get("/tolerancias/{linha}")
def ver_tolerancias(linha: str, usuario: Usuario, tolerancias: Tolerancias) -> dict:
    if linha not in tolerancias:
        raise HTTPException(status_code=404, detail=f"Linha {linha} não cadastrada")
    return {"linha": linha, "consultado_por": usuario, "tolerancias": tolerancias[linha]}


def demonstrar() -> None:
    cliente = TestClient(app)
    print("sem chave     ->", cliente.get("/eu").json())
    print("chave errada  ->", cliente.get("/eu", headers={"X-Chave": "xyz"}).status_code)
    print("chave certa   ->", cliente.get("/eu", headers={"X-Chave": "exp-456"}).json())
    resposta = cliente.get("/tolerancias/A", headers={"X-Chave": "lab-123"})
    print("tolerâncias A ->", resposta.json())

    # Nos testes, trocamos uma dependência por outra (sem mexer nas rotas):
    app.dependency_overrides[obter_tolerancias] = lambda: {"A": {"espessura": [19.0, 21.0]}}
    resposta = cliente.get("/tolerancias/A", headers={"X-Chave": "lab-123"})
    print("com override  ->", resposta.json()["tolerancias"])
    app.dependency_overrides.clear()  # sempre desfaça no fim


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
