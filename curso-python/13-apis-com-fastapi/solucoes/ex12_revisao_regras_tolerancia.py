"""
Exercício 13.12 — Revisão: regras de tolerância (faixa e nominal ± %) na API (SOLUÇÃO)
"""

from enum import Enum
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

Linha = Literal["A", "B", "C", "D"]


class TipoTolerancia(str, Enum):
    # Herdar de str faz o Enum virar texto no JSON ("faixa"), sem conversão manual.
    FAIXA = "faixa"
    NOMINAL = "nominal"


def numero_br(valor: str | int | float) -> float:
    """Converte número do Python ou texto (brasileiro ou não) em float."""
    if isinstance(valor, (int, float)):
        return float(valor)
    texto = str(valor).strip()
    if "," in texto:
        # Formato brasileiro: tira os pontos de milhar, vírgula vira ponto (módulo 05).
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)  # texto inválido -> ValueError, como pede o enunciado


class Regra(BaseModel):
    """Tolerância por faixa ou por nominal ± %. Complete campos e validador."""

    tipo: TipoTolerancia
    minimo: float | None = None
    maximo: float | None = None
    nominal: float | None = None
    percentual: float | None = None

    @model_validator(mode="after")
    def conferir_campos(self) -> "Regra":
        # "after": roda depois que cada campo já foi validado e convertido.
        # É o lugar para regras que envolvem VÁRIOS campos ao mesmo tempo.
        if self.tipo == TipoTolerancia.FAIXA:
            if self.minimo is None or self.maximo is None:
                raise ValueError("faixa exige minimo e maximo")
            if self.minimo > self.maximo:
                raise ValueError("minimo não pode ser maior que maximo")
        else:
            if self.nominal is None or self.percentual is None:
                raise ValueError("nominal exige nominal e percentual")
            if self.nominal <= 0 or not 0 < self.percentual <= 100:
                raise ValueError("nominal deve ser > 0 e percentual entre 0 e 100")
        return self


def limites(regra: Regra) -> tuple[float, float]:
    """(mínimo, máximo) da regra."""
    if regra.tipo == TipoTolerancia.FAIXA:
        return regra.minimo, regra.maximo
    folga = regra.nominal * regra.percentual / 100
    # round(..., 4) evita 36.480000000000004 no relatório.
    return round(regra.nominal - folga, 4), round(regra.nominal + folga, 4)


class ItemLote(BaseModel):
    """Uma medição do lote. Campos: ensaio, valor (aceita "20,5")."""

    ensaio: str
    valor: float

    @field_validator("valor", mode="before")
    @classmethod
    def aceitar_formato_brasileiro(cls, valor):
        # "before": recebe o dado CRU (ainda pode ser "1.250,5"). O ValueError
        # de numero_br vira um erro de validação 422 automaticamente.
        return numero_br(valor)


class Lote(BaseModel):
    """Campos: linha (A a D) e medicoes (lista de ItemLote, ao menos 1)."""

    linha: Linha
    medicoes: list[ItemLote] = Field(min_length=1)


REGRAS: dict[tuple[str, str], Regra] = {}

app = FastAPI()


def resposta_da_regra(linha: str, ensaio: str, regra: Regra) -> dict:
    minimo, maximo = limites(regra)
    return {
        "linha": linha,
        "ensaio": ensaio,
        "tipo": regra.tipo,
        "minimo": minimo,
        "maximo": maximo,
    }


@app.put("/regras/{linha}/{ensaio}")
def gravar_regra(linha: Linha, ensaio: str, regra: Regra) -> dict:
    # PUT é idempotente: gravar a mesma regra duas vezes dá o mesmo resultado.
    ensaio = ensaio.lower()
    REGRAS[(linha, ensaio)] = regra
    return resposta_da_regra(linha, ensaio, regra)


@app.get("/regras/{linha}/{ensaio}")
def ver_regra(linha: Linha, ensaio: str) -> dict:
    ensaio = ensaio.lower()
    regra = REGRAS.get((linha, ensaio))
    if regra is None:
        raise HTTPException(status_code=404, detail="Regra não cadastrada")
    return resposta_da_regra(linha, ensaio, regra)


@app.post("/lotes/validar")
def validar_lote(lote: Lote) -> dict:
    itens, sem_regra = [], []
    for item in lote.medicoes:
        ensaio = item.ensaio.lower()
        regra = REGRAS.get((lote.linha, ensaio))
        if regra is None:
            sem_regra.append(ensaio)
            continue
        minimo, maximo = limites(regra)
        itens.append(
            {
                "ensaio": ensaio,
                "valor": item.valor,
                "minimo": minimo,
                "maximo": maximo,
                "aprovado": minimo <= item.valor <= maximo,
            }
        )
    aprovado = not sem_regra and all(i["aprovado"] for i in itens)
    return {"linha": lote.linha, "aprovado": aprovado, "itens": itens, "sem_regra": sem_regra}
