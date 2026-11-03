"""
Exercício 13.05 — Modelo Pydantic de uma medição
Nível: ★☆☆

Contexto: antes de aceitar uma medição na API, queremos garantir que ela faz
sentido: OP com 6 dígitos, linha que existe, valor positivo. Um modelo
Pydantic descreve essas regras uma vez e valida tudo sozinho.

Tarefa:
1. Complete a classe Medicao (herda de BaseModel) com os campos:
   - op: str com exatamente 6 dígitos (Field(pattern=r"^\\d{6}$"))
   - linha: só "A", "B", "C" ou "D" (Literal["A", "B", "C", "D"])
   - ensaio: str com pelo menos 2 caracteres (Field(min_length=2))
   - valor: float maior que zero (Field(gt=0))
   - unidade: str, padrão "µm"
   - observacao: str ou None, padrão None
2. Implemente resumo(medicao), que devolve um texto assim:
       "OP 123456 | linha A | espessura: 20.4 µm"
   (use o valor como o Python mostra o float, sem formatar).

Exemplos:
    >>> m = Medicao(op="123456", linha="A", ensaio="espessura", valor="20.4")
    >>> m.valor
    20.4
    >>> resumo(m)
    'OP 123456 | linha A | espessura: 20.4 µm'
    >>> Medicao(op="12345", linha="A", ensaio="cof", valor=0.2)
    Traceback (most recent call last):
    ...
    pydantic_core._pydantic_core.ValidationError: 1 validation error for Medicao

Dica: from typing import Literal; from pydantic import Field. Um campo com
valor padrão (unidade: str = "µm") vira opcional.

Teste com:  python curso.py testar 13 ex05
"""

from pydantic import BaseModel


class Medicao(BaseModel):
    """Uma medição de laboratório validada."""

    # Escreva seus campos aqui (op, linha, ensaio, valor, unidade, observacao)


def resumo(medicao: Medicao) -> str:
    """Texto curto para log: 'OP 123456 | linha A | espessura: 20.4 µm'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
