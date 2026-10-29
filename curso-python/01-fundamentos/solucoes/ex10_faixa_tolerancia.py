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
    # "X% do nominal" é nominal * X / 100. O mínimo é o nominal menos isso.
    return nominal - nominal * tolerancia_pct / 100
    # Alternativa equivalente: nominal * (1 - tolerancia_pct / 100). Por causa do
    # float, as duas podem diferir na 15ª casa (25 * 1.1 = 27.500000000000004).
    # Por isso os testes comparam com pytest.approx, e o texto usa :.2f.


def limite_maximo(nominal: float, tolerancia_pct: float) -> float:
    """Devolve o limite máximo da faixa de tolerância."""
    return nominal + nominal * tolerancia_pct / 100


def descrever_faixa(nominal: float, tolerancia_pct: float, unidade: str) -> str:
    """Devolve a faixa no formato '<mín> a <máx> <unidade>'."""
    # Reaproveitamos as duas funções acima: uma função pode chamar outra.
    # Assim, se a regra de cálculo mudar, muda num lugar só.
    minimo = limite_minimo(nominal, tolerancia_pct)
    maximo = limite_maximo(nominal, tolerancia_pct)
    return f"{minimo:.2f} a {maximo:.2f} {unidade}"
