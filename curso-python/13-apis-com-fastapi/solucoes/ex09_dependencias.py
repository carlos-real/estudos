"""
Exercício 13.09 — Dependências: chave de acesso, perfil e regras injetadas (SOLUÇÃO)
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

CHAVES = {"lab-123": "escrita", "bi-789": "leitura"}

REGRAS = {
    "A": {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]},
    "B": {"espessura": [38.0, 42.0]},
}


def perfil_atual(x_chave: Annotated[str | None, Header()] = None) -> str:
    """Perfil ("escrita" ou "leitura") da chave enviada no cabeçalho X-Chave."""
    # O FastAPI transforma o nome x_chave no cabeçalho "x-chave" (cabeçalhos
    # não diferenciam maiúsculas, então "X-Chave" também serve).
    if x_chave not in CHAVES:
        raise HTTPException(status_code=401, detail="Chave de acesso inválida ou ausente")
    return CHAVES[x_chave]


def obter_regras() -> dict:
    """Fonte das regras (nos testes, é trocada por outra)."""
    return REGRAS


class Faixa(BaseModel):
    """Corpo do PUT. Campos: minimo, maximo."""

    minimo: float
    maximo: float


# Apelidos: a assinatura das rotas fica curta e o significado, claro.
Perfil = Annotated[str, Depends(perfil_atual)]
Regras = Annotated[dict, Depends(obter_regras)]

app = FastAPI()


@app.get("/regras/{linha}")
def ver_regras(linha: str, perfil: Perfil, regras: Regras) -> dict:
    # `perfil` não é usado aqui dentro, mas declarar a dependência já obriga a
    # chave a ser válida: sem ela, perfil_atual levanta 401 antes da rota rodar.
    if linha not in regras:
        raise HTTPException(status_code=404, detail=f"Linha {linha} sem regras")
    return {"linha": linha, "regras": regras[linha]}


@app.put("/regras/{linha}/{ensaio}")
def gravar_regra(linha: str, ensaio: str, faixa: Faixa, perfil: Perfil, regras: Regras) -> dict:
    if perfil != "escrita":
        raise HTTPException(status_code=403, detail="Sem permissão de escrita")
    # setdefault: devolve regras[linha], criando {} antes se a linha não existir.
    regras.setdefault(linha, {})[ensaio] = [faixa.minimo, faixa.maximo]
    return {"linha": linha, "ensaio": ensaio, "minimo": faixa.minimo, "maximo": faixa.maximo}


# Alternativa: quando a rota não precisa do VALOR da dependência, só da
# verificação, dá para declarar no decorador:
#     @app.get("/regras/{linha}", dependencies=[Depends(perfil_atual)])
