"""Herança, super() e polimorfismo com tipos de ensaio.

Rode com:  python exemplos/05_heranca_polimorfismo.py
"""

from abc import ABC, abstractmethod


class Ensaio(ABC):
    """Classe base ABSTRATA: não se cria um 'Ensaio' genérico."""

    def __init__(self, nome: str, valor: float, unidade: str = "") -> None:
        self.nome = nome
        self.valor = valor
        self.unidade = unidade

    @abstractmethod
    def aprovado(self) -> bool:
        """Cada filha é obrigada a implementar."""

    def laudo(self) -> str:
        situacao = "APROVADO" if self.aprovado() else "REPROVADO"
        return f"{self.nome:<10} {self.valor:>7.2f} {self.unidade:<5} {situacao}"


class EnsaioFaixa(Ensaio):
    def __init__(self, nome, valor, minimo, maximo, unidade=""):
        super().__init__(nome, valor, unidade)
        self.minimo, self.maximo = minimo, maximo

    def aprovado(self) -> bool:
        return self.minimo <= self.valor <= self.maximo


class EnsaioMinimo(Ensaio):
    def __init__(self, nome, valor, minimo, unidade=""):
        super().__init__(nome, valor, unidade)
        self.minimo = minimo

    def aprovado(self) -> bool:
        return self.valor >= self.minimo


class EnsaioMaximo(Ensaio):
    def __init__(self, nome, valor, maximo, unidade=""):
        super().__init__(nome, valor, unidade)
        self.maximo = maximo

    def aprovado(self) -> bool:
        return self.valor <= self.maximo


ensaios = [
    EnsaioFaixa("espessura", 25.3, 22.5, 27.5, "µm"),
    EnsaioMinimo("tração", 18.0, 20.0, "MPa"),
    EnsaioMaximo("cof", 0.22, 0.30),
]
for ensaio in ensaios:  # o mesmo laudo() funciona para todos: polimorfismo
    print(ensaio.laudo())

print("EnsaioMinimo é um Ensaio?", issubclass(EnsaioMinimo, Ensaio))
print("Ordem de busca (MRO):", [c.__name__ for c in EnsaioMinimo.__mro__])
try:
    Ensaio("genérico", 1.0)
except TypeError as erro:
    print("Erro:", erro)
