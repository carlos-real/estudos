"""
Exercício 02.12 — Três seguidas fora: pare a linha
Nível: ★★★

Contexto: Uma medição fora da faixa pode ser um ponto isolado. Mas várias medições
SEGUIDAS fora indicam que o processo saiu de controle, e a regra do laboratório manda
parar a linha. Você vai encontrar onde começa a primeira sequência problemática.

Tarefa: implemente `inicio_sequencia_fora(valores, minimo, maximo, tamanho)`, que
devolve a POSIÇÃO (contando a partir de 1) da medição que inicia a primeira sequência
de `tamanho` medições consecutivas fora da faixa [minimo, maximo].
- Os limites são inclusivos: valor igual a minimo ou maximo está DENTRO.
- Se não existir tal sequência (ou a lista estiver vazia), devolva 0.
- `tamanho` é sempre 1 ou mais.
- Sequências mais longas que `tamanho` contam (devolva o início delas).

Exemplos:
    >>> inicio_sequencia_fora([25, 22, 21, 20, 25], 23, 27, 3)
    2
    >>> inicio_sequencia_fora([22, 25, 21, 20, 25], 23, 27, 3)
    0
    >>> inicio_sequencia_fora([20, 20, 25, 20, 20, 20], 23, 27, 3)
    4

Dica: mantenha dois contadores: a posição atual (aumenta sempre) e quantas fora
SEGUIDAS você viu (aumenta quando está fora, volta a zero quando está dentro).
Quando o segundo chegar em `tamanho`, onde começou a sequência?

Teste com:  python curso.py testar 02 ex12
"""


def inicio_sequencia_fora(
    valores: list[float], minimo: float, maximo: float, tamanho: int
) -> int:
    """Devolve a posição (1, 2, ...) do início da 1ª sequência fora, ou 0."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
