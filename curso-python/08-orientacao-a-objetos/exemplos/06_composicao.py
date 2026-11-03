"""Composição: a linha TEM uma especificação (não É uma especificação).

Rode com:  python exemplos/06_composicao.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tolerancia:
    minimo: float
    maximo: float

    def aprova(self, valor: float) -> bool:
        return self.minimo <= valor <= self.maximo


class Especificacao:
    def __init__(self, titulo: str, tolerancias: dict[str, Tolerancia], texto: str = ""):
        self.titulo = titulo
        self.texto = texto
        self.tolerancias = dict(tolerancias)


class LinhaDeProducao:
    def __init__(self, nome: str, fixas: dict[str, Tolerancia], padrao: Especificacao):
        self.nome = nome
        self.fixas = dict(fixas)
        self.padrao = padrao  # a linha TEM uma especificação padrão
        self._por_op: dict[str, Especificacao] = {}  # e TEM as especificações das OPs

    def cadastrar(self, op: str, especificacao: Especificacao) -> None:
        self._por_op[op] = especificacao

    def especificacao_para(self, op: str) -> Especificacao:
        return self._por_op.get(op, self.padrao)

    def avaliar(self, op: str, medidas: dict[str, float]) -> dict[str, bool]:
        tolerancias = {**self.fixas, **self.especificacao_para(op).tolerancias}
        return {nome: tol.aprova(medidas[nome]) for nome, tol in tolerancias.items()}


padrao_b = Especificacao("Filme PE 25 µm", {"espessura": Tolerancia(22.5, 27.5)})
linha_b = LinhaDeProducao("B", {"cof": Tolerancia(0.10, 0.30)}, padrao_b)
linha_b.cadastrar(
    "OP245110",
    Especificacao(
        "Café Montanha",
        {"espessura": Tolerancia(24.0, 26.0), "cof": Tolerancia(0.10, 0.40)},
        "Espessura 25 ± 1 µm e COF até 0,40 (acordo com o cliente)",
    ),
)

medidas = {"espessura": 25.4, "cof": 0.33}
for op in ("OP245102", "OP245110"):
    espec = linha_b.especificacao_para(op)
    print(f"{op}: especificação '{espec.titulo}' -> {linha_b.avaliar(op, medidas)}")
