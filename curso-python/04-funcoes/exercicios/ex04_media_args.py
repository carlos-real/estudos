"""
Exercício 04.04 — Média com quantos valores vierem
Nível: ★☆☆

Contexto: O analista quer chamar a média direto no REPL, sem montar lista:
media(50.2, 49.8, 51.0). E quer saber o maior desvio de um conjunto de
medições em relação ao nominal.

Tarefa: implemente duas funções com *args.
1. `media(*valores)` devolve a média dos valores recebidos.
   Sem nenhum valor, devolva None.
2. `maior_desvio(nominal, *medicoes)` devolve o maior desvio, em módulo, entre
   cada medição e o nominal, arredondado com round(..., 2).
   Sem medições, devolva 0.0.

Exemplos:
    >>> media(50.0, 52.0)
    51.0
    >>> print(media())
    None
    >>> medicoes = [49.2, 51.5, 50.1]
    >>> media(*medicoes)
    50.26666666666667
    >>> maior_desvio(50.0, 49.2, 51.5, 50.1)
    1.5

Dica: dentro da função, `valores` é uma tupla comum. E abs(x) dá o módulo.

Teste com:  python curso.py testar 04 ex04
"""


def media(*valores: float) -> float | None:
    """Média de todos os valores recebidos (None se não vier nenhum)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def maior_desvio(nominal: float, *medicoes: float) -> float:
    """Maior |medição − nominal|, com 2 casas (0.0 sem medições)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
