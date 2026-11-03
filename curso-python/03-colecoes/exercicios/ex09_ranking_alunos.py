"""
Exercício 03.09 — Ranking da turma
Nível: ★★☆

Contexto: Um professor de curso técnico guarda as notas finais num dicionário
nome -> nota e quer publicar o ranking e a lista de aprovados.

Tarefa: implemente duas funções.
1. `ranking(notas)` devolve uma lista de tuplas (nome, nota):
   - da maior nota para a menor;
   - em caso de empate na nota, por nome em ordem alfabética.
2. `aprovados(notas, media_minima)` devolve a lista de nomes com nota maior ou
   igual à média mínima, em ordem alfabética.

Exemplos:
    >>> notas = {"Carla": 8.5, "Bruno": 9.0, "Ana": 8.5, "Davi": 4.0}
    >>> ranking(notas)
    [('Bruno', 9.0), ('Ana', 8.5), ('Carla', 8.5), ('Davi', 4.0)]
    >>> aprovados(notas, 6.0)
    ['Ana', 'Bruno', 'Carla']

Dica: notas.items() dá pares (nome, nota). sorted aceita key= com uma lambda que
devolve uma TUPLA de critérios. Para inverter só a nota, use o sinal de menos.

Teste com:  python curso.py testar 03 ex09
"""


def ranking(notas: dict[str, float]) -> list[tuple[str, float]]:
    """Devolve (nome, nota) da maior para a menor nota; empate por nome."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def aprovados(notas: dict[str, float], media_minima: float) -> list[str]:
    """Devolve, em ordem alfabética, os nomes com nota >= media_minima."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
