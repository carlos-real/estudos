"""
Solução — Exercício 03.08 — Leitura de código: cópia ou referência?

Ideia central: atribuir (b = a) NÃO copia; cria outra etiqueta para o MESMO
objeto. E .copy() é uma cópia RASA: copia a "caixa de fora", não o que está
dentro dela.
"""


def previsao_a() -> list[float]:
    """Devolva o que o Trecho A imprime (ex.: return [1.0, 2.0])."""
    # b = a faz b apontar para a MESMA lista. O append por b aparece por a.
    #   a ──┐
    #       ├──> [50.2, 49.8, 51.0]
    #   b ──┘
    return [50.2, 49.8, 51.0]


def previsao_b() -> list[float]:
    """Devolva o que o Trecho B imprime."""
    # .copy() criou uma lista nova. Trocar copia[0] não afeta a original.
    return [50.2, 49.8]


def previsao_c() -> list[float]:
    """Devolva o que o Trecho C imprime."""
    # linhas.copy() é cópia RASA: o dicionário é novo, mas os VALORES (as
    # listas) são os mesmos objetos. backup["A"] e linhas["A"] são a mesma
    # lista, então o append aparece nos dois.
    #   linhas ──> {"A": ●, "B": ●}
    #                    │       └──> [20.1]
    #   backup ──> {"A": ●, "B": ●}   (os ● apontam para as MESMAS listas)
    #                    └──> [50.2, 49.9]
    # Para copiar "até o fundo": import copy; backup = copy.deepcopy(linhas)
    return [50.2, 49.9]


def previsao_d() -> list[int]:
    """Devolva o que o Trecho D imprime."""
    # Remover itens de uma lista enquanto o for passa por ela pula elementos:
    # - na posição 1 está 55 -> é removido; a lista vira [10, 60, 20];
    # - o for vai para a posição 2, que agora é 20. O 60 "escapou"!
    # Correção: monte uma lista nova: [v for v in valores if v <= 50]
    return [10, 60, 20]


def corrigir_offset(medicoes: list[float], offset: float) -> list[float]:
    """Devolve uma lista NOVA com cada medição menos o offset (2 casas)."""
    # O defeito original: medicoes[i] = ... escreve NA lista recebida, e quem
    # chamou a função perde os valores brutos. A correção é montar uma lista
    # nova; a recebida só é lida.
    return [round(valor - offset, 2) for valor in medicoes]

    # Versão com laço, também correta:
    #     corrigidas = []
    #     for valor in medicoes:
    #         corrigidas.append(round(valor - offset, 2))
    #     return corrigidas
