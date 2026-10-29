"""Refatoração segura: mudar a estrutura do código SEM mudar o comportamento.

Antes de refatorar código antigo, congele o comportamento atual num teste
("teste de caracterização"). Depois refatore e confira que o resultado é o mesmo.
Rode:  python exemplos/06_refatoracao.py
"""

# ---------------------------------------------------------------- ANTES
# Funciona, mas: nomes de uma letra, código repetido, números mágicos de índice.


def proc(d, t):
    r = []
    for x in d:
        if x[1] == "esp":
            if x[2] >= t["esp"][0] and x[2] <= t["esp"][1]:
                r.append((x[0], "OK"))
            else:
                r.append((x[0], "FORA"))
        elif x[1] == "gram":
            if x[2] >= t["gram"][0] and x[2] <= t["gram"][1]:
                r.append((x[0], "OK"))
            else:
                r.append((x[0], "FORA"))
    return r


# ---------------------------------------------------------------- DEPOIS
# Mesmo comportamento, com nomes que contam a história e uma função pequena
# para a regra que se repetia.

Medicao = tuple[str, str, float]  # (op, ensaio, valor)
Limites = tuple[float, float]  # (mínimo, máximo)


def situacao(valor: float, limites: Limites) -> str:
    """'OK' se o valor está dentro dos limites (inclusive), senão 'FORA'."""
    minimo, maximo = limites
    return "OK" if minimo <= valor <= maximo else "FORA"


def conferir_medicoes(
    medicoes: list[Medicao], tolerancias: dict[str, Limites]
) -> list[tuple[str, str]]:
    """Devolve (op, situação) de cada medição cujo ensaio tem tolerância cadastrada.

    Ensaios sem tolerância são ignorados, como o código antigo fazia. Se isso é
    um bug, a correção vem num commit separado: refatorar não é corrigir.
    """
    return [
        (op, situacao(valor, tolerancias[ensaio]))
        for op, ensaio, valor in medicoes
        if ensaio in tolerancias
    ]


# ---------------------------------------------------------------- TESTE DE CARACTERIZAÇÃO
TOLERANCIAS = {"esp": (19.0, 21.0), "gram": (18.5, 19.5)}
MEDICOES = [
    ("101", "esp", 20.0),
    ("102", "esp", 21.0),  # borda
    ("103", "esp", 21.5),
    ("104", "gram", 18.4),
    ("105", "gram", 19.5),  # borda
    ("106", "cof", 0.3),  # ensaio sem tolerância: o antigo ignora
]

if __name__ == "__main__":
    antes = proc(MEDICOES, TOLERANCIAS)
    depois = conferir_medicoes(MEDICOES, TOLERANCIAS)
    print("Antes: ", antes)
    print("Depois:", depois)
    assert antes == depois, "a refatoração mudou o comportamento!"
    print("Mesmo resultado: refatoração segura.")
