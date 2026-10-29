"""
Exercício 13.04 — Filtros com parâmetros de consulta (SOLUÇÃO)
"""

from typing import Annotated

from fastapi import FastAPI, Query

BOBINAS = [
    {"numero": 1, "op": "123456", "linha": "A", "peso_kg": 412.5, "status": "liberada"},
    {"numero": 2, "op": "123456", "linha": "A", "peso_kg": 398.0, "status": "liberada"},
    {"numero": 3, "op": "123456", "linha": "A", "peso_kg": 405.2, "status": "retida"},
    {"numero": 4, "op": "123789", "linha": "B", "peso_kg": 640.0, "status": "liberada"},
    {"numero": 5, "op": "123789", "linha": "B", "peso_kg": 655.5, "status": "liberada"},
    {"numero": 6, "op": "123789", "linha": "B", "peso_kg": 610.0, "status": "retida"},
    {"numero": 7, "op": "124001", "linha": "C", "peso_kg": 1210.0, "status": "liberada"},
    {"numero": 8, "op": "124001", "linha": "C", "peso_kg": 1100.0, "status": "retida"},
    {"numero": 9, "op": "124050", "linha": "D", "peso_kg": 820.0, "status": "liberada"},
    {"numero": 10, "op": "124050", "linha": "D", "peso_kg": 790.0, "status": "liberada"},
    {"numero": 11, "op": "124050", "linha": "D", "peso_kg": 805.0, "status": "liberada"},
    {"numero": 12, "op": "124050", "linha": "D", "peso_kg": 99.5, "status": "retida"},
]

app = FastAPI()


def passa_nos_filtros(bobina: dict, linha: str | None, status: str | None, peso_min: float) -> bool:
    """Função pequena e pura: a regra do filtro fica fácil de ler e de testar."""
    if linha is not None and bobina["linha"] != linha.upper():
        return False
    if status is not None and bobina["status"] != status:
        return False
    return bobina["peso_kg"] >= peso_min


@app.get("/bobinas")
def listar_bobinas(
    # Parâmetro que NÃO aparece no caminho vira parâmetro de consulta (?linha=...).
    # `str | None = None` o torna opcional.
    linha: str | None = None,
    status: str | None = None,
    # Annotated junta o tipo e as regras extras. O FastAPI valida e responde 422
    # sozinho; a sua função nem é chamada com um valor inválido.
    peso_min: Annotated[float, Query(ge=0)] = 0,
    limite: Annotated[int, Query(ge=1, le=50)] = 10,
) -> list[dict]:
    filtradas = [b for b in BOBINAS if passa_nos_filtros(b, linha, status, peso_min)]
    return filtradas[:limite]  # fatiar além do fim não dá erro (módulo 03)


# Estilo antigo, que você ainda vai encontrar em muitos projetos:
#     limite: int = Query(10, ge=1, le=50)
# Funciona igual; a documentação atual do FastAPI recomenda Annotated.
