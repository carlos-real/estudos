"""
Exercício 09.10 — Conserte o bug: códigos das bobinas
Nível: ★★☆

Contexto: cada bobina de uma OP recebe uma etiqueta "<op>-<número>", com o
número em 3 dígitos começando em 001. A OP 12345 com 3 bobinas gera
12345-001, 12345-002 e 12345-003. A produção reclamou: as etiquetas começam
em 000 e, às vezes, saem com espaços no meio.

Tarefa: a função abaixo tem 3 bugs. Encontre e corrija.
  1. Leia o código e preveja: o que gerar_codigos_bobinas("12345", 3) devolve
     hoje? E gerar_codigos_bobinas("12345", 0)? Anote antes de rodar.
  2. Rode os testes e corrija um bug por vez.

Regras (o comportamento CORRETO):
  - Devolve uma lista com `quantidade` códigos, numerados de 1 a quantidade,
    sempre com 3 dígitos (001, 002, ..., 120).
  - A OP pode vir com espaços em volta (" 4512 "): use a OP sem espaços.
  - quantidade menor que 1 levanta ValueError (não existe OP com 0 bobinas).

Exemplos (comportamento correto):
    >>> gerar_codigos_bobinas("12345", 3)
    ['12345-001', '12345-002', '12345-003']
    >>> gerar_codigos_bobinas(" 4512 ", 1)
    ['4512-001']

Dica: o clássico "erro por um" (off-by-one) mora no range. Teste no REPL:
list(range(3)) e list(range(1, 4)).

Teste com:  python curso.py testar 09 ex10
"""


def gerar_codigos_bobinas(op: str, quantidade: int) -> list[str]:
    """Gera os códigos '<op>-001', '<op>-002', ... das bobinas de uma OP."""
    codigos = []
    for numero in range(quantidade):
        codigos.append(f"{op}-{numero:03d}")
    return codigos
