"""
Exercício 13.08 — APIRouter e documentação automática
Nível: ★☆☆

Contexto: quando a API cresce, cada assunto ganha seu próprio arquivo com um
APIRouter (ensaios, medições, certificados...). O app principal só "pluga"
os routers. De quebra, prefixo, tags e resumos deixam o /docs organizado
para quem vai usar a API (a TI, o pessoal do BI, você daqui a 6 meses).

Tarefa (tudo neste arquivo, para simplificar):
1. Crie o app com título "API do Laboratório" e versão "1.0.0".
2. Crie `router = APIRouter(prefix="/ensaios", tags=["ensaios"])` com:
   - GET "/"         -> lista dos nomes de ENSAIOS em ordem alfabética,
                        com summary="Lista os ensaios"
   - GET "/{nome}"   -> {"nome": nome, "unidade": ..., "norma": ...},
                        com summary="Detalhes de um ensaio".
                        Nome inexistente -> 404 com detail "Ensaio X não cadastrado".
3. Inclua o router no app (app.include_router).

Exemplos:
    >>> cliente.get("/ensaios/cof").json()
    {'nome': 'cof', 'unidade': 'adimensional', 'norma': 'ASTM D1894'}
    >>> cliente.get("/openapi.json").json()["info"]["title"]
    'API do Laboratório'

Dica: from fastapi import APIRouter, HTTPException. Com o servidor no ar,
abra /docs e veja as rotas agrupadas pela tag "ensaios".

Teste com:  python curso.py testar 13 ex08
"""

from fastapi import FastAPI

ENSAIOS = {
    "espessura": {"unidade": "µm", "norma": "ASTM D6988"},
    "cof": {"unidade": "adimensional", "norma": "ASTM D1894"},
    "tracao": {"unidade": "MPa", "norma": "ASTM D882"},
    "selagem": {"unidade": "N/15 mm", "norma": "ASTM F88"},
}

app = FastAPI()  # configure o título e a versão

# Escreva o router e as rotas aqui (e não esqueça do include_router)
