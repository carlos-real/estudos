"""
Exercício 02.08 — Média das medições válidas
Nível: ★★☆

Contexto: O micrômetro digital às vezes "pisca" e registra 0 ou um valor negativo.
Esses valores são falhas de leitura e não podem entrar na média, senão puxam o
resultado para baixo e reprovam um lote bom.

Tarefa:
1. `media_valida(valores)` recebe uma lista de medições e devolve a média só dos
   valores maiores que zero, arredondada com round() para 2 casas.
   - Use continue para pular os valores inválidos.
   - Se não houver nenhum valor válido (ou a lista estiver vazia), devolva None.
2. `contar_invalidas(valores)` devolve quantos valores são menores ou iguais a zero.
Não use sum(), len() de listas filtradas nem compreensões: o objetivo é praticar
acumuladores e contadores.

Exemplos:
    >>> media_valida([24.8, 25.1, 25.3])
    25.07
    >>> media_valida([25.0, 0, -1, 25.4])
    25.2
    >>> print(media_valida([0, 0]))
    None
    >>> contar_invalidas([25.0, 0, -1, 25.4])
    2

Dica: você vai precisar de dois acumuladores: a soma e a quantidade de válidos.

Teste com:  python curso.py testar 02 ex08
"""


def media_valida(valores: list[float]) -> float | None:
    """Devolve a média (2 casas) dos valores maiores que zero, ou None."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def contar_invalidas(valores: list[float]) -> int:
    """Devolve quantos valores são menores ou iguais a zero."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
