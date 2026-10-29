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


def resumir_sequencia(resultados: list[str]) -> list[tuple[str, int]]:
    """Compacta a lista em (valor, repetições seguidas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def maior_sequencia(resultados: list[str], alvo: str = "R") -> int:
    """Tamanho da maior sequência seguida de `alvo`."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_por_lote(bobinas: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Peso total de cada lote, em ordem de lote."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
