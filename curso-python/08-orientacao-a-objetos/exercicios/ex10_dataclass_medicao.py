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

from datetime import date


class Medicao:
    """Uma medição registrada (imutável)."""

    def __init__(self, data: date, linha: str, valor: float, observacao: str = "") -> None:
        # __init__ provisório: apague-o e transforme a classe numa dataclass
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta classe")


def ordenar(medicoes: list[Medicao]) -> list[Medicao]:
    """Medições em ordem de data, linha e valor."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ultima_por_linha(medicoes: list[Medicao]) -> dict[str, Medicao]:
    """Medição mais recente de cada linha."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def sem_duplicadas(medicoes: list[Medicao]) -> list[Medicao]:
    """Remove medições repetidas, mantendo a primeira e a ordem."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
