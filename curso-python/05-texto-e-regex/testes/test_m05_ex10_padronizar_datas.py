import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_padronizar_datas")


def test_troca_duas_datas():
    texto = "Produzido em 05/03/2025, liberado em 07/03/2025."
    assert ex.padronizar_datas(texto) == "Produzido em 2025-03-05, liberado em 2025-03-07."


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("5/3/2025", "2025-03-05"),
        ("31/12/2024", "2024-12-31"),
        ("1/10/2025", "2025-10-01"),
        ("10/1/2025", "2025-01-10"),
    ],
)
def test_completa_zeros_de_dia_e_mes(entrada, esperado):
    assert ex.padronizar_datas(entrada) == esperado


@pytest.mark.parametrize(
    "texto",
    [
        "Lote 2025-A-0153 sem data",
        "NF 123/2025",
        "Relação 1/2",
        "105/03/2025",
        "01/02/20251",
    ],
)
def test_texto_sem_data_nao_muda(texto):
    assert ex.padronizar_datas(texto) == texto


def test_varias_linhas():
    texto = "Coleta: 2/9/2025\nLaudo: 03/09/2025"
    assert ex.padronizar_datas(texto) == "Coleta: 2025-09-02\nLaudo: 2025-09-03"
