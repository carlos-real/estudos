import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_depurar_peso")


def test_previsao_a_caso_que_funciona():
    assert ex.previsoes()[0] == pytest.approx(25.0)


def test_previsao_b_peso_errado_silencioso():
    assert ex.previsoes()[1] == pytest.approx(250.5), (
        "Releia: \\d+ não aceita ponto, mas o search continua procurando no resto da linha."
    )


def test_previsao_c_nome_do_erro():
    assert ex.previsoes()[2] == "AttributeError", (
        "Sem vírgula, o search devolve None. O que acontece em None.group(1)?"
    )


@pytest.mark.parametrize(
    ("linha", "esperado"),
    [
        ("OP: 123456 | NF: 98765 | Peso: 1.250,5 kg", 1250.5),
        ("Peso: 25,0 kg", 25.0),
        ("peso 980", 980.0),
        ("PESO:2.000,00 KG", 2000.0),
        ("Peso: 75,25", 75.25),
    ],
)
def test_extrai_peso_corrigido(linha, esperado):
    assert ex.extrair_peso(linha) == pytest.approx(esperado)


def test_ignora_outros_numeros_com_kg():
    assert ex.extrair_peso("Tara: 12,5 kg | Peso: 25,0 kg") == pytest.approx(25.0), (
        "O peso é o número depois da palavra 'Peso', não o primeiro número com kg."
    )


@pytest.mark.parametrize("linha", ["Bom dia, laboratório!", "Peso: a confirmar", ""])
def test_linha_sem_peso_devolve_none(linha):
    assert ex.extrair_peso(linha) is None
