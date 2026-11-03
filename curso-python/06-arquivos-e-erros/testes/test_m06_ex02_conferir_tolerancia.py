import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_conferir_tolerancia")


@pytest.mark.parametrize("valor", [25.4, 22.5, 27.5])
def test_valor_dentro_da_faixa_e_devolvido(valor):
    assert ex.conferir_tolerancia(valor, 22.5, 27.5) == valor


@pytest.mark.parametrize("valor", [22.4, 28.0, -1.0])
def test_valor_fora_levanta_excecao_propria(valor):
    with pytest.raises(ex.ValorForaDaTolerancia):
        ex.conferir_tolerancia(valor, 22.5, 27.5)


def test_mensagem_mostra_valor_e_faixa():
    with pytest.raises(
        ex.ValorForaDaTolerancia, match=r"28\.0 fora da faixa \[22\.5, 27\.5\]"
    ):
        ex.conferir_tolerancia(28.0, 22.5, 27.5)


def test_faixa_invertida_levanta_value_error():
    with pytest.raises(ValueError, match="faixa inválida"):
        ex.conferir_tolerancia(25.0, 30.0, 20.0)


def test_faixa_invertida_nao_e_confundida_com_valor_fora():
    with pytest.raises(ValueError) as info:
        ex.conferir_tolerancia(25.0, 30.0, 20.0)
    assert not isinstance(info.value, ex.ValorForaDaTolerancia)
