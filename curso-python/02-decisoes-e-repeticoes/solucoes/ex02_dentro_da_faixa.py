"""
Exercício 02.02 — Dentro da faixa?
Nível: ★☆☆

Contexto: A pergunta mais feita no laboratório: "este resultado está dentro da
especificação?". Os limites são inclusivos: um valor exatamente igual ao mínimo ou ao
máximo está aprovado.

Tarefa:
1. `dentro_da_faixa(valor, minimo, maximo)` devolve True se minimo <= valor <= maximo,
   e False caso contrário.
2. `rotular(valor, minimo, maximo)` devolve "OK" se o valor estiver dentro da faixa e
   "FORA" se não estiver. Use uma expressão condicional (x if condição else y).

Exemplos:
    >>> dentro_da_faixa(25.4, 23.0, 27.0)
    True
    >>> dentro_da_faixa(27.0, 23.0, 27.0)
    True
    >>> rotular(22.9, 23.0, 27.0)
    'FORA'

Dica: Python aceita comparação encadeada, como na matemática: a <= b <= c.

Teste com:  python curso.py testar 02 ex02
"""


def dentro_da_faixa(valor: float, minimo: float, maximo: float) -> bool:
    """Diz se o valor está entre minimo e maximo (inclusive)."""
    # A comparação já É um bool: basta devolvê-la. Evite o "if cond: return True
    # else: return False", que diz a mesma coisa com quatro linhas.
    return minimo <= valor <= maximo
    # Equivalente sem encadear: return valor >= minimo and valor <= maximo


def rotular(valor: float, minimo: float, maximo: float) -> str:
    """Devolve 'OK' se o valor está na faixa, senão 'FORA'."""
    # Expressão condicional: <valor se verdadeiro> if <condição> else <valor se falso>.
    # Reaproveitamos a função de cima para não repetir a regra.
    return "OK" if dentro_da_faixa(valor, minimo, maximo) else "FORA"
