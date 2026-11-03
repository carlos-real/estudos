import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_enum_situacao")
S = ex.Situacao


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("liberado", S.LIBERADO),
        ("  LIBERADO ", S.LIBERADO),
        ("Reprovado", S.REPROVADO),
        ("pendente\n", S.PENDENTE),
    ],
)
def test_de_texto(texto, esperado):
    assert S.de_texto(texto) is esperado


@pytest.mark.parametrize("texto", ["liberada", "ok", ""])
def test_de_texto_desconhecido_gera_value_error(texto):
    with pytest.raises(ValueError):
        S.de_texto(texto)


def test_pode_emitir():
    assert S.LIBERADO.pode_emitir is True
    assert S.REPROVADO.pode_emitir is False
    assert S.PENDENTE.pode_emitir is False


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("COF: liberado", ("COF", S.LIBERADO)),
        ("  tração : REPROVADO", ("TRAÇÃO", S.REPROVADO)),
        ("Espessura:pendente ", ("ESPESSURA", S.PENDENTE)),
    ],
)
def test_interpretar_observacao(texto, esperado):
    assert ex.interpretar_observacao(texto) == esperado


def test_interpretar_observacao_separa_so_no_primeiro_dois_pontos():
    with pytest.raises(ValueError):
        ex.interpretar_observacao("COF: liberado: obs")  # "liberado: obs" não é situação


@pytest.mark.parametrize("texto", ["COF liberado", "", "situação desconhecida"])
def test_interpretar_observacao_sem_dois_pontos(texto):
    with pytest.raises(ValueError):
        ex.interpretar_observacao(texto)
