"""
Exercício 01.02 — Cabeçalho de laudo
Nível: ★☆☆

Contexto: Os laudos impressos pelo laboratório começam com um cabeçalho: uma linha de
sinais de igual, o título em MAIÚSCULAS e outra linha de sinais de igual.

Tarefa: implemente `imprimir_cabecalho(titulo, largura)`, que IMPRIME (com print) três
linhas:
    1. o caractere "=" repetido `largura` vezes;
    2. o título em maiúsculas;
    3. de novo o "=" repetido `largura` vezes.
A função não devolve nada (não precisa de return).

Exemplos:
    >>> imprimir_cabecalho("laudo de espessura", 20)
    ====================
    LAUDO DE ESPESSURA
    ====================

Dica: em Python, "ab" * 3 resulta em "ababab".

Teste com:  python curso.py testar 01 ex02
"""


def imprimir_cabecalho(titulo: str, largura: int) -> None:
    """Imprime o cabeçalho de três linhas do laudo."""
    # Multiplicar um texto por um inteiro repete o texto. Guardar numa variável evita
    # repetir a mesma conta duas vezes (e garante que as duas linhas são iguais).
    linha = "=" * largura
    print(linha)
    print(titulo.upper())  # upper() também funciona com acentos: "ção" vira "ÇÃO"
    print(linha)
    # Sem return: toda função sem return devolve None. É o esperado aqui, porque o
    # trabalho desta função é IMPRIMIR, não calcular um valor.
