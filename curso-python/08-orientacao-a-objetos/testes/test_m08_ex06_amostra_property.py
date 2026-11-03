import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_amostra_property")


def test_criacao_normaliza_codigo_e_guarda_float():
    a = ex.Amostra(" am-001 ", 25)
    assert a.codigo == "AM-001"
    assert a.valor == 25.0 and type(a.valor) is float
    assert a.unidade == "µm"
    assert a.historico == ()


def test_codigo_e_so_leitura():
    a = ex.Amostra("AM-001", 25.3)
    with pytest.raises(AttributeError):
        a.codigo = "AM-999"
    assert a.codigo == "AM-001"


@pytest.mark.parametrize("codigo", ["", "   "])
def test_codigo_vazio_gera_value_error(codigo):
    with pytest.raises(ValueError):
        ex.Amostra(codigo, 25.3)


def test_alterar_valor_registra_historico():
    a = ex.Amostra("AM-001", 25.3)
    a.valor = 25.1
    a.valor = 24.9
    assert a.valor == pytest.approx(24.9)
    assert a.historico == (25.3, 25.1)


def test_historico_e_tupla_que_nao_altera_o_original():
    a = ex.Amostra("AM-001", 25.3)
    a.valor = 25.0
    historico = a.historico
    assert isinstance(historico, tuple)
    a.valor = 24.0
    assert historico == (25.3,), "Devolva uma cópia (tupla), não a lista interna"


@pytest.mark.parametrize("ruim", [-0.1, -25])
def test_valor_negativo_gera_value_error(ruim):
    a = ex.Amostra("AM-001", 25.3)
    with pytest.raises(ValueError):
        a.valor = ruim
    assert a.valor == pytest.approx(25.3), "Valor inválido não pode ser gravado"
    assert a.historico == ()


@pytest.mark.parametrize("ruim", ["25,3", None, True])
def test_valor_que_nao_e_numero_gera_type_error(ruim):
    a = ex.Amostra("AM-001", 25.3)
    with pytest.raises(TypeError):
        a.valor = ruim


def test_validacao_vale_tambem_no_init():
    with pytest.raises(ValueError):
        ex.Amostra("AM-001", -5)
    with pytest.raises(TypeError):
        ex.Amostra("AM-001", "25")


def test_zero_e_permitido():
    assert ex.Amostra("AM-001", 0).valor == 0.0
