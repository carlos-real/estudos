"""Modelos de dados do domínio: as "fichas" que circulam entre as camadas.

Nenhum modelo sabe ler planilha, banco ou e-mail. Eles só guardam dados e
garantem que esses dados fazem sentido (validação no __post_init__).
"""

from __future__ import annotations

from dataclasses import dataclass, field

TIPOS_TOLERANCIA = ("fixa", "nominal")


@dataclass(frozen=True)
class Tolerancia:
    """Limite de uma característica.

    - tipo "fixa": usa `minimo` e/ou `maximo` (None = sem limite daquele lado).
    - tipo "nominal": usa `percentual` sobre o valor nominal da OP (ex.: ± 10%).
    """

    caracteristica: str
    tipo: str
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None

    def __post_init__(self) -> None:
        if self.tipo not in TIPOS_TOLERANCIA:
            raise ValueError(f"tipo de tolerância inválido: {self.tipo!r}")
        if self.tipo == "fixa":
            if self.minimo is None and self.maximo is None:
                raise ValueError(f"{self.caracteristica}: tolerância fixa sem mínimo e máximo")
            if self.minimo is not None and self.maximo is not None:
                if self.minimo > self.maximo:
                    raise ValueError(f"{self.caracteristica}: mínimo maior que o máximo")
        elif self.percentual is None or self.percentual <= 0:
            raise ValueError(
                f"{self.caracteristica}: tolerância nominal precisa de percentual > 0"
            )


@dataclass
class Especificacao:
    """Conjunto de tolerâncias. `linha` só é preenchida nos padrões de linha."""

    titulo: str
    texto: str = ""
    linha: str = ""
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)


@dataclass
class Medicao:
    """Uma linha da planilha de valores (uma OP)."""

    op: str
    aba: str
    linha: str
    valores: dict[str, float] = field(default_factory=dict)
    nominais: dict[str, float] = field(default_factory=dict)
    especificacao: str = ""
    observacao: str = ""
    produto: str = ""
    linha_excel: int = 0


@dataclass(frozen=True)
class Pedido:
    """Pedido de certificado vindo da expedição (um por e-mail)."""

    op: str
    nf: str
    peso_kg: float
    origem: str = ""

    def __post_init__(self) -> None:
        if not self.op.strip() or not self.nf.strip():
            raise ValueError("pedido precisa de OP e NF")
        if self.peso_kg <= 0:
            raise ValueError(f"peso deve ser maior que zero (recebido: {self.peso_kg})")


@dataclass
class ResultadoValidacao:
    """Resultado da conferência de uma OP contra uma especificação."""

    op: str
    especificacao: str
    motivos: list[str] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not self.motivos


@dataclass
class ItemFila:
    """Um pedido depois da triagem.

    situacao: "emitir" ou "bloqueado" (triagem); depois da emissão:
    "ensaio", "emitido", "falha" ou "ignorado".
    """

    op: str
    nf: str
    peso_kg: float
    situacao: str
    especificacao: str = ""
    motivos: list[str] = field(default_factory=list)
    comprovante: str = ""


class EspecificacaoDesconhecida(Exception):
    """O título informado não existe no banco (ou a linha não tem padrão)."""


class PedidoInvalido(ValueError):
    """E-mail da expedição fora do padrão (falta OP, NF, peso, ou há ambiguidade)."""


class PlanilhaInvalida(ValueError):
    """A planilha não tem o formato combinado (ex.: falta uma coluna)."""
