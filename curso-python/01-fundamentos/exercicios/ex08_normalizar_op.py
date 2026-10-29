"""
Exercício 01.08 — Normalizar o número da OP
Nível: ★★☆

Contexto: Cada pessoa escreve a ordem de produção (OP) de um jeito: " op-12345 ",
"OP 12.345", "Op: 12345" ou só "12345". Para cruzar a planilha com o e-mail da
expedição, o sistema precisa de um formato único: "OP12345".

Tarefa: implemente `normalizar_op(texto)`, que:
1. passa o texto para maiúsculas;
2. remove as letras "OP" e os caracteres "-", ".", ":" e espaços (em qualquer posição);
3. devolve "OP" seguido do que sobrou.

Exemplos:
    >>> normalizar_op(" op-12345 ")
    'OP12345'
    >>> normalizar_op("OP 12.345")
    'OP12345'
    >>> normalizar_op("12345")
    'OP12345'

Dica: replace() pode ser encadeado: texto.replace("a", "").replace("b", "").

Teste com:  python curso.py testar 01 ex08
"""


def normalizar_op(texto: str) -> str:
    """Devolve a OP no formato padrão 'OP' + número."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
