"""
Exercício 12.03 — Buscar tolerâncias numa API (com sessão injetada)
Nível: ★★☆

Contexto: a TI publicou uma API interna com as tolerâncias de cada linha. Seu
código vai consultá-la, mas os testes não podem depender da rede. Por isso a
função RECEBE a sessão HTTP como parâmetro: no programa real você passa um
requests.Session(); nos testes, uma sessão falsa que só finge responder.

A API responde a  GET <base_url>/tolerancias?linha=A  com um JSON assim:
    {"linha": "A",
     "itens": [{"ensaio": "espessura", "minimo": 18.0, "maximo": 22.0},
               {"ensaio": "cof", "minimo": 0.2, "maximo": 0.3}]}

Tarefa: implemente buscar_tolerancias(sessao, base_url, linha, timeout=10).
- A linha aceita "a" ou "A"; converta para maiúscula. Se não for A, B, C ou D,
  levante ValueError ANTES de qualquer chamada à rede.
- Chame sessao.get(f"{base_url}/tolerancias", params={"linha": <linha>},
  timeout=timeout). Sempre passe timeout!
- Chame resposta.raise_for_status() (erros HTTP NÃO devem ser engolidos).
- Devolva um dicionário {ensaio: (minimo, maximo)} montado a partir de "itens".

Exemplos:
    >>> buscar_tolerancias(requests.Session(), "http://api.lab.local", "a")
    {'espessura': (18.0, 22.0), 'cof': (0.2, 0.3)}

Dica: resposta.json() já devolve dicionários e listas do Python.

Teste com:  python curso.py testar 12 ex03
"""

import requests


def buscar_tolerancias(
    sessao: requests.Session, base_url: str, linha: str, timeout: float = 10
) -> dict[str, tuple[float, float]]:
    """Consulta a API e devolve {ensaio: (mínimo, máximo)} da linha."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
