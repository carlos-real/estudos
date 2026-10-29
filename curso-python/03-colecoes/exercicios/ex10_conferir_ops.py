"""
Exercício 03.10 — OPs pedidas x OPs com resultado
Nível: ★★☆

Contexto: A expedição mandou por e-mail as OPs que vão sair hoje. A planilha do
laboratório tem as OPs que já têm resultado de ensaio. Antes de emitir os
certificados, você precisa cruzar as duas listas.

Tarefa: implemente `conferir_ops(ops_pedidas, ops_com_resultado)`, que devolve
um dicionário com três listas, cada uma SEM repetidos e em ordem alfabética:
- "prontas": OPs pedidas que têm resultado (podem ganhar certificado);
- "sem_resultado": OPs pedidas que ainda não têm resultado (cobrar o lab);
- "nao_pedidas": OPs com resultado que a expedição não pediu.

Exemplos:
    >>> conferir_ops(["OP-3", "OP-1", "OP-2", "OP-1"], ["OP-2", "OP-4", "OP-1"])
    {'prontas': ['OP-1', 'OP-2'], 'sem_resultado': ['OP-3'], 'nao_pedidas': ['OP-4']}

Dica: converta as listas em conjuntos e use as operações & (interseção) e
- (diferença). Conjuntos não têm ordem: ordene com sorted() no final.

Teste com:  python curso.py testar 03 ex10
"""


def conferir_ops(ops_pedidas: list[str], ops_com_resultado: list[str]) -> dict[str, list[str]]:
    """Cruza OPs pedidas com OPs que têm resultado (listas ordenadas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
