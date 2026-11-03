import dataclasses
from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_dataclass_medicao")
M = ex.Medicao

M1 = (date(2026, 10, 1), "B", 25.2)
M2 = (date(2026, 10, 1), "A", 20.4)
M3 = (date(2026, 9, 30), "C", 40.1)
M4 = (date(2026, 10, 5), "A", 19.8)


def test_campos_e_padrao():
    m = M(*M2)
    assert dataclasses.is_dataclass(m)
    assert [f.name for f in dataclasses.fields(m)] == ["data", "linha", "valor", "observacao"]
    assert m.observacao == ""


def test_imutavel():
    m = M(*M2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.valor = 99.0


def test_igualdade_ignora_observacao():
    assert M(*M2, "primeira") == M(*M2, "redigitada")
    assert M(*M2) != M(*M4)


def test_hash_permite_set():
    assert len({M(*M2, "x"), M(*M2, "y"), M(*M1)}) == 2


def test_ordem_por_data_linha_valor():
    assert M(*M3) < M(*M2) < M(*M1), "A ordem dos campos define a comparação"


def test_ordenar():
    medicoes = [M(*M1), M(*M4), M(*M3), M(*M2)]
    assert ex.ordenar(medicoes) == [M(*M3), M(*M2), M(*M1), M(*M4)]
    assert medicoes[0] == M(*M1), "ordenar devolve lista nova, sem mexer na original"


def test_ultima_por_linha():
    resultado = ex.ultima_por_linha([M(*M4), M(*M1), M(*M2), M(*M3)])
    assert resultado == {"A": M(*M4), "B": M(*M1), "C": M(*M3)}
    assert list(resultado) == ["A", "B", "C"]


def test_sem_duplicadas_mantem_primeira_e_ordem():
    primeira = M(*M2, "1ª")
    entrada = [M(*M1), primeira, M(*M1), M(*M2, "redigitada"), M(*M3)]
    resultado = ex.sem_duplicadas(entrada)
    assert resultado == [M(*M1), M(*M2), M(*M3)]
    assert resultado[1].observacao == "1ª", "Mantenha a PRIMEIRA ocorrência"


def test_listas_vazias():
    assert ex.ordenar([]) == []
    assert ex.ultima_por_linha([]) == {}
    assert ex.sem_duplicadas([]) == []
