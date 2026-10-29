import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_formatar_medida")


def test_valores_padrao():
    assert ex.formatar_medida(50.24) == "50.2 µm"


def test_unidade_posicional():
    assert ex.formatar_medida(46, "g/m²") == "46.0 g/m²"


@pytest.mark.parametrize(
    ("kwargs", "esperado"),
    [
        ({"casas": 2}, "50.24 µm"),
        ({"casas": 0}, "50 µm"),
        ({"unidade": "kg"}, "50.2 kg"),
        ({"decimal": ","}, "50,2 µm"),
        ({"decimal": ",", "casas": 3, "unidade": "mm"}, "50,240 mm"),
    ],
)
def test_argumentos_nomeados_em_qualquer_ordem(kwargs, esperado):
    assert ex.formatar_medida(50.24, **kwargs) == esperado


def test_unidade_vazia_nao_deixa_espaco_no_fim():
    resultado = ex.formatar_medida(0.2234, unidade="", casas=3)
    assert resultado == "0.223", "Sem unidade, devolva só o número (sem espaço no fim)."


def test_peso_com_virgula():
    assert ex.formatar_medida(1250.5, unidade="kg", decimal=",") == "1250,5 kg"
