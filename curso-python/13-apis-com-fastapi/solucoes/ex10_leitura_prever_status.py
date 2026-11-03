"""
Exercício 13.10 — Leitura de código: preveja as respostas da API do colega (SOLUÇÃO)

O raciocínio de cada previsão está nos comentários de prever_status().
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ----------------------------------------------------------------------------
# A API do colega (NÃO altere)
# ----------------------------------------------------------------------------
TOLERANCIAS = {
    "A": {"espessura": (18.0, 22.0), "cof": (0.2, 0.3)},
    "B": {"espessura": (38.0, 42.0)},
}

app = FastAPI()


class Medicao(BaseModel):
    ensaio: str
    valor: float = Field(gt=0)


@app.get("/tolerancias/{linha}")
def ver_tolerancias(linha: str):
    if linha not in TOLERANCIAS:
        raise HTTPException(status_code=404, detail="Linha não encontrada")
    return TOLERANCIAS[linha]


@app.post("/tolerancias/{linha}/validar")
def validar(linha: str, medicao: Medicao):
    minimo, maximo = TOLERANCIAS[linha][medicao.ensaio]
    return {"aprovado": minimo <= medicao.valor <= maximo}


@app.get("/bobinas")
def listar_bobinas(limite: int = 10):
    return [{"numero": n} for n in range(1, limite + 1)]


# ----------------------------------------------------------------------------
# Suas previsões
# ----------------------------------------------------------------------------
def prever_status() -> dict[str, int]:
    """Código de status previsto para cada requisição."""
    return {
        # Rota existe, "A" está no dicionário.
        "1: GET /tolerancias/A": 200,
        # O caminho casa com a rota, mas "a" != "A": o if levanta o 404 do colega.
        "2: GET /tolerancias/a": 404,
        # Não existe rota para "/tolerancias" sem a linha: 404 do próprio FastAPI.
        "3: GET /tolerancias": 404,
        # O caminho existe, mas só para GET: 405 Method Not Allowed.
        "4: DELETE /tolerancias/A": 405,
        # Field(gt=0): zero não é MAIOR que zero. Validação falha antes da função: 422.
        "5: POST /tolerancias/A/validar com {'ensaio': 'cof', 'valor': 0}": 422,
        # O Pydantic, no modo padrão, converte o texto "20" em 20.0. Passa: 200.
        "6: POST /tolerancias/A/validar com {'ensaio': 'espessura', 'valor': '20'}": 200,
        # A linha B não tem "cof": TOLERANCIAS["B"]["cof"] levanta KeyError, que
        # ninguém trata. Exceção não tratada numa rota = 500 Internal Server Error.
        # Conserto: buscar com .get() e levantar HTTPException(404) quando faltar.
        "7: POST /tolerancias/B/validar com {'ensaio': 'cof', 'valor': 0.25}": 500,
        # limite: int não aceita "abc": 422.
        "8: GET /bobinas?limite=abc": 422,
        # -1 É um int válido (não há ge=1). range(1, 0) é vazio: 200 com [].
        # Conserto: limite: Annotated[int, Query(ge=1, le=100)] = 10.
        "9: GET /bobinas?limite=-1": 200,
    }


def prever_json_tolerancias_a() -> dict:
    """O JSON (como dict) devolvido por GET /tolerancias/A."""
    # JSON não tem tuplas: (18.0, 22.0) vira a lista [18.0, 22.0].
    return {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]}
