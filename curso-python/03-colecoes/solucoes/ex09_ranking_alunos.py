"""
Solução — Exercício 03.09 — Ranking da turma

Ideia central: sorted com key. A key recebe UM item e devolve "o que deve ser
comparado". Uma tupla compara o 1º elemento; se empatar, o 2º; e assim por diante.
"""


def ranking(notas: dict[str, float]) -> list[tuple[str, float]]:
    """Devolve (nome, nota) da maior para a menor nota; empate por nome."""
    # Cada item de notas.items() é uma tupla (nome, nota): par[0] é o nome e
    # par[1] é a nota. A key devolve (-nota, nome):
    # - "-nota" faz a MAIOR nota vir primeiro (9.0 vira -9.0, que é o menor);
    # - "nome" desempata em ordem alfabética crescente.
    return sorted(notas.items(), key=lambda par: (-par[1], par[0]))

    # Por que não reverse=True? Porque inverteria também o desempate,
    # e os nomes sairiam de Z para A.


def aprovados(notas: dict[str, float], media_minima: float) -> list[str]:
    """Devolve, em ordem alfabética, os nomes com nota >= media_minima."""
    # Compreensão filtra; sorted ordena o resultado (strings: ordem alfabética).
    return sorted(nome for nome, nota in notas.items() if nota >= media_minima)
