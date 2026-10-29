"""Modelos com dataclasses: validação, imutabilidade, cópia e herança de regras.

Rode:  python exemplos/02_modelos_com_dataclasses.py
"""

from dataclasses import FrozenInstanceError, dataclass, field, replace


@dataclass(frozen=True)
class Tolerancia:
    caracteristica: str
    tipo: str
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None

    def __post_init__(self) -> None:
        if self.tipo not in ("fixa", "nominal"):
            raise ValueError(f"tipo de tolerância inválido: {self.tipo!r}")


@dataclass
class ItemFila:
    op: str
    nf: str
    situacao: str
    motivos: list[str] = field(default_factory=list)


# 1) O __post_init__ barra o objeto inválido na porta
try:
    Tolerancia("cof", "faixa", 0.15, 0.35)
except ValueError as erro:
    print("recusado:", erro)

# 2) frozen=True: regra carregada do banco não muda por acidente
cof = Tolerancia("cof", "fixa", 0.15, 0.35)
try:
    cof.maximo = 0.50
except FrozenInstanceError:
    print("Tolerancia é imutável")

# 3) replace: cópia com campos trocados (o original fica intacto)
item = ItemFila("24518", "123456", "emitir")
emitido = replace(item, situacao="ensaio")
print(item.situacao, "->", emitido.situacao)

# 4) {**padrao, **cliente}: o cliente sobrescreve só o que define
padrao_c = {
    "cof": Tolerancia("cof", "fixa", 0.10, 0.30),
    "selagem": Tolerancia("selagem", "fixa", 10.0),
}
esp_0412 = {"cof": Tolerancia("cof", "fixa", 0.18, 0.25)}
efetiva = {**padrao_c, **esp_0412}
for nome, tolerancia in efetiva.items():
    print(f"{nome}: mín {tolerancia.minimo}, máx {tolerancia.maximo}")
