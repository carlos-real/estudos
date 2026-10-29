"""
Exercício 07.08 — Sequências de resultados com groupby
Nível: ★★☆

Contexto: Na carta de acompanhamento, cada bobina recebe "A" (aprovada) ou "R"
(reprovada), na ordem de produção. Uma sequência longa de "R" indica problema na
máquina. E, no fim do turno, você soma o peso das bobinas de cada lote.

Tarefa:
1. `resumir_sequencia(resultados)` compacta a lista em tuplas (valor, quantas vezes
   seguidas). ["A", "A", "R", "A"] → [("A", 2), ("R", 1), ("A", 1)].
2. `maior_sequencia(resultados, alvo="R")` devolve o tamanho da MAIOR sequência
   seguida do valor `alvo` (0 se ele não aparecer).
3. `peso_por_lote(bobinas)` recebe tuplas (lote, peso_kg) FORA de ordem e devolve uma
   lista de tuplas (lote, peso total com round(..., 2)), com os lotes em ordem
   alfabética e cada lote aparecendo UMA vez.

Use itertools.groupby nas três.

Exemplos:
    >>> resumir_sequencia(["A", "A", "R", "R", "R", "A"])
    [('A', 2), ('R', 3), ('A', 1)]
    >>> maior_sequencia(["R", "A", "R", "R", "A"])
    2
    >>> peso_por_lote([("L02", 150.0), ("L01", 120.5), ("L02", 149.5)])
    [('L01', 120.5), ('L02', 299.5)]

Dica: groupby só junta itens VIZINHOS. No item 3, ordene antes pela mesma chave.
O "grupo" é um iterador: para contar, use len(list(grupo)) ou sum(1 for _ in grupo).

Teste com:  python curso.py testar 07 ex08
"""

from itertools import groupby


def resumir_sequencia(resultados: list[str]) -> list[tuple[str, int]]:
    """Compacta a lista em (valor, repetições seguidas)."""
    # groupby sem key agrupa itens vizinhos iguais. O grupo só pode ser lido UMA vez.
    return [(valor, len(list(grupo))) for valor, grupo in groupby(resultados)]


def maior_sequencia(resultados: list[str], alvo: str = "R") -> int:
    """Tamanho da maior sequência seguida de `alvo`."""
    # Reaproveita o resumo e filtra só as sequências do alvo.
    tamanhos = [quantidade for valor, quantidade in resumir_sequencia(resultados) if valor == alvo]
    # max([]) dá erro; o parâmetro default resolve a lista vazia.
    return max(tamanhos, default=0)


def peso_por_lote(bobinas: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Peso total de cada lote, em ordem de lote."""

    def lote_da_bobina(bobina: tuple[str, float]) -> str:
        return bobina[0]

    # Sem ordenar, ("L02", "L01", "L02") viraria TRÊS grupos e o L02 apareceria duas vezes.
    ordenadas = sorted(bobinas, key=lote_da_bobina)
    resultado = []
    for lote, grupo in groupby(ordenadas, key=lote_da_bobina):
        total = sum(peso for _lote, peso in grupo)
        resultado.append((lote, round(total, 2)))
    return resultado
    # Alternativa sem groupby (também correta): defaultdict(float) + sorted(...items()).
