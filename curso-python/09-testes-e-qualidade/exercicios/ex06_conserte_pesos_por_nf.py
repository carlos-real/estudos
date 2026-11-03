"""
Exercício 09.06 — Conserte o bug: peso total por NF
Nível: ★★☆

Contexto: a expedição manda um e-mail por carregamento, com a NF e o peso. Uma
mesma NF pode sair em vários carregamentos (entrega parcial). O relatório
precisa do peso TOTAL de cada NF, mas os totais estão vindo menores do que o
real e algumas NFs aparecem duplicadas.

Tarefa: a função abaixo já está escrita e tem 2 bugs. Encontre e corrija.
  1. Leia o código e preveja: com os pedidos
       [{"nf": "1001", "peso": 250.0}, {"nf": "1001", "peso": 120.5}]
     o que a função devolve hoje? Anote seu palpite antes de rodar.
  2. Rode os testes. Corrija um bug de cada vez e rode de novo.

Regras (o comportamento CORRETO):
  - Recebe uma lista de dicionários com as chaves "nf" (texto) e "peso" (kg).
  - Devolve um dicionário {nf: peso_total}.
  - O número da NF pode vir com espaços em volta (" 1001 "): é a mesma NF que
    "1001", e a chave do resultado fica sem espaços.

Exemplo (comportamento correto):
    >>> somar_pesos_por_nf([
    ...     {"nf": "1001", "peso": 250.0},
    ...     {"nf": "1002", "peso": 80.0},
    ...     {"nf": " 1001", "peso": 120.5},
    ... ])
    {'1001': 370.5, '1002': 80.0}

Dica: para cada bug, escreva no papel o dicionário totais depois de cada
volta do for. Ou use breakpoint() dentro do laço e o comando "p totais".

Teste com:  python curso.py testar 09 ex06
"""


def somar_pesos_por_nf(pedidos: list[dict]) -> dict[str, float]:
    """Soma o peso (kg) de cada NF. Uma NF pode aparecer em vários pedidos."""
    totais = {}
    for pedido in pedidos:
        nf = pedido["nf"]
        totais[nf] = pedido["peso"]
    return totais
