"""
Exercício 13.06 — Rota que valida uma medição contra a tolerância
Nível: ★★☆

Contexto: o operador mede a espessura na linha e quer saber na hora: passou?
E quanto falta para reprovar? A API recebe a medição no CORPO do POST
(JSON) e devolve o resultado.

Tarefa:
1. avaliar(valor, minimo, maximo) devolve (aprovado, margem):
   - aprovado: minimo <= valor <= maximo
   - margem: distância até o limite MAIS PRÓXIMO, ou seja
     min(valor - minimo, maximo - valor), arredondada com round(..., 4).
     Fica negativa quando o valor está fora.
2. Complete os modelos:
   - PedidoValidacao: linha (str), ensaio (str), valor (float, ge=0)
   - ResultadoValidacao: linha (str), ensaio (str), valor, minimo, maximo,
     margem (floats) e aprovado (bool)
3. Crie POST "/validar" que recebe um PedidoValidacao e devolve um
   ResultadoValidacao (use-o como tipo de retorno da função):
   - padronize linha para MAIÚSCULA e ensaio para minúscula sem espaços nas
     pontas antes de procurar em TOLERANCIAS;
   - se não houver tolerância, HTTPException 404 com detail
     "Tolerância não cadastrada: linha X / ensaio Y" (já padronizados).

Exemplos:
    >>> avaliar(20.4, 18.0, 22.0)
    (True, 1.6)
    >>> cliente.post("/validar", json={"linha": "a", "ensaio": " COF ", "valor": 0.31}).json()
    {'linha': 'A', 'ensaio': 'cof', 'valor': 0.31, 'minimo': 0.2, 'maximo': 0.3,
     'margem': -0.01, 'aprovado': False}

Dica: o tipo de retorno (-> ResultadoValidacao) vira o "modelo de resposta": o
FastAPI valida e documenta o que sai.

Teste com:  python curso.py testar 13 ex06
"""

from fastapi import FastAPI
from pydantic import BaseModel

TOLERANCIAS = {
    "A": {"espessura": (18.0, 22.0), "cof": (0.2, 0.3)},
    "B": {"espessura": (38.0, 42.0), "gramatura": (36.5, 39.5)},
    "C": {"tracao": (25.0, 40.0)},
}


def avaliar(valor: float, minimo: float, maximo: float) -> tuple[bool, float]:
    """(aprovado, margem até o limite mais próximo)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


class PedidoValidacao(BaseModel):
    """O que o cliente envia. Campos: linha, ensaio, valor (>= 0)."""

    # Escreva seus campos aqui


class ResultadoValidacao(BaseModel):
    """O que a API devolve. Campos: linha, ensaio, valor, minimo, maximo, margem, aprovado."""

    # Escreva seus campos aqui


app = FastAPI()

# Escreva sua rota POST /validar aqui
