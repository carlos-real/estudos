"""dataclasses: menos código repetido, mais recursos.

Rode com:  python exemplos/07_dataclasses.py
"""

from dataclasses import FrozenInstanceError, asdict, dataclass, field, replace
from datetime import date


@dataclass
class Bobina:
    lote: str
    numero: int
    peso_kg: float
    defeitos: list[str] = field(default_factory=list)  # lista nova para cada bobina

    def __post_init__(self) -> None:
        if self.peso_kg <= 0:
            raise ValueError(f"Peso inválido: {self.peso_kg}")


b1 = Bobina("L2610", 1, 152.4)
b2 = Bobina("L2610", 1, 152.4)
print(b1)
print("Iguais?", b1 == b2, "| mesmo objeto?", b1 is b2)
b1.defeitos.append("gel")
print("Defeitos b1:", b1.defeitos, "| b2:", b2.defeitos)
print("Como dicionário:", asdict(b1))


@dataclass(frozen=True, order=True)
class Medicao:
    data: date
    linha: str
    valor: float
    observacao: str = field(default="", compare=False)


m1 = Medicao(date(2026, 10, 2), "A", 20.4)
m2 = Medicao(date(2026, 10, 1), "B", 25.2, "redigitada")
print(sorted([m1, m2])[0].linha, "vem primeiro (data menor)")
try:
    m1.valor = 99.0
except FrozenInstanceError as erro:
    print("Erro:", erro)
corrigida = replace(m1, valor=20.1)  # imutável: cria OUTRA com o campo trocado
print("Original:", m1.valor, "| corrigida:", corrigida.valor)
print("Hashable (pode ir para set):", len({m1, corrigida, m1}))
