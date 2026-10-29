"""
Exercício 00.03 — Peso total da carga
Nível: ★☆☆

Contexto: A expedição vai carregar várias bobinas do mesmo filme, todas com o mesmo
peso. A nota fiscal (NF) precisa do peso total da carga, em kg.

Tarefa: implemente `peso_total(peso_bobina_kg, quantidade)`, que DEVOLVE o peso
total: o peso de uma bobina multiplicado pela quantidade de bobinas.
- Quantidade 0 dá peso total 0.
- Não arredonde: devolva o resultado da conta.

Exemplos:
    >>> peso_total(250.0, 4)
    1000.0
    >>> peso_total(312.5, 3)
    937.5
    >>> peso_total(180.0, 0)
    0.0

Dica: em Python, multiplicação é `*`. Experimente `312.5 * 3` no REPL antes.

Teste com:  python curso.py testar 00 ex03
"""


def peso_total(peso_bobina_kg: float, quantidade: int) -> float:
    """Devolve o peso total (kg) de `quantidade` bobinas de `peso_bobina_kg` cada."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
