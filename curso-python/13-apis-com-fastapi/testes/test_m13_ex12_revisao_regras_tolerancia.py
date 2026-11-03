import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_regras_tolerancia")
cliente = TestClient(ex.app)

ESPESSURA_B = {"tipo": "nominal", "nominal": 40, "percentual": 5}
COF_FAIXA = {"tipo": "faixa", "minimo": 0.2, "maximo": 0.3}


@pytest.fixture(autouse=True)
def regras_vazias():
    ex.REGRAS.clear()
    yield
    ex.REGRAS.clear()


def gravar(linha, ensaio, corpo):
    resposta = cliente.put(f"/regras/{linha}/{ensaio}", json=corpo)
    assert resposta.status_code == 200, (
        f"PUT /regras deveria dar 200, deu {resposta.status_code}"
    )
    return resposta.json()


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        (20, 20.0),
        (0.25, 0.25),
        ("1.250,5", 1250.5),
        ("20,5", 20.5),
        ("20.5", 20.5),
        (" 7 ", 7.0),
    ],
)
def test_numero_br(entrada, esperado):
    assert ex.numero_br(entrada) == pytest.approx(esperado)


@pytest.mark.parametrize("entrada", ["abc", "", "1,2,3"])
def test_numero_br_invalido(entrada):
    with pytest.raises(ValueError):
        ex.numero_br(entrada)


def test_limites_faixa_e_nominal():
    assert ex.limites(ex.Regra(**COF_FAIXA)) == (0.2, 0.3)
    assert ex.limites(ex.Regra(**ESPESSURA_B)) == (38.0, 42.0)
    gramatura = ex.Regra(tipo="nominal", nominal=38, percentual=4)
    assert ex.limites(gramatura) == (36.48, 39.52)


@pytest.mark.parametrize(
    "dados",
    [
        {"tipo": "faixa", "minimo": 0.2},
        {"tipo": "faixa", "minimo": 0.4, "maximo": 0.3},
        {"tipo": "nominal", "nominal": 40},
        {"tipo": "nominal", "nominal": 0, "percentual": 5},
        {"tipo": "nominal", "nominal": 40, "percentual": 0},
        {"tipo": "nominal", "nominal": 40, "percentual": 150},
        {"tipo": "intervalo", "minimo": 1, "maximo": 2},
    ],
)
def test_regra_invalida(dados):
    with pytest.raises(ValidationError):
        ex.Regra(**dados)


def test_put_e_get_de_regra():
    assert gravar("B", "Espessura", ESPESSURA_B) == {
        "linha": "B",
        "ensaio": "espessura",
        "tipo": "nominal",
        "minimo": 38.0,
        "maximo": 42.0,
    }
    resposta = cliente.get("/regras/B/espessura")
    assert resposta.status_code == 200
    assert resposta.json()["maximo"] == 42.0


def test_get_sem_regra_e_linha_invalida():
    gravar("A", "cof", COF_FAIXA)
    resposta = cliente.get("/regras/A/espessura")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "Regra não cadastrada"}
    assert cliente.put("/regras/E/cof", json=COF_FAIXA).status_code == 422


def test_put_com_regra_inconsistente_da_422():
    gravar("A", "cof", COF_FAIXA)
    ruim = {"tipo": "faixa", "minimo": 0.5, "maximo": 0.1}
    assert cliente.put("/regras/A/cof", json=ruim).status_code == 422
    assert cliente.get("/regras/A/cof").json()["minimo"] == 0.2, "A regra antiga continua"


def test_lote_aprovado_com_valores_em_texto_brasileiro():
    gravar("B", "espessura", ESPESSURA_B)
    gravar("B", "cof", COF_FAIXA)
    lote = {
        "linha": "B",
        "medicoes": [
            {"ensaio": "Espessura", "valor": "41,2"},
            {"ensaio": "cof", "valor": 0.25},
        ],
    }
    resposta = cliente.post("/lotes/validar", json=lote)
    assert resposta.status_code == 200
    assert resposta.json() == {
        "linha": "B",
        "aprovado": True,
        "itens": [
            {
                "ensaio": "espessura",
                "valor": 41.2,
                "minimo": 38.0,
                "maximo": 42.0,
                "aprovado": True,
            },
            {"ensaio": "cof", "valor": 0.25, "minimo": 0.2, "maximo": 0.3, "aprovado": True},
        ],
        "sem_regra": [],
    }


def test_lote_reprovado_e_sem_regra():
    gravar("B", "espessura", ESPESSURA_B)
    lote = {
        "linha": "B",
        "medicoes": [
            {"ensaio": "gramatura", "valor": 37},
            {"ensaio": "espessura", "valor": "42,5"},
            {"ensaio": "selagem", "valor": 2},
        ],
    }
    dados = cliente.post("/lotes/validar", json=lote).json()
    assert dados["aprovado"] is False
    assert [i["aprovado"] for i in dados["itens"]] == [False]
    assert dados["sem_regra"] == ["gramatura", "selagem"]


def test_lote_so_com_item_sem_regra_nao_e_aprovado():
    gravar("A", "cof", COF_FAIXA)
    lote = {"linha": "A", "medicoes": [{"ensaio": "tracao", "valor": 30}]}
    dados = cliente.post("/lotes/validar", json=lote).json()
    assert dados["aprovado"] is False
    assert dados["itens"] == []


@pytest.mark.parametrize(
    "lote",
    [
        {"linha": "A", "medicoes": []},
        {"linha": "E", "medicoes": [{"ensaio": "cof", "valor": 0.2}]},
        {"linha": "A", "medicoes": [{"ensaio": "cof", "valor": "vinte"}]},
    ],
)
def test_lote_invalido_da_422(lote):
    gravar("A", "cof", COF_FAIXA)
    ok = {"linha": "A", "medicoes": [{"ensaio": "cof", "valor": "0,25"}]}
    assert cliente.post("/lotes/validar", json=ok).status_code == 200
    assert cliente.post("/lotes/validar", json=lote).status_code == 422
