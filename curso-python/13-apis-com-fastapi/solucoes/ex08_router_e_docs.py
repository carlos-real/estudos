"""
Exercício 13.08 — APIRouter e documentação automática (SOLUÇÃO)

Num projeto de verdade, o router ficaria em rotas/ensaios.py e o main.py faria
    from .rotas import ensaios
    app.include_router(ensaios.router)
Veja o exemplo 07 (pasta exemplos/api_laboratorio).
"""

from fastapi import APIRouter, FastAPI, HTTPException

ENSAIOS = {
    "espessura": {"unidade": "µm", "norma": "ASTM D6988"},
    "cof": {"unidade": "adimensional", "norma": "ASTM D1894"},
    "tracao": {"unidade": "MPa", "norma": "ASTM D882"},
    "selagem": {"unidade": "N/15 mm", "norma": "ASTM F88"},
}

app = FastAPI(title="API do Laboratório", version="1.0.0")

# prefix: todas as rotas do router começam com /ensaios.
# tags: agrupa as rotas no /docs.
router = APIRouter(prefix="/ensaios", tags=["ensaios"])


@router.get("/", summary="Lista os ensaios")
def listar_ensaios() -> list[str]:
    return sorted(ENSAIOS)


@router.get("/{nome}", summary="Detalhes de um ensaio")
def ver_ensaio(nome: str) -> dict:
    """A docstring da função vira a descrição da rota no /docs."""
    if nome not in ENSAIOS:
        raise HTTPException(status_code=404, detail=f"Ensaio {nome} não cadastrado")
    return {"nome": nome, **ENSAIOS[nome]}


# Sem esta linha, as rotas do router simplesmente não existem no app.
app.include_router(router)
