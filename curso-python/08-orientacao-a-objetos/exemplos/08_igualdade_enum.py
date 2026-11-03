"""Igualdade (is, ==, __eq__, __hash__) e Enum.

Rode com:  python exemplos/08_igualdade_enum.py
"""

from enum import Enum


class OrdemProducao:
    def __init__(self, numero: str) -> None:
        self.numero = "".join(c for c in numero if c.isdigit())  # "OP-245101" -> "245101"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, OrdemProducao):
            return NotImplemented
        return self.numero == outro.numero

    def __hash__(self) -> int:
        return hash(self.numero)

    def __repr__(self) -> str:
        return f"OrdemProducao('OP{self.numero}')"


a = OrdemProducao("OP-245101")
b = OrdemProducao("op 245101")
print(a == b, a is b, a == "245101")
print("OPs diferentes no conjunto:", len({a, b, OrdemProducao("OP245102")}))


class Linha(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Situacao(Enum):
    LIBERADO = "liberado"
    REPROVADO = "reprovado"
    PENDENTE = "pendente"


s = Situacao("liberado")  # procura pelo VALOR
print(s, "|", s.name, "|", s.value, "|", s is Situacao.LIBERADO)
print("Linhas:", [linha.value for linha in Linha])
try:
    Linha("E")
except ValueError as erro:
    print("Erro:", erro)
