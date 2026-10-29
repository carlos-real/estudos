"""
Exercício 04.09 — Leitura de código: escopo, padrão mutável e print × return
Nível: ★★☆

Contexto: Antes de escrever funções, todo programador passa muito tempo LENDO
funções dos outros. Aqui você lê, prevê e conserta.

Parte 1 — Preveja. Faça cada função devolver a sua previsão. Preveja no papel
PRIMEIRO; depois rode no REPL para conferir (e entenda o porquê se errou).

    # Trecho A: o que aparece na tela, linha por linha?
    def dobro(x):
        print(x * 2)

    resultado = dobro(5)
    print(resultado)

    # Trecho B: o que o último print mostra?
    total = 0

    def somar(valor):
        total = valor + 1
        return total

    somar(10)
    print(total)

    # Trecho C: o que o print mostra?
    def registrar(item, lista=[]):
        lista.append(item)
        return lista

    registrar("bolha")
    registrar("risco")
    print(registrar("gel"))

    # Trecho D: o que o print mostra?
    def zerar(valores):
        valores = []
        return valores

    def limpar(valores):
        valores.clear()

    a = [1, 2]
    b = [3, 4]
    zerar(a)
    limpar(b)
    print(a, b)

Parte 2 — Conserte. Esta função tem TRÊS defeitos:

    def resumo_lote(medicoes, minimo, maximo, fora=[]):
        for valor in medicoes:
            if valor < minimo or valor > maximo:
                fora.append(valor)
        pct = len(fora) / len(medicoes) * 100
        print(f"{pct:.1f}% fora da faixa")

Reescreva `resumo_lote(medicoes, minimo, maximo)` como função PURA: devolve a
tupla (lista dos valores fora da faixa, percentual fora com round(..., 1)).
Lista vazia: ([], 0.0). Chamadas seguidas não podem interferir uma na outra.

Exemplos:
    >>> resumo_lote([50.2, 44.1, 56.3, 49.9], 45.0, 55.0)
    ([44.1, 56.3], 50.0)
    >>> resumo_lote([], 45.0, 55.0)
    ([], 0.0)

Dica: para a Parte 2, pergunte de cada linha: "isso depende de algo de fora da
função?" e "isso devolve o resultado ou só mostra?".

Teste com:  python curso.py testar 04 ex09
"""


def previsao_a() -> list[str]:
    """Linhas que o Trecho A mostra na tela, em ordem (ex.: ["1", "2"])."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_b() -> int:
    """O que o último print do Trecho B mostra."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_c() -> list[str]:
    """O que o print do Trecho C mostra."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_d() -> tuple[list[int], list[int]]:
    """Os valores de a e b no print do Trecho D, como tupla (a, b)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_lote(
    medicoes: list[float], minimo: float, maximo: float
) -> tuple[list[float], float]:
    """Devolve (valores fora da faixa, percentual fora com 1 casa)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
