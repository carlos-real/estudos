"""
Exercício 13.09 — Dependências: chave de acesso, perfil e regras injetadas
Nível: ★★☆

Contexto: a API de regras vai ser usada por dois públicos: o laboratório
(pode ler e alterar regras) e o pessoal do BI (só lê). Cada um recebe uma
chave, enviada no cabeçalho X-Chave. Verificar a chave em toda rota seria
repetição; com Depends, a verificação vira uma peça reaproveitável.

Tarefa:
1. perfil_atual(x_chave): devolve o perfil da chave em CHAVES ("escrita" ou
   "leitura"). Chave ausente ou desconhecida -> HTTPException 401 com detail
   "Chave de acesso inválida ou ausente". (A assinatura já está pronta: o
   Header() faz o FastAPI ler o cabeçalho X-Chave.)
2. obter_regras(): devolve o dicionário REGRAS.
3. Complete o modelo Faixa: minimo (float) e maximo (float).
4. Rotas, usando Depends(perfil_atual) e Depends(obter_regras):
   - GET /regras/{linha}: qualquer chave válida. Devolve
     {"linha": linha, "regras": <dict de ensaios da linha>}, ou 404 com detail
     "Linha X sem regras".
   - PUT /regras/{linha}/{ensaio}: corpo Faixa. Só perfil "escrita"; perfil
     "leitura" -> 403 com detail "Sem permissão de escrita". Grava
     [minimo, maximo] no dicionário de regras (crie a linha se não existir) e
     devolve {"linha": ..., "ensaio": ..., "minimo": ..., "maximo": ...}.
   Use SEMPRE o dicionário recebido de obter_regras (não REGRAS direto): os
   testes trocam essa dependência com app.dependency_overrides.

Exemplos:
    >>> cliente.get("/regras/A", headers={"X-Chave": "bi-789"}).json()
    {'linha': 'A', 'regras': {'espessura': [18.0, 22.0], 'cof': [0.2, 0.3]}}
    >>> cliente.get("/regras/A").status_code
    401

Dica: from fastapi import Depends, HTTPException.
def rota(perfil: Annotated[str, Depends(perfil_atual)], ...). 401 = "não sei
quem você é"; 403 = "sei quem você é, mas você não pode".

Teste com:  python curso.py testar 13 ex09
"""

from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

CHAVES = {"lab-123": "escrita", "bi-789": "leitura"}

REGRAS = {
    "A": {"espessura": [18.0, 22.0], "cof": [0.2, 0.3]},
    "B": {"espessura": [38.0, 42.0]},
}


def perfil_atual(x_chave: Annotated[str | None, Header()] = None) -> str:
    """Perfil ("escrita" ou "leitura") da chave enviada no cabeçalho X-Chave."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def obter_regras() -> dict:
    """Fonte das regras (nos testes, é trocada por outra)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


class Faixa(BaseModel):
    """Corpo do PUT. Campos: minimo, maximo."""

    # Escreva seus campos aqui


app = FastAPI()

# Escreva suas rotas aqui
