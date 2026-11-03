"""
Exercício 13.07 — Ocorrências de qualidade: os códigos de status certos (SOLUÇÃO)
"""

from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

OCORRENCIAS: dict[int, dict] = {}


class OcorrenciaEntrada(BaseModel):
    """O que o cliente envia. Campos: op, descricao, gravidade."""

    op: str = Field(pattern=r"^\d{6}$")
    descricao: str = Field(min_length=5)
    gravidade: Literal["baixa", "media", "alta"]


app = FastAPI()


def buscar_ou_404(id_ocorrencia: int) -> dict:
    # Levantar HTTPException aqui dentro funciona: a exceção "sobe" pela rota
    # que chamou e o FastAPI transforma em resposta 404.
    if id_ocorrencia not in OCORRENCIAS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ocorrência não encontrada")
    return OCORRENCIAS[id_ocorrencia]


@app.post("/ocorrencias", status_code=status.HTTP_201_CREATED)
def criar_ocorrencia(entrada: OcorrenciaEntrada) -> dict:
    repetida = any(
        o["op"] == entrada.op and o["descricao"] == entrada.descricao
        for o in OCORRENCIAS.values()
    )
    if repetida:
        # 409 Conflict: o pedido é válido, mas conflita com o que já existe.
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Ocorrência repetida")
    novo_id = max(OCORRENCIAS, default=0) + 1  # default evita erro com dict vazio
    ocorrencia = {"id": novo_id, **entrada.model_dump(), "status": "aberta"}
    OCORRENCIAS[novo_id] = ocorrencia
    return ocorrencia


@app.get("/ocorrencias")
def listar_ocorrencias(status: Literal["aberta", "encerrada"] | None = None) -> list[dict]:
    # Atenção: aqui o parâmetro `status` esconde o módulo `status` do FastAPI
    # dentro desta função. Não usamos o módulo aqui, então tudo bem; em código
    # maior, prefira outro nome (ex.: situacao) para não confundir.
    todas = [OCORRENCIAS[i] for i in sorted(OCORRENCIAS)]
    if status is None:
        return todas
    return [o for o in todas if o["status"] == status]


@app.get("/ocorrencias/{id_ocorrencia}")
def ver_ocorrencia(id_ocorrencia: int) -> dict:
    return buscar_ou_404(id_ocorrencia)


@app.patch("/ocorrencias/{id_ocorrencia}/encerrar")
def encerrar_ocorrencia(id_ocorrencia: int) -> dict:
    ocorrencia = buscar_ou_404(id_ocorrencia)
    if ocorrencia["status"] == "encerrada":
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Ocorrência já encerrada")
    ocorrencia["status"] = "encerrada"  # o dict é o mesmo guardado em OCORRENCIAS
    return ocorrencia


@app.delete("/ocorrencias/{id_ocorrencia}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_ocorrencia(id_ocorrencia: int) -> None:
    buscar_ou_404(id_ocorrencia)
    del OCORRENCIAS[id_ocorrencia]
    # 204 = "deu certo e não tenho nada para mostrar": a função devolve None.
