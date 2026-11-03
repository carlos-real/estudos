import pytest

from validador_certificados.texto import esta_liberado, normalizar, numero_br


def test_normalizar():
    assert normalizar("  COF:   Não  Liberado ") == "cof: nao liberado"
    assert normalizar(None) == ""


@pytest.mark.parametrize(
    "observacao",
    [
        "COF: liberado",
        "cof liberado",
        "COF:LIBERADO",
        "COF - LIBERADO",
        "Cof: Liberado. Bobina 2 com rebarba",
        "COF:\xa0líberado",
    ],
)
def test_observacoes_liberadas(observacao):
    assert esta_liberado(observacao) is True


@pytest.mark.parametrize(
    "observacao",
    [
        "COF: não liberado - refazer ensaio",
        "COF NAO LIBERADO",
        "COF: aguardando 24h",
        "liberado",
        "",
        None,
    ],
)
def test_observacoes_nao_liberadas(observacao):
    assert esta_liberado(observacao) is False


@pytest.mark.parametrize(
    ("texto", "esperado"), [("1.250,5", 1250.5), ("2.040", 2040.0), ("980,0", 980.0)]
)
def test_numero_br(texto, esperado):
    assert numero_br(texto) == pytest.approx(esperado)
