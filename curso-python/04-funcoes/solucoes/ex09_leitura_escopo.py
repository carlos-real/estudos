"""
Solução — Exercício 04.09 — Leitura de código: escopo, padrão mutável e print × return
"""


def previsao_a() -> list[str]:
    """Linhas que o Trecho A mostra na tela, em ordem (ex.: ["1", "2"])."""
    # dobro MOSTRA 10, mas não tem return: devolve None. Então "resultado"
    # vale None, e o segundo print mostra None.
    return ["10", "None"]


def previsao_b() -> int:
    """O que o último print do Trecho B mostra."""
    # O "total = ..." DENTRO da função cria uma variável LOCAL com o mesmo nome.
    # A global continua 0. (E o retorno de somar(10) foi jogado fora.)
    return 0


def previsao_c() -> list[str]:
    """O que o print do Trecho C mostra."""
    # A lista padrão é criada UMA vez, no def. As três chamadas sem lista
    # acrescentam na mesma lista.
    return ["bolha", "risco", "gel"]


def previsao_d() -> tuple[list[int], list[int]]:
    """Os valores de a e b no print do Trecho D, como tupla (a, b)."""
    # zerar: "valores = []" só move a etiqueta LOCAL para uma lista nova;
    # a lista de "a" não é tocada.
    # limpar: valores.clear() mexe no OBJETO recebido, que é o mesmo de "b".
    return [1, 2], []


def resumo_lote(
    medicoes: list[float], minimo: float, maximo: float
) -> tuple[list[float], float]:
    """Devolve (valores fora da faixa, percentual fora com 1 casa)."""
    # Defeito 1: padrão mutável (fora=[]) acumulava entre chamadas.
    #            Agora a lista é criada aqui dentro, a cada chamada.
    # Defeito 2: print em vez de return. Quem chamava não recebia nada.
    # Defeito 3: divisão por zero com lista vazia. Retorno antecipado resolve.
    if not medicoes:
        return [], 0.0

    fora = [valor for valor in medicoes if valor < minimo or valor > maximo]
    pct = round(len(fora) / len(medicoes) * 100, 1)
    return fora, pct
