"""
Exercício 05.03 — Separar rótulo e valor
Nível: ★☆☆

Contexto: Os laudos exportados em texto têm uma informação por linha, no formato
"rótulo: valor". O valor às vezes tem ":" dentro (um horário, por exemplo).

Tarefa: implemente `separar_campo(linha)`, que devolve uma tupla
(rótulo, valor):
- divida no PRIMEIRO ":" da linha;
- tire os espaços das pontas do rótulo e do valor;
- se a linha não tiver ":", devolva (linha sem espaços nas pontas, "").

Exemplos:
    >>> separar_campo("Espessura (µm): 25,0")
    ('Espessura (µm)', '25,0')
    >>> separar_campo("  Horário da coleta :  14:30 ")
    ('Horário da coleta', '14:30')
    >>> separar_campo("Observações gerais")
    ('Observações gerais', '')

Dica: `partition` foi feito para isso.

Teste com:  python curso.py testar 05 ex03
"""


def separar_campo(linha: str) -> tuple[str, str]:
    """Divide "rótulo: valor" no primeiro ":" e devolve (rótulo, valor)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
