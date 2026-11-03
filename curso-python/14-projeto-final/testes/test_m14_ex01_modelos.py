import dataclasses

import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_modelos")


def test_tolerancia_fixa_valida():
    tolerancia = ex.Tolerancia("cof", "fixa", minimo=0.15, maximo=0.35)
    assert (tolerancia.minimo, tolerancia.maximo) == (0.15, 0.35)


@pytest.mark.parametrize(("minimo", "maximo"), [(20.0, None), (None, 0.35), (0.25, 0.25)])
def test_tolerancia_fixa_com_um_lado_so_ou_limites_iguais(minimo, maximo):
    tolerancia = ex.Tolerancia("tracao", "fixa", minimo=minimo, maximo=maximo)
    assert tolerancia.tipo == "fixa"


def test_tolerancia_nominal_valida():
    tolerancia = ex.Tolerancia("espessura", "nominal", percentual=10.0)
    assert tolerancia.percentual == 10.0


@pytest.mark.parametrize(
    "argumentos",
    [
        {"tipo": "faixa", "minimo": 0.1, "maximo": 0.3},
        {"tipo": "FIXA", "minimo": 0.1, "maximo": 0.3},
        {"tipo": "fixa"},
        {"tipo": "fixa", "minimo": 0.40, "maximo": 0.20},
        {"tipo": "nominal"},
        {"tipo": "nominal", "percentual": 0},
        {"tipo": "nominal", "percentual": -5.0},
    ],
)
def test_tolerancia_invalida_levanta_value_error(argumentos):
    with pytest.raises(ValueError):
        ex.Tolerancia("cof", **argumentos)


def test_tolerancia_e_imutavel():
    tolerancia = ex.Tolerancia("cof", "fixa", minimo=0.15, maximo=0.35)
    with pytest.raises(dataclasses.FrozenInstanceError):
        tolerancia.maximo = 0.50


def test_pedido_valido():
    pedido = ex.Pedido(op="24518", nf="123456", peso_kg=1250.5, origem="email_01.txt")
    assert pedido.peso_kg == pytest.approx(1250.5)


@pytest.mark.parametrize(
    ("op", "nf", "peso"),
    [("24518", "123456", 0), ("24518", "123456", -10.0), ("", "123456", 10.0),
     ("24518", "   ", 10.0)],
)  # fmt: skip
def test_pedido_invalido_levanta_value_error(op, nf, peso):
    with pytest.raises(ValueError):
        ex.Pedido(op=op, nf=nf, peso_kg=peso)


def test_resultado_sem_motivos_esta_aprovado():
    assert ex.ResultadoValidacao("24518", "PADRAO-A").aprovado is True


def test_resultado_com_motivo_esta_reprovado():
    resultado = ex.ResultadoValidacao("24519", "PADRAO-A", ["espessura 44.8 fora"])
    assert resultado.aprovado is False


def test_aprovado_acompanha_os_motivos():
    resultado = ex.ResultadoValidacao("24518", "PADRAO-A")
    resultado.motivos.append("cof 0.38 acima do máximo 0.35")
    assert resultado.aprovado is False, (
        "aprovado deve ser calculado a partir dos motivos (propriedade), não guardado"
    )
