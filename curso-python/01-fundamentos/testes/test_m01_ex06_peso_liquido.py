import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_peso_liquido")


def test_palete_com_oito_bobinas():
    assert ex.calcular_peso_liquido(1250.5, 22.0, 8, 1.35) == pytest.approx(1217.7)


def test_resultado_arredondado_em_duas_casas():
    resultado = ex.calcular_peso_liquido(500.0, 18.7, 4, 1.237)
    assert resultado == pytest.approx(476.35, abs=1e-9), (
        f"Sua função devolveu {resultado}. Faltou arredondar com round(valor, 2)?"
    )


def test_sem_bobinas_desconta_so_o_palete():
    assert ex.calcular_peso_liquido(300.0, 20.0, 0, 1.5) == pytest.approx(280.0)


def test_tubetes_sao_multiplicados_pela_quantidade():
    # 1000 - 25 - 10 * 2 = 955
    assert ex.calcular_peso_liquido(1000.0, 25.0, 10, 2.0) == pytest.approx(955.0)
