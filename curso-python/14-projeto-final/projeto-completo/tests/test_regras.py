import pytest

from validador_certificados.modelos import (
    EspecificacaoDesconhecida,
    Pedido,
    ResultadoValidacao,
    Tolerancia,
)
from validador_certificados.regras import (
    escolher_especificacao,
    limites_nominal,
    validar_medicao,
    verificar_fixa,
    verificar_nominal,
)


# ----------------------------------------------------------------- modelos
@pytest.mark.parametrize(
    "argumentos",
    [
        {"tipo": "faixa"},
        {"tipo": "fixa"},
        {"tipo": "fixa", "minimo": 0.4, "maximo": 0.2},
        {"tipo": "nominal"},
        {"tipo": "nominal", "percentual": 0},
    ],
)
def test_tolerancia_invalida_levanta_value_error(argumentos):
    with pytest.raises(ValueError):
        Tolerancia("cof", **argumentos)


def test_pedido_com_peso_zero_e_invalido():
    with pytest.raises(ValueError):
        Pedido(op="24518", nf="123456", peso_kg=0)


def test_resultado_aprovado_quando_nao_ha_motivos():
    assert ResultadoValidacao("24518", "PADRAO-A").aprovado
    assert not ResultadoValidacao("24518", "PADRAO-A", ["cof alto"]).aprovado


# ----------------------------------------------------------------- tolerâncias
def test_fixa_dentro_e_nos_limites():
    assert verificar_fixa("cof", 0.22, 0.15, 0.35) is None
    assert verificar_fixa("cof", 0.15, 0.15, 0.35) is None
    assert verificar_fixa("cof", 0.35, 0.15, 0.35) is None


def test_fixa_mensagens():
    assert verificar_fixa("cof", 0.38, 0.15, 0.35) == "cof 0.38 acima do máximo 0.35"
    assert verificar_fixa("selagem", 7.6, 8.0, None) == "selagem 7.6 abaixo do mínimo 8"


def test_limites_nominal_sem_lixo_de_float():
    assert limites_nominal(30, 8) == (27.6, 32.4)
    assert limites_nominal(70.5, 7) == (65.565, 75.435)


def test_nominal_fora_da_faixa():
    esperado = "espessura 44.8 fora de 40 ± 10% (36 a 44)"
    assert verificar_nominal("espessura", 44.8, 40, 10) == esperado
    assert verificar_nominal("espessura", 44.0, 40, 10) is None


def test_validar_medicao_junta_todos_os_motivos(especificacoes, nova_medicao):
    medicao = nova_medicao(valores={"espessura": 44.8, "cof": 0.38}, nominais={})
    resultado = validar_medicao(medicao, especificacoes["PADRAO-A"])
    assert resultado.motivos == [
        "espessura sem valor nominal",
        "cof 0.38 acima do máximo 0.35",
        "selagem sem valor medido",
    ]
    assert not resultado.aprovado


# ----------------------------------------------------------------- especificação
def test_titulo_vazio_usa_padrao_da_linha(especificacoes):
    assert escolher_especificacao("  ", "A", especificacoes).titulo == "PADRAO-A"


def test_titulo_conhecido_herda_do_padrao(especificacoes):
    escolhida = escolher_especificacao(" esp-0412 ", "C", especificacoes)
    assert escolhida.titulo == "ESP-0412"
    assert escolhida.tolerancias["cof"].maximo == 0.25  # do cliente
    assert escolhida.tolerancias["espessura"].percentual == 8.0  # do padrão C
    assert especificacoes["PADRAO-C"].tolerancias["cof"].maximo == 0.30  # intacto


def test_titulo_desconhecido_nunca_vira_padrao(especificacoes):
    with pytest.raises(EspecificacaoDesconhecida, match="ESP-9999"):
        escolher_especificacao("ESP-9999", "A", especificacoes)


def test_linha_sem_padrao(especificacoes):
    with pytest.raises(EspecificacaoDesconhecida, match="linha B"):
        escolher_especificacao("", "B", especificacoes)
