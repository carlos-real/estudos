from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_expedicao")

EMAIL = """Bom dia! Segue a programação.
Data de embarque: 05/11/2026
OP 245101 - NF 123456 - Peso: 1.250,5 kg
op 245102 - nf 123456 - peso: 980,00 kg
OP 245107 - NF 123460 - Peso: 2.010,75 kg
Att., Expedição
"""

EMAIL_SEM_DATA = """Pessoal, segue:
OP245200 -NF 9001- Peso:310,2 kg
OP  245201  -  NF 9002  -  Peso: 12.000 kg
"""


def test_extrair_itens_do_email():
    assert ex.extrair_itens(EMAIL) == [
        ("OP245101", "123456", pytest.approx(1250.5)),
        ("OP245102", "123456", pytest.approx(980.0)),
        ("OP245107", "123460", pytest.approx(2010.75)),
    ]


def test_extrair_itens_com_espacos_variados_e_milhar():
    itens = ex.extrair_itens(EMAIL_SEM_DATA)
    assert [(op, nf) for op, nf, _ in itens] == [("OP245200", "9001"), ("OP245201", "9002")]
    assert itens[1][2] == pytest.approx(12000.0), "'12.000' no Brasil é doze mil"


def test_extrair_itens_sem_itens():
    assert ex.extrair_itens("Bom dia, hoje não tem embarque.") == []


def test_extrair_data_embarque():
    assert ex.extrair_data_embarque(EMAIL) == date(2026, 11, 5)
    assert ex.extrair_data_embarque("DATA DE EMBARQUE: 01/12/2026") == date(2026, 12, 1)


def test_extrair_data_embarque_ausente():
    assert ex.extrair_data_embarque(EMAIL_SEM_DATA) is None


@pytest.mark.parametrize(
    ("dias_antes", "esperado"),
    [
        (2, date(2026, 11, 3)),  # terça
        (1, date(2026, 11, 4)),
        (4, date(2026, 10, 30)),  # 01/11 é domingo: recua para sexta 30/10
        (5, date(2026, 10, 30)),  # 31/10 é sábado: recua para sexta 30/10
    ],
)
def test_prazo_certificado(dias_antes, esperado):
    assert ex.prazo_certificado(EMAIL, dias_antes) == esperado


def test_prazo_certificado_padrao_sao_dois_dias():
    assert ex.prazo_certificado(EMAIL) == date(2026, 11, 3)


def test_prazo_certificado_sem_data():
    assert ex.prazo_certificado(EMAIL_SEM_DATA) is None


def test_total_por_nf():
    assert ex.total_por_nf(EMAIL) == {
        "123456": pytest.approx(2230.5),
        "123460": pytest.approx(2010.75),
    }
    assert list(ex.total_por_nf(EMAIL)) == ["123456", "123460"]


def test_total_por_nf_sem_itens():
    assert ex.total_por_nf("nada aqui") == {}
