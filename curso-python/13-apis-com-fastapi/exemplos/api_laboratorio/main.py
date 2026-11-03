"""Ponto de entrada: cria o app e inclui os routers."""

from fastapi import FastAPI

from .rotas import medicoes, tolerancias

app = FastAPI(
    title="API do Laboratório de Qualidade",
    version="1.0.0",
    description="Consulta de tolerâncias e registro de medições das linhas A a D.",
)
app.include_router(tolerancias.router)
app.include_router(medicoes.router)


@app.get("/saude", tags=["infra"], summary="A API está no ar?")
def saude() -> dict:
    return {"status": "ok"}
