"""
Exercício 13.07 — Ocorrências de qualidade: os códigos de status certos
Nível: ★★☆

Contexto: o laboratório registra ocorrências (não conformidades) por OP:
"bolhas no filme", "COF acima do especificado"... Cada operação da API deve
responder com o código de status que conta o que aconteceu: 201 criou,
404 não existe, 409 conflito com o estado atual, 204 apagou (sem corpo).

Tarefa: guarde as ocorrências no dicionário OCORRENCIAS ({id: dict}).
1. Complete OcorrenciaEntrada: op (6 dígitos), descricao (mínimo 5 caracteres)
   e gravidade ("baixa", "media" ou "alta").
2. Crie as rotas:
   - POST /ocorrencias -> 201. Guarda e devolve
     {"id": <novo>, "op": ..., "descricao": ..., "gravidade": ..., "status": "aberta"}.
     O novo id é o maior id existente + 1 (o primeiro é 1).
     Mesma op E mesma descricao de uma ocorrência já cadastrada -> 409 com
     detail "Ocorrência repetida".
   - GET /ocorrencias -> 200, lista de todas, em ordem de id. Parâmetro de
     consulta opcional `status` ("aberta" ou "encerrada") filtra a lista.
   - GET /ocorrencias/{id} -> 200 com a ocorrência, ou 404 com detail
     "Ocorrência não encontrada".
   - PATCH /ocorrencias/{id}/encerrar -> 200 com a ocorrência já com
     "status": "encerrada". Se já estava encerrada -> 409 com detail
     "Ocorrência já encerrada". Se não existe -> 404 (mesma mensagem acima).
   - DELETE /ocorrencias/{id} -> 204 sem corpo, ou 404.

Exemplos:
    >>> cliente.post("/ocorrencias", json={"op": "123456", "descricao": "Bolhas no filme",
    ...                                    "gravidade": "alta"}).status_code
    201
    >>> cliente.patch("/ocorrencias/1/encerrar").json()["status"]
    'encerrada'

Dica: @app.post("/ocorrencias", status_code=201); @app.patch(...);
@app.delete(..., status_code=204) com a função devolvendo None. Uma função
auxiliar buscar_ou_404(id) evita repetir o mesmo if em três rotas.

Teste com:  python curso.py testar 13 ex07
"""

from fastapi import FastAPI
from pydantic import BaseModel

OCORRENCIAS: dict[int, dict] = {}


class OcorrenciaEntrada(BaseModel):
    """O que o cliente envia. Campos: op, descricao, gravidade."""

    # Escreva seus campos aqui


app = FastAPI()

# Escreva suas rotas aqui
