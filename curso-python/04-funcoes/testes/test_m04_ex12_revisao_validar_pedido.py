import copy

import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_validar_pedido")


@pytest.mark.parametrize("op", ["OP-4512", " op-45120 ", "OP-123456"])
def test_op_valida(op):
    assert ex.validar_op(op) is None


@pytest.mark.parametrize(
    ("op", "esperado"),
    [
        ("OP-12", "OP inválida: 'OP-12'"),
        ("OP-1234567", "OP inválida: 'OP-1234567'"),
        ("4512", "OP inválida: '4512'"),
        ("op 4512", "OP inválida: 'OP 4512'"),
        ("OP-45A2", "OP inválida: 'OP-45A2'"),
        ("   ", "OP vazia"),
    ],
)
def test_op_invalida(op, esperado):
    assert ex.validar_op(op) == esperado


@pytest.mark.parametrize("nf", ["1", "000123456", " 4501 "])
def test_nf_valida(nf):
    assert ex.validar_nf(nf) is None


@pytest.mark.parametrize(
    ("nf", "esperado"),
    [
        ("12A", "NF inválida: '12A'"),
        ("1234567890", "NF inválida: '1234567890'"),
        ("", "NF vazia"),
    ],
)
def test_nf_invalida(nf, esperado):
    assert ex.validar_nf(nf) == esperado


@pytest.mark.parametrize(
    ("peso", "esperado"),
    [
        (1250.5, None),
        (30000, None),
        (None, "peso ausente"),
        (0, "peso deve ser maior que zero"),
        (-5, "peso deve ser maior que zero"),
        (30000.1, "peso acima de 30000 kg (confira a unidade)"),
    ],
)
def test_validar_peso(peso, esperado):
    assert ex.validar_peso(peso) == esperado


def test_validar_pedido_valido():
    assert ex.validar_pedido({"op": "OP-4512", "nf": "123", "peso_kg": 10.0}) == []


def test_validar_pedido_lista_problemas_na_ordem():
    pedido = {"op": "OP-12", "nf": "12A", "peso_kg": 0}
    assert ex.validar_pedido(pedido) == [
        "OP inválida: 'OP-12'",
        "NF inválida: '12A'",
        "peso deve ser maior que zero",
    ]


def test_validar_pedido_chaves_ausentes_ou_none():
    assert ex.validar_pedido({}) == ["OP vazia", "NF vazia", "peso ausente"]
    assert ex.validar_pedido({"op": None, "nf": None, "peso_kg": None}) == [
        "OP vazia",
        "NF vazia",
        "peso ausente",
    ]


PEDIDOS = [
    {"op": " op-45120", "nf": " 123456 ", "peso_kg": 1250.5, "cliente": "Alfa"},
    {"op": "OP-12", "nf": "123", "peso_kg": 0},
    {"nf": "777", "peso_kg": 500.0},
    {"op": "OP-4513", "nf": "124", "peso_kg": 80.0},
]


def test_separar_pedidos():
    validos, mensagens = ex.separar_pedidos(PEDIDOS)
    assert validos == [
        {"op": "OP-45120", "nf": "123456", "peso_kg": 1250.5, "cliente": "Alfa"},
        {"op": "OP-4513", "nf": "124", "peso_kg": 80.0},
    ]
    assert mensagens == [
        "pedido 2: OP inválida: 'OP-12'; peso deve ser maior que zero",
        "pedido 3: OP vazia",
    ]


def test_separar_pedidos_nao_altera_os_originais():
    pedidos = copy.deepcopy(PEDIDOS)
    ex.separar_pedidos(pedidos)
    assert pedidos == PEDIDOS, "Crie dicionários novos para os pedidos limpos."


def test_separar_lista_vazia():
    assert ex.separar_pedidos([]) == ([], [])
