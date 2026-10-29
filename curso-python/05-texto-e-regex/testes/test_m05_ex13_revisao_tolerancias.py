import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_tolerancias")

ESPECIFICACAO = """ESPECIFICAÇÃO ESPECIAL - CLIENTE PLASTIFORT
Espessura: 25 µm ± 10%
Gramatura: 23,0 g/m² +/- 5%
COF estático: 0,15 a 0,30
Tração MD: 30 a 45 MPa
"""


def test_le_todos_os_ensaios():
    tolerancias = ex.ler_tolerancias(ESPECIFICACAO)
    assert set(tolerancias) == {"espessura", "gramatura", "cof_estatico", "tracao_md"}


@pytest.mark.parametrize(
    ("chave", "minimo", "maximo"),
    [
        ("espessura", 22.5, 27.5),
        ("gramatura", 21.85, 24.15),
        ("cof_estatico", 0.15, 0.30),
        ("tracao_md", 30.0, 45.0),
    ],
)
def test_limites_calculados(chave, minimo, maximo):
    faixa = ex.ler_tolerancias(ESPECIFICACAO)[chave]
    assert faixa == (pytest.approx(minimo), pytest.approx(maximo))


def test_nominal_sem_unidade_e_numero_com_milhar():
    tolerancias = ex.ler_tolerancias("Peso da bobina: 1.200 ± 2,5%")
    assert tolerancias["peso_da_bobina"] == (pytest.approx(1170.0), pytest.approx(1230.0))


def test_linhas_fora_do_formato_sao_ignoradas():
    texto = "TÍTULO DA ESPECIFICAÇÃO\nObs: aplicar corona\n\nCOF dinâmico: 0,10 a 0,25"
    assert ex.ler_tolerancias(texto) == {"cof_dinamico": (0.10, 0.25)}


def test_texto_vazio():
    assert ex.ler_tolerancias("") == {}


def test_conferir_ok_fora_e_sem_medicao():
    medicoes = {"espessura": 26.1, "gramatura": 25.0, "cof_estatico": 0.22}
    assert ex.conferir(ESPECIFICACAO, medicoes) == {
        "espessura": "OK",
        "gramatura": "FORA",
        "cof_estatico": "OK",
        "tracao_md": "SEM MEDIÇÃO",
    }


@pytest.mark.parametrize("valor", [22.5, 27.5])
def test_conferir_limites_contam_como_dentro(valor):
    assert ex.conferir("Espessura: 25 µm ± 10%", {"espessura": valor}) == {"espessura": "OK"}


def test_conferir_ignora_medicoes_fora_da_especificacao():
    resultado = ex.conferir("COF estático: 0,15 a 0,30", {"cof_estatico": 0.4, "selagem": 9})
    assert resultado == {"cof_estatico": "FORA"}
