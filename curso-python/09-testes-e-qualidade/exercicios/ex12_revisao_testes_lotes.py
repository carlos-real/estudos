"""
Exercício 09.12 — Revisão: escreva os testes de dividir_em_lotes
Nível: ★★★

Revisão: mistura listas, fatiamento e mutabilidade (módulo 03), funções como
valores (módulo 04) e exceções (módulo 06) com escrita de testes (este módulo).

Contexto: a expedição monta paletes com no máximo N bobinas. A função
dividir_em_lotes recebe a lista de bobinas e o tamanho do palete e devolve os
lotes. Ela vai rodar todos os dias no robô da expedição, então seus testes
precisam ser à prova de bala.

Tarefa: complete testar_dividir_em_lotes(dividir_em_lotes) com asserts que
confiram TODAS as regras abaixo.

Regras de dividir_em_lotes(itens, tamanho) — a especificação:
  - devolve uma lista de listas, na ordem original, cada uma com `tamanho`
    itens; o último lote pode ter menos (o que sobrou);
  - nunca devolve lote vazio; lista de itens vazia devolve [];
  - tamanho menor que 1 levanta ValueError;
  - NÃO modifica a lista recebida (quem chamou continua com a lista intacta).

Exemplos:
    >>> dividir_em_lotes(["B1", "B2", "B3", "B4", "B5"], 2)
    [['B1', 'B2'], ['B3', 'B4'], ['B5']]
    >>> dividir_em_lotes([1, 2, 3, 4], 2)
    [[1, 2], [3, 4]]
    >>> dividir_em_lotes([], 3)
    []

Como o curso corrige: chama sua função com a versão CORRETA (nada pode falhar)
e com 4 versões COM BUG (cada uma precisa ser reprovada por algum assert seu).

Dica: liste as regras e, para cada uma, escreva pelo menos um caso que a
quebraria se estivesse errada. A última regra é a mais esquecida: guarde uma
cópia da lista ANTES de chamar a função (lista.copy() ou list(lista)) e
compare DEPOIS. Para pytest.raises, escreva "import pytest" no topo.

Teste com:  python curso.py testar 09 ex12
"""

from collections.abc import Callable


def testar_dividir_em_lotes(dividir_em_lotes: Callable[[list, int], list[list]]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
