"""
Exercício 04.13 — Revisão: pipeline de limpeza de códigos
Nível: ★★★

Contexto: Este exercício mistura o módulo 04 (funções como valores, *args,
closures) com o 01 (strip, upper, replace), o 02 (laços e decisões) e o 03
(conjunto para tirar repetidos). Os códigos de OP chegam sujos de vários
lugares: " op 4512", "OP-4512", "op-4513 ", "". Em vez de uma função cheia de
ifs, você vai montar uma LINHA DE MONTAGEM de funções pequenas.

Tarefa: implemente três funções.
1. `compor(*funcoes)` devolve UMA função nova que recebe um valor e aplica as
   funções em sequência, da esquerda para a direita:
   compor(f, g, h)(x) é o mesmo que h(g(f(x))).
   compor() sem funções devolve uma função que devolve o próprio valor.
2. `trocar_espacos_por_hifen(texto)` troca cada espaço por "-".
3. `limpar_codigos(codigos)`: monte, com compor, a limpeza
   strip -> upper -> trocar_espacos_por_hifen e aplique a cada código.
   Descarte os que ficarem vazios e tire os repetidos, mantendo a ordem da
   primeira aparição. Devolva a lista nova.

Exemplos:
    >>> def dobrar(x):
    ...     return x * 2
    >>> def somar_um(x):
    ...     return x + 1
    >>> compor(dobrar, somar_um)(3)
    7
    >>> compor(somar_um, dobrar)(3)
    8
    >>> compor()(5)
    5
    >>> limpar = compor(str.strip, str.upper)
    >>> limpar("  op-1 ")
    'OP-1'
    >>> limpar_codigos([" op 4512", "OP-4512", "", "op-4513 "])
    ['OP-4512', 'OP-4513']

Dica: str.strip é a própria função do método: str.strip("  a ") devolve "a".
Dentro de compor, defina uma função que percorre `funcoes` aplicando uma de
cada vez (um acumulador, como no módulo 02) e devolva essa função.

Teste com:  python curso.py testar 04 ex13
"""

from collections.abc import Callable


def compor(*funcoes: Callable) -> Callable:
    """Devolve uma função que aplica as funções da esquerda para a direita."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def trocar_espacos_por_hifen(texto: str) -> str:
    """Troca cada espaço por hífen."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def limpar_codigos(codigos: list[str]) -> list[str]:
    """Limpa os códigos (strip, upper, espaço -> hífen), sem vazios nem repetidos."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
