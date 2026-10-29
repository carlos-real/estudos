"""
Exercício 13.03 — Linhas de produção e o erro 404
Nível: ★☆☆

Contexto: a API do laboratório precisa informar os dados de cada linha de
produção. Pedir uma linha que não existe não é "erro do servidor": é um 404,
com uma mensagem clara para quem chamou.

Tarefa: usando o dicionário LINHAS, crie no `app`:
- GET "/linhas"           devolve a lista de códigos em ordem: ["A", "B", "C", "D"]
- GET "/linhas/{codigo}"  devolve {"codigo": <código>, "nome": ..., "produto": ...}
  - aceite minúsculas: /linhas/b mostra a linha B (com "codigo": "B");
  - se a linha não existir, levante HTTPException com status 404 e
    detail "Linha X não encontrada" (X em maiúscula).

Exemplos:
    >>> cliente.get("/linhas/b").json()
    {'codigo': 'B', 'nome': 'Extrusora B', 'produto': 'Filme PE 40 µm'}
    >>> cliente.get("/linhas/z").json()
    {'detail': 'Linha Z não encontrada'}

Dica: from fastapi import HTTPException;
raise HTTPException(status_code=404, detail="...").

Teste com:  python curso.py testar 13 ex03
"""

from fastapi import FastAPI

LINHAS = {
    "A": {"nome": "Extrusora A", "produto": "Filme PP 20 µm"},
    "B": {"nome": "Extrusora B", "produto": "Filme PE 40 µm"},
    "C": {"nome": "Laminadora C", "produto": "Laminado PET/PE"},
    "D": {"nome": "Extrusora D", "produto": "Filme PE 60 µm"},
}

app = FastAPI()

# Escreva suas rotas aqui
