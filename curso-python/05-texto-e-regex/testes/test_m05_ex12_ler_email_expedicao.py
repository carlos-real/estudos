import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_ler_email_expedicao")

EMAIL_PADRAO = """De: expedicao@plastifort.com.br
Assunto: Certificados - carga de 28/10

Bom dia, laboratório!

Favor emitir os certificados dos pedidos abaixo:

OP: 123456 | NF: 98765 | Peso: 1.250,5 kg
OP: 123457 | NF: 98766 | Peso: 980,0 kg
OP: 123458 | NF: 98767 | Peso: 2.040,75 kg

A OP 123459 vai na próxima carga.

Obrigado,
Expedição
"""


def test_email_padrao():
    assert ex.ler_email_expedicao(EMAIL_PADRAO) == [
        {"op": "123456", "nf": "98765", "peso_kg": 1250.5},
        {"op": "123457", "nf": "98766", "peso_kg": 980.0},
        {"op": "123458", "nf": "98767", "peso_kg": 2040.75},
    ]


@pytest.mark.parametrize(
    ("linha", "esperado"),
    [
        ("op 123457; nf 98.766; peso 980", {"op": "123457", "nf": "98766", "peso_kg": 980.0}),
        (
            "OP-123459 | NF: 98768 | PESO: 75,25",
            {"op": "123459", "nf": "98768", "peso_kg": 75.25},
        ),
        (
            "  OP:123460|NF:1.234.567|Peso:2.000,00KG  ",
            {"op": "123460", "nf": "1234567", "peso_kg": 2000.0},
        ),
        ("Op 123461 ; Nf: 5 ; Peso 12,5 kg", {"op": "123461", "nf": "5", "peso_kg": 12.5}),
    ],
)
def test_variacoes_de_digitacao(linha, esperado):
    assert ex.ler_email_expedicao(linha) == [esperado]


@pytest.mark.parametrize(
    "linha",
    [
        "A OP 123459 vai na próxima carga.",
        "OP: 12345 | NF: 98765 | Peso: 980 kg",
        "NF: 98765 | OP: 123456 | Peso: 980 kg",
        "OP: 123456 | NF: 98765",
        "Bom dia, laboratório!",
    ],
)
def test_linhas_que_nao_sao_pedido_sao_ignoradas(linha):
    assert ex.ler_email_expedicao(linha) == []


def test_email_vazio():
    assert ex.ler_email_expedicao("") == []


def test_quebras_de_linha_do_windows():
    email = (
        "Bom dia\r\nOP: 111111 | NF: 1 | Peso: 10 kg\r\nOP: 222222 | NF: 2 | Peso: 20 kg\r\n"
    )
    pedidos = ex.ler_email_expedicao(email)
    assert [p["op"] for p in pedidos] == ["111111", "222222"]
    assert [p["peso_kg"] for p in pedidos] == [10.0, 20.0]


def test_tipos_dos_campos():
    pedido = ex.ler_email_expedicao("OP: 123456 | NF: 98765 | Peso: 980 kg")[0]
    assert isinstance(pedido["op"], str) and isinstance(pedido["nf"], str)
    assert isinstance(pedido["peso_kg"], float)
