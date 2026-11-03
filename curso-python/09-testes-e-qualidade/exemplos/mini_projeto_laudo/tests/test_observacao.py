"""Testes da observação de liberação (escritos com TDD, um de cada vez)."""

import pytest

from observacao import ler_liberacoes


@pytest.mark.parametrize(
    ("observacao", "esperado"),
    [
        ("COF: liberado", {"COF": True}),
        ("Tração: reprovado", {"TRAÇÃO": False}),
        ("COF: liberado; Selagem: reprovado", {"COF": True, "SELAGEM": False}),
    ],
    ids=["um-liberado", "um-reprovado", "dois-ensaios"],
)
def test_ler_liberacoes(observacao, esperado):
    assert ler_liberacoes(observacao) == esperado


def test_status_desconhecido_levanta_erro():
    with pytest.raises(ValueError, match="pendente"):
        ler_liberacoes("COF: pendente")
