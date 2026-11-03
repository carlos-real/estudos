"""
Exercício 13.04 — Filtros com parâmetros de consulta
Nível: ★★☆

Contexto: a expedição quer listar bobinas com filtros: só da linha C, só as
liberadas, só acima de 500 kg... Filtros opcionais são parâmetros de consulta
(a parte depois do "?": /bobinas?linha=C&status=liberada).

Tarefa: usando a lista BOBINAS, crie GET "/bobinas" com estes parâmetros de
consulta, todos opcionais:
- linha: str ou None (padrão None). Compare sem diferenciar maiúsculas.
- status: str ou None (padrão None). Ex.: "liberada", "retida".
- peso_min: float, padrão 0, não pode ser negativo (ge=0).
- limite: int, padrão 10, entre 1 e 50 (ge=1, le=50).
Devolva as bobinas que passam em TODOS os filtros informados, na ordem
original da lista, cortando em `limite` itens. Valores fora das regras
(limite=0, peso_min=-1, limite=abc) devem dar 422.

Exemplos:
    >>> cliente.get("/bobinas", params={"linha": "c", "status": "liberada"}).json()
    [{'numero': 7, 'op': '124001', 'linha': 'C', 'peso_kg': 1210.0, 'status': 'liberada'}]
    >>> len(cliente.get("/bobinas").json())
    10

Dica: from typing import Annotated; from fastapi import Query;
limite: Annotated[int, Query(ge=1, le=50)] = 10

Teste com:  python curso.py testar 13 ex04
"""

from fastapi import FastAPI

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

# Escreva sua rota aqui
