"""
Exercício 01.10 — Faixa de tolerância
Nível: ★★☆

Contexto: A especificação de um filme diz "espessura 25 µm ± 10%". Antes de aprovar
ou reprovar qualquer coisa, o sistema precisa saber os limites: o mínimo e o máximo
aceitos.

Tarefa:
1. `limite_minimo(nominal, tolerancia_pct)` devolve nominal - tolerancia_pct% do nominal.
2. `limite_maximo(nominal, tolerancia_pct)` devolve nominal + tolerancia_pct% do nominal.
3. `descrever_faixa(nominal, tolerancia_pct, unidade)` devolve o texto
   "<mínimo> a <máximo> <unidade>", com os limites em 2 casas decimais.
Não arredonde os limites nas funções 1 e 2 (só o texto da função 3 é formatado).

Exemplos:
    >>> limite_minimo(25, 10)
    22.5
    >>> descrever_faixa(25, 10, "µm")
    '22.50 a 27.50 µm'

Dica: 10% de 25 é 25 * 10 / 100.

Teste com:  python curso.py testar 01 ex10
"""


def limite_minimo(nominal: float, tolerancia_pct: float) -> float:
    """Devolve o limite mínimo da faixa de tolerância."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def limite_maximo(nominal: float, tolerancia_pct: float) -> float:
    """Devolve o limite máximo da faixa de tolerância."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def descrever_faixa(nominal: float, tolerancia_pct: float, unidade: str) -> str:
    """Devolve a faixa no formato '<mín> a <máx> <unidade>'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
