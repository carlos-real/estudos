import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_liberacao")


def test_previsao_da_versao_do_estagiario():
    previsao = ex.prever_v1()
    assert len(previsao) == 4, "São 4 observações: devolva 4 respostas."
    assert previsao[0] is True, "1: 'não liberado' contém a palavra 'liberado'..."
    assert previsao[1] is True, "2: 'Liberado para corte' também contém 'liberado'."
    assert previsao[2] is False, "3: 'líberado' (com acento) não contém 'liberado'."
    assert previsao[3] == "AttributeError", "4: None não tem o método lower()."


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("  COF:   Não  Liberado ", "cof: nao liberado"),
        ("Observação", "observacao"),
        ("COF:\xa0LÍBERADO", "cof: liberado"),
        ("", ""),
        (None, ""),
    ],
)
def test_normalizar(texto, esperado):
    assert ex.normalizar(texto) == esperado


@pytest.mark.parametrize(
    "observacao",
    [
        "COF: liberado",
        "cof liberado",
        "COF:LIBERADO",
        "COF - LIBERADO",
        "COF -  liberada",
        "Cof: Liberado. Bobina 2 com rebarba",
        "Obs.: COF: liberado em 21/10",
        "COF: líberado",
    ],
)
def test_observacoes_liberadas(observacao):
    assert ex.esta_liberado(observacao) is True


@pytest.mark.parametrize(
    "observacao",
    [
        "COF: não liberado - refazer ensaio",
        "COF NAO LIBERADO",
        "COF: aguardando 24h",
        "Liberado para corte; COF pendente",
        "liberado",
        "",
        None,
    ],
)
def test_observacoes_nao_liberadas(observacao):
    assert ex.esta_liberado(observacao) is False
