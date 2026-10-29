"""
Exercício 02.03 — Ano bissexto
Nível: ★☆☆

Contexto: Calendários, validade de laudos, prazos de garantia: todo sistema que mexe
com datas precisa saber se um ano tem 365 ou 366 dias.

Tarefa:
1. `eh_bissexto(ano)` devolve True se o ano for bissexto. A regra é:
   - divisível por 4 e NÃO divisível por 100; OU
   - divisível por 400.
   (2024 é bissexto; 1900 não é; 2000 é.)
2. `dias_no_ano(ano)` devolve 366 para anos bissextos e 365 para os demais.

Exemplos:
    >>> eh_bissexto(2024)
    True
    >>> eh_bissexto(1900)
    False
    >>> dias_no_ano(2000)
    366

Dica: "divisível por 4" é ano % 4 == 0. Monte a regra com and, or e not.

Teste com:  python curso.py testar 02 ex03
"""


def eh_bissexto(ano: int) -> bool:
    """Diz se o ano é bissexto."""
    # Traduzindo a regra ao pé da letra, com parênteses para deixar a intenção clara
    # (and já tem prioridade sobre or, mas quem lê agradece).
    divisivel_por_4 = ano % 4 == 0
    divisivel_por_100 = ano % 100 == 0
    divisivel_por_400 = ano % 400 == 0
    return (divisivel_por_4 and not divisivel_por_100) or divisivel_por_400


def dias_no_ano(ano: int) -> int:
    """Devolve quantos dias o ano tem (365 ou 366)."""
    return 366 if eh_bissexto(ano) else 365
