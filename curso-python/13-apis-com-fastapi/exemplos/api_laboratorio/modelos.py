"""Modelos Pydantic: o contrato da API (o que entra e o que sai)."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Linha = Literal["A", "B", "C", "D"]


class Tolerancia(BaseModel):
    linha: Linha
    ensaio: str
    tipo: Literal["faixa", "nominal"]
    minimo: float
    maximo: float


class MedicaoEntrada(BaseModel):
    op: str = Field(pattern=r"^\d{6}$", examples=["123456"])
    linha: Linha
    ensaio: str = Field(min_length=2, examples=["espessura"])
    valor: float = Field(gt=0, examples=[20.4])

    @field_validator("ensaio")
    @classmethod
    def padronizar_ensaio(cls, valor: str) -> str:
        return valor.strip().lower()


class MedicaoAvaliada(MedicaoEntrada):
    id: int
    minimo: float
    maximo: float
    aprovado: bool


class SituacaoOP(BaseModel):
    op: str
    medicoes: int
    reprovadas: int
    liberada: bool
