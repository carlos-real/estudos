"""
Exercício 04.07 — Ordenar com key e lambda
Nível: ★★☆

Contexto: O parâmetro key= de sorted, min e max recebe uma função que diz O QUE
comparar. Com ela você responde perguntas como "qual medição está mais perto do
nominal?" sem escrever nenhum laço.

Tarefa: implemente três funções, cada uma com UMA chamada a min ou sorted.
1. `mais_proxima_do_nominal(medicoes, nominal)`: a medição com a menor
   distância até o nominal. Em empate, a que aparece primeiro.
   Lista vazia: None.
2. `ordenar_por_desvio(medicoes, nominal)`: lista NOVA, da medição mais
   próxima do nominal para a mais distante. Empates mantêm a ordem original.
3. `ordenar_palavras(palavras)`: lista nova ordenada pelo tamanho da palavra
   e, no empate, em ordem alfabética SEM diferenciar maiúsculas.

Exemplos:
    >>> mais_proxima_do_nominal([50.6, 49.8, 51.0], 50.0)
    49.8
    >>> ordenar_por_desvio([53.0, 50.5, 47.0, 49.0], 50.0)
    [50.5, 49.0, 53.0, 47.0]
    >>> ordenar_palavras(["Selagem", "cof", "tração", "Gel"])
    ['cof', 'Gel', 'tração', 'Selagem']

Dica: a key de ordenar_palavras devolve uma tupla: (tamanho, palavra em
minúsculas).

Teste com:  python curso.py testar 04 ex07
"""


def mais_proxima_do_nominal(medicoes: list[float], nominal: float) -> float | None:
    """Medição mais próxima do nominal (a primeira, em empate) ou None."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ordenar_por_desvio(medicoes: list[float], nominal: float) -> list[float]:
    """Nova lista, da medição mais próxima do nominal para a mais distante."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ordenar_palavras(palavras: list[str]) -> list[str]:
    """Nova lista por tamanho e, no empate, alfabética sem diferenciar maiúsculas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
