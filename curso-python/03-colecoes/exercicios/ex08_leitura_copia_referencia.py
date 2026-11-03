"""
Exercício 03.08 — Leitura de código: cópia ou referência?
Nível: ★★☆

Contexto: Um colega escreveu um script de correção de medições e jura que "o
Python mudou a lista sozinho". Antes de culpar o Python, leia o código.

Parte 1 — Preveja. Para cada trecho, faça a função correspondente devolver o
valor que o print mostraria. Preveja no papel PRIMEIRO; depois rode no REPL para
conferir. Se errou, descubra o porquê (seção 4 da aula).

    # Trecho A
    a = [50.2, 49.8]
    b = a
    b.append(51.0)
    print(a)

    # Trecho B
    original = [50.2, 49.8]
    copia = original.copy()
    copia[0] = 99.9
    print(original)

    # Trecho C
    linhas = {"A": [50.2], "B": [20.1]}
    backup = linhas.copy()
    backup["A"].append(49.9)
    print(linhas["A"])

    # Trecho D
    valores = [10, 55, 60, 20]
    for v in valores:
        if v > 50:
            valores.remove(v)
    print(valores)

Parte 2 — Conserte. A função abaixo deveria devolver as medições corrigidas
(cada uma menos o offset do aparelho, arredondada em 2 casas) SEM alterar a
lista original. Mas ela altera:

    def corrigir_offset(medicoes, offset):
        for i in range(len(medicoes)):
            medicoes[i] = round(medicoes[i] - offset, 2)
        return medicoes

Escreva `corrigir_offset` corrigida: mesma resposta, lista original intacta.

Exemplos:
    >>> medicoes = [50.4, 49.9]
    >>> corrigir_offset(medicoes, 0.2)
    [50.2, 49.7]
    >>> medicoes
    [50.4, 49.9]

Dica: para a Parte 1, desenhe as etiquetas e as caixas como nos diagramas da
aula. Para a Parte 2, monte uma lista NOVA em vez de escrever na recebida.

Teste com:  python curso.py testar 03 ex08
"""


def previsao_a() -> list[float]:
    """Devolva o que o Trecho A imprime (ex.: return [1.0, 2.0])."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_b() -> list[float]:
    """Devolva o que o Trecho B imprime."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_c() -> list[float]:
    """Devolva o que o Trecho C imprime."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_d() -> list[int]:
    """Devolva o que o Trecho D imprime."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def corrigir_offset(medicoes: list[float], offset: float) -> list[float]:
    """Devolve uma lista NOVA com cada medição menos o offset (2 casas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
