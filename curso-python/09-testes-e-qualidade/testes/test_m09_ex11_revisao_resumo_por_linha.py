import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_revisao_resumo_por_linha")

TOLERANCIAS = {"A": (24.0, 26.0), "B": (18.0, 21.0), "C": (0.25, 0.35), "D": (20.0, 30.0)}


def test_conta_total_e_fora_por_linha():
    registros = ["A;25,0", "A;27,0", "B;19,0", "A;25,5", "B;20,0"]
    resultado = ex.resumir_por_linha(registros, TOLERANCIAS)
    assert resultado == {
        "A": {"total": 3, "fora": 1, "percentual_fora": 33.3},
        "B": {"total": 2, "fora": 0, "percentual_fora": 0.0},
    }


def test_percentual_com_uma_casa_decimal():
    registros = ["A;25,0", "A;23,0", "A;25,0", "A;25,0", "C;0,30", "C;0,20", "C;0,40"]
    resultado = ex.resumir_por_linha(registros, TOLERANCIAS)
    assert resultado["A"]["percentual_fora"] == pytest.approx(25.0)
    assert resultado["C"]["percentual_fora"] == pytest.approx(66.7)
    assert resultado["A"]["total"] == 4


def test_valores_nas_bordas_estao_dentro():
    registros = ["A;24,0", "A;26,0"]
    resultado = ex.resumir_por_linha(registros, TOLERANCIAS)
    assert resultado == {"A": {"total": 2, "fora": 0, "percentual_fora": 0.0}}, (
        "24,0 e 26,0 são as bordas da linha A: estão DENTRO"
    )


def test_linha_em_minusculas_e_com_espacos_e_a_mesma_linha():
    registros = [" a ;25,0", "A;30,0"]
    resultado = ex.resumir_por_linha(registros, TOLERANCIAS)
    assert resultado == {"A": {"total": 2, "fora": 1, "percentual_fora": 50.0}}


def test_todas_fora():
    registros = ["D;10,0", "D;50,0"]
    resultado = ex.resumir_por_linha(registros, TOLERANCIAS)
    assert resultado == {"D": {"total": 2, "fora": 2, "percentual_fora": 100.0}}


def test_linha_sem_tolerancia_levanta_value_error():
    with pytest.raises(ValueError, match="linha E sem tolerância"):
        ex.resumir_por_linha(["A;25,0", "E;25,0"], TOLERANCIAS)
