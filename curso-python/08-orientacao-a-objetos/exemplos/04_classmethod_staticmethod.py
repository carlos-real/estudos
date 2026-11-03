"""Construtores alternativos (@classmethod) e funções utilitárias (@staticmethod).

Rode com:  python exemplos/04_classmethod_staticmethod.py
"""


class Tolerancia:
    def __init__(self, minimo: float, maximo: float) -> None:
        if minimo > maximo:
            raise ValueError("mínimo maior que máximo")
        self.minimo = minimo
        self.maximo = maximo

    @classmethod
    def por_nominal(cls, nominal: float, percentual: float) -> "Tolerancia":
        margem = nominal * percentual / 100
        return cls(nominal - margem, nominal + margem)

    @classmethod
    def de_texto(cls, texto: str) -> "Tolerancia":
        """'0,10 a 0,30' -> Tolerancia(0.1, 0.3)."""
        minimo, maximo = texto.split(" a ")
        return cls(cls.numero_br(minimo), cls.numero_br(maximo))

    @staticmethod
    def numero_br(texto: str) -> float:
        return float(texto.strip().replace(".", "").replace(",", "."))

    def aprova(self, valor: float) -> bool:
        return self.minimo <= valor <= self.maximo

    def __repr__(self) -> str:
        return f"Tolerancia({self.minimo!r}, {self.maximo!r})"


print(Tolerancia(0.10, 0.30))
print(Tolerancia.por_nominal(25, 10))
print(Tolerancia.de_texto("0,10 a 0,30"))
print(Tolerancia.numero_br("1.250,5"))
print("COF 0,32 aprovado?", Tolerancia.de_texto("0,10 a 0,30").aprova(0.32))
