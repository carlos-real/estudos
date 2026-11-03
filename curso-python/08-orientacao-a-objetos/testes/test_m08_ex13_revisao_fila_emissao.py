import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_fila_emissao")
P = ex.PedidoExpedicao

EMAIL = """Bom dia! Segue a programação de hoje.
OP 245101 - NF 123456 - Peso: 1.250,5 kg
op 245102 - nf 123456 - peso: 980,00 kg
OP245107 -NF 123460- Peso:2.010,75 kg
Att., Expedição
"""


def test_fila_comeca_vazia():
    fila = ex.FilaDeEmissao()
    assert len(fila) == 0
    assert list(fila) == []
    assert fila.peso_total == 0


def test_adicionar_e_len():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 10.0))
    fila.adicionar(P("OP2", "100", 5.5))  # mesma NF, outra OP: pode
    assert len(fila) == 2


def test_adicionar_repetido_gera_value_error():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 10.0))
    with pytest.raises(ValueError):
        fila.adicionar(P("OP1", "100", 12.0))
    assert len(fila) == 1


def test_proximo_e_fifo():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 10.0))
    fila.adicionar(P("OP2", "200", 20.0))
    assert fila.proximo() == P("OP1", "100", 10.0)
    assert fila.proximo() == P("OP2", "200", 20.0)
    assert len(fila) == 0


def test_proximo_em_fila_vazia():
    with pytest.raises(ex.FilaVaziaError):
        ex.FilaDeEmissao().proximo()


def test_iterar_nao_esvazia_a_fila():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 10.0))
    fila.adicionar(P("OP2", "200", 20.0))
    assert [p.op for p in fila] == ["OP1", "OP2"]
    assert [p.op for p in fila] == ["OP1", "OP2"], "Iterar duas vezes dá o mesmo resultado"
    assert len(fila) == 2


def test_contains_por_nf():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 10.0))
    assert "100" in fila
    assert "999" not in fila


def test_adicionar_do_email():
    fila = ex.FilaDeEmissao()
    assert fila.adicionar_do_email(EMAIL) == 3
    assert list(fila) == [
        P("OP245101", "123456", 1250.5),
        P("OP245102", "123456", 980.0),
        P("OP245107", "123460", 2010.75),
    ]


def test_adicionar_do_email_ignora_repetidos():
    fila = ex.FilaDeEmissao()
    fila.adicionar_do_email(EMAIL)
    assert fila.adicionar_do_email(EMAIL) == 0, "Repetidos são ignorados, sem erro"
    assert fila.adicionar_do_email("OP 245200 - NF 9001 - Peso: 10 kg\n" + EMAIL) == 1
    assert len(fila) == 4
    assert fila.adicionar_do_email("Sem pedidos hoje.") == 0


def test_peso_total_e_repr():
    fila = ex.FilaDeEmissao()
    fila.adicionar(P("OP1", "100", 0.1))
    fila.adicionar(P("OP2", "100", 0.2))
    assert fila.peso_total == 0.3
    fila.adicionar_do_email(EMAIL)
    assert repr(fila) == "FilaDeEmissao(5 pedidos, 4241.55 kg)"
