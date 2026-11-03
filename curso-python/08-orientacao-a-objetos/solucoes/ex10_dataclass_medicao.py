"""
Exercício 08.10 — Medições imutáveis e ordenáveis com dataclass
Nível: ★★☆

Contexto: Medição registrada não se altera (rastreabilidade!). E você precisa
ordenar medições por data, pegar a última de cada linha e remover registros
duplicados que vieram da planilha (a mesma medição digitada duas vezes, às vezes
com observação diferente).

Tarefa:
1. Transforme `Medicao` numa dataclass IMUTÁVEL e ORDENÁVEL
   (`@dataclass(frozen=True, order=True)`) com os campos, nesta ordem:
       data: date
       linha: str
       valor: float
       observacao: str = ""   -> NÃO participa de comparação nem de igualdade:
                                use field(default="", compare=False)
   A ordem dos campos define a ordenação: primeiro data, depois linha, depois valor.
2. `ordenar(medicoes)`: nova lista em ordem (use sorted, que já sabe comparar).
3. `ultima_por_linha(medicoes)`: {linha: medição mais recente}, com as linhas em
   ordem alfabética.
4. `sem_duplicadas(medicoes)`: remove repetidas (iguais = mesma data, linha e
   valor), mantendo a PRIMEIRA ocorrência e a ordem original. Use um set de
   medições já vistas (frozen=True deixa a dataclass "hashable").

Exemplos:
    >>> from datetime import date
    >>> m = Medicao(date(2026, 10, 1), "A", 20.4, "1ª leitura")
    >>> m == Medicao(date(2026, 10, 1), "A", 20.4, "redigitada")
    True
    >>> m.valor = 99
    Traceback (most recent call last):
    ...
    dataclasses.FrozenInstanceError: cannot assign to field 'valor'

Teste com:  python curso.py testar 08 ex10
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, order=True)
class Medicao:
    """Uma medição registrada (imutável)."""

    data: date
    linha: str
    valor: float
    # compare=False: fica fora de ==, <, > e do hash. Observação não muda a medição.
    observacao: str = field(default="", compare=False)


def ordenar(medicoes: list[Medicao]) -> list[Medicao]:
    """Medições em ordem de data, linha e valor."""
    # order=True gerou __lt__ e companhia, comparando os campos na ordem declarada.
    return sorted(medicoes)


def ultima_por_linha(medicoes: list[Medicao]) -> dict[str, Medicao]:
    """Medição mais recente de cada linha."""
    ultima: dict[str, Medicao] = {}
    for medicao in ordenar(medicoes):  # em ordem: a última atribuição é a mais recente
        ultima[medicao.linha] = medicao
    return {linha: ultima[linha] for linha in sorted(ultima)}


def sem_duplicadas(medicoes: list[Medicao]) -> list[Medicao]:
    """Remove medições repetidas, mantendo a primeira e a ordem."""
    vistas: set[Medicao] = set()  # só é possível porque a dataclass é frozen (hashable)
    resultado = []
    for medicao in medicoes:
        if medicao not in vistas:
            vistas.add(medicao)
            resultado.append(medicao)
    return resultado
