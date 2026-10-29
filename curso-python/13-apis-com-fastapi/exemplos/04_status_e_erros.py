"""Exemplo 04 — Códigos de status e HTTPException num cadastro de amostras.

Os dados ficam num dicionário em memória (somem quando o servidor reinicia).
No exemplo 06 eles passam para o SQLite.

Rode com:
    python exemplos/04_status_e_erros.py             # demonstração
    python exemplos/04_status_e_erros.py --servir
"""

import sys

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI(title="Amostras")


class AmostraEntrada(BaseModel):
    codigo: str = Field(min_length=3)
    op: str = Field(pattern=r"^\d{6}$")
    descricao: str = ""


class Amostra(AmostraEntrada):
    """Herança (módulo 08): tudo da entrada + o id gerado pelo servidor."""

    id: int


AMOSTRAS: dict[int, Amostra] = {}


def buscar_ou_404(id_amostra: int) -> Amostra:
    """Função auxiliar: evita repetir o mesmo if em várias rotas."""
    if id_amostra not in AMOSTRAS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Amostra {id_amostra} não existe")
    return AMOSTRAS[id_amostra]


@app.post("/amostras", status_code=status.HTTP_201_CREATED)
def criar_amostra(entrada: AmostraEntrada) -> Amostra:
    if any(a.codigo == entrada.codigo for a in AMOSTRAS.values()):
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail=f"Já existe amostra com código {entrada.codigo}"
        )
    novo_id = max(AMOSTRAS, default=0) + 1
    amostra = Amostra(id=novo_id, **entrada.model_dump())
    AMOSTRAS[novo_id] = amostra
    return amostra


@app.get("/amostras")
def listar_amostras() -> list[Amostra]:
    return list(AMOSTRAS.values())


@app.get("/amostras/{id_amostra}")
def ver_amostra(id_amostra: int) -> Amostra:
    return buscar_ou_404(id_amostra)


@app.delete("/amostras/{id_amostra}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_amostra(id_amostra: int) -> None:
    buscar_ou_404(id_amostra)
    del AMOSTRAS[id_amostra]


def demonstrar() -> None:
    cliente = TestClient(app)
    passos = [
        ("POST", "/amostras", {"codigo": "AM-001", "op": "123456", "descricao": "Bobina 3"}),
        ("POST", "/amostras", {"codigo": "AM-002", "op": "123789"}),
        ("POST", "/amostras", {"codigo": "AM-001", "op": "124001"}),
        ("GET", "/amostras/2", None),
        ("DELETE", "/amostras/2", None),
        ("DELETE", "/amostras/2", None),
        ("GET", "/amostras", None),
    ]
    for metodo, caminho, corpo in passos:
        resposta = cliente.request(metodo, caminho, json=corpo)
        conteudo = resposta.json() if resposta.content else "(sem corpo)"
        print(f"{metodo:<6} {caminho:<12} -> {resposta.status_code} {conteudo}")


if __name__ == "__main__":
    if "--servir" in sys.argv:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        demonstrar()
