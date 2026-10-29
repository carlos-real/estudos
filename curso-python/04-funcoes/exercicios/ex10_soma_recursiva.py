"""
Exercício 04.10 — Recursão: pesos aninhados
Nível: ★★☆

Contexto: Um carregamento é uma lista de paletes; cada palete é uma lista de
caixas ou de bobinas; uma caixa pode ter outras caixas dentro... Não dá para
saber quantos níveis existem. Esse é o tipo de estrutura em que a RECURSÃO
brilha.

    carga = [[100.0, 120.5], [80.0, [40.0, 40.0]], 10.0]

Aqui há dois paletes e uma bobina avulsa (10.0). O 2º palete tem uma bobina
de 80.0 e uma caixa com duas bobinas de 40.0.

Tarefa: implemente duas funções RECURSIVAS (que chamam a si mesmas).
1. `soma_aninhada(itens)` devolve a soma de todos os números, em qualquer
   profundidade.
2. `contar_valores(itens)` devolve quantos números existem, em qualquer
   profundidade (as listas em si não contam).
Listas vazias (em qualquer nível) somam 0 e têm 0 valores.

Exemplos:
    >>> carga = [[100.0, 120.5], [80.0, [40.0, 40.0]], 10.0]
    >>> soma_aninhada(carga)
    390.5
    >>> contar_valores(carga)
    6
    >>> soma_aninhada([[], [[]]])
    0

Dica: para cada item, pergunte isinstance(item, list). Se for lista, chame a
própria função para ela (caso recursivo). Se for número, use o número (caso
base).

Teste com:  python curso.py testar 04 ex10
"""


def soma_aninhada(itens: list) -> float:
    """Soma todos os números de uma lista que pode conter listas em qualquer nível."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def contar_valores(itens: list) -> int:
    """Conta os números de uma lista que pode conter listas em qualquer nível."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
