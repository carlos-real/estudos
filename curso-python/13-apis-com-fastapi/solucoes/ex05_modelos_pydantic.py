"""
Exercício 13.05 — Modelo Pydantic de uma medição (SOLUÇÃO)
"""

from typing import Literal

from pydantic import BaseModel, Field


class Medicao(BaseModel):
    """Uma medição de laboratório validada."""

    # pattern: regex que o texto INTEIRO precisa seguir (^ e $ = início e fim).
    op: str = Field(pattern=r"^\d{6}$")
    # Literal: só estes valores. Mais simples que um Enum quando são poucos textos.
    linha: Literal["A", "B", "C", "D"]
    ensaio: str = Field(min_length=2)
    # gt = greater than (maior que). Há também ge, lt e le.
    # O Pydantic converte "20.4" (texto) em 20.4 (float) no modo padrão.
    valor: float = Field(gt=0)
    unidade: str = "µm"
    observacao: str | None = None


def resumo(medicao: Medicao) -> str:
    """Texto curto para log: 'OP 123456 | linha A | espessura: 20.4 µm'."""
    # Dentro do código, uma Medicao validada é um objeto comum: atributos com
    # ponto, com os tipos garantidos. Nada de dados["valor"] e torcer.
    return (
        f"OP {medicao.op} | linha {medicao.linha} | "
        f"{medicao.ensaio}: {medicao.valor} {medicao.unidade}"
    )
