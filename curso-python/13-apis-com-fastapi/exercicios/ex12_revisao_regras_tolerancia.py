"""
Exercício 13.12 — Revisão: regras de tolerância (faixa e nominal ± %) na API
Nível: ★★★

Revisão de: Enum (módulo 08), números no formato brasileiro (módulo 05),
funções puras (módulo 04) + validação avançada com Pydantic (este módulo).

Contexto: o projeto final precisa de dois tipos de tolerância. Por FAIXA
(COF de 0,20 a 0,30) e por NOMINAL ± % (espessura 40 µm ± 5%, ou seja, 38 a
42). E as medições às vezes chegam como texto copiado do Excel: "1.250,5".

Tarefa:
1. TipoTolerancia: um Enum de texto (class TipoTolerancia(str, Enum)) com
   FAIXA = "faixa" e NOMINAL = "nominal".
2. numero_br(valor): int/float -> float. Texto COM vírgula é brasileiro
   ("1.250,5" -> 1250.5; "20,5" -> 20.5). Texto SEM vírgula vale como número
   Python ("20.5" -> 20.5). Texto inválido -> ValueError.
3. Regra (BaseModel): tipo (TipoTolerancia) e minimo, maximo, nominal,
   percentual (float ou None, padrão None). Um @model_validator(mode="after")
   exige:
   - faixa: minimo e maximo preenchidos e minimo <= maximo;
   - nominal: nominal > 0 e 0 < percentual <= 100 (ambos preenchidos).
   Senão, levante ValueError (o Pydantic transforma em ValidationError / 422).
4. limites(regra) -> (minimo, maximo). Para nominal:
   (round(nominal - folga, 4), round(nominal + folga, 4)), folga = nominal * percentual / 100.
5. ItemLote: ensaio (str) e valor (float), com @field_validator("valor",
   mode="before") que usa numero_br (texto inválido vira 422).
   Lote: linha (Literal "A" a "D") e medicoes (list[ItemLote], ao menos 1 item).
6. Rotas (guarde as regras em REGRAS[(linha, ensaio)]; ensaio sempre em minúsculas):
   - PUT /regras/{linha}/{ensaio}, corpo Regra -> 200 com
     {"linha", "ensaio", "tipo", "minimo", "maximo"} (limites já calculados).
     Linha fora de A-D -> 422 (use Literal no parâmetro de caminho).
   - GET /regras/{linha}/{ensaio} -> o mesmo formato, ou 404 com detail
     "Regra não cadastrada".
   - POST /lotes/validar, corpo Lote -> {"linha": ..., "aprovado": bool,
     "itens": [{"ensaio", "valor", "minimo", "maximo", "aprovado"}, ...],
     "sem_regra": [ensaios sem regra, na ordem do lote]}.
     Itens sem regra não entram em "itens". O lote só é aprovado se todos os
     itens forem aprovados E "sem_regra" estiver vazio.

Exemplos:
    >>> numero_br("1.250,5")
    1250.5
    >>> cliente.put("/regras/B/espessura", json={"tipo": "nominal", "nominal": 40,
    ...                                          "percentual": 5}).json()
    {'linha': 'B', 'ensaio': 'espessura', 'tipo': 'nominal', 'minimo': 38.0, 'maximo': 42.0}

Dica: from pydantic import model_validator, field_validator. No validador
"after", use self.tipo, self.minimo... e termine com `return self`.

Teste com:  python curso.py testar 13 ex12
"""

from fastapi import FastAPI
from pydantic import BaseModel

# Escreva aqui a classe TipoTolerancia (Enum)


def numero_br(valor: str | int | float) -> float:
    """Converte número do Python ou texto (brasileiro ou não) em float."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


class Regra(BaseModel):
    """Tolerância por faixa ou por nominal ± %. Complete campos e validador."""

    # Escreva seus campos e o model_validator aqui


def limites(regra: Regra) -> tuple[float, float]:
    """(mínimo, máximo) da regra."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


class ItemLote(BaseModel):
    """Uma medição do lote. Campos: ensaio, valor (aceita "20,5")."""

    # Escreva seus campos e o field_validator aqui


class Lote(BaseModel):
    """Campos: linha (A a D) e medicoes (lista de ItemLote, ao menos 1)."""

    # Escreva seus campos aqui


REGRAS: dict[tuple[str, str], Regra] = {}

app = FastAPI()

# Escreva suas rotas aqui
