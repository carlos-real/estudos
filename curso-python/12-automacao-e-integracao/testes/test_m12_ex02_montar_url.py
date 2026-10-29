import pytest

from _curso import carregar

ex = carregar(__file__, "ex02_montar_url")

BASE = "https://api.lab.local"


@pytest.mark.parametrize(
    ("base", "caminho"),
    [
        ("https://api.lab.local", "medicoes"),
        ("https://api.lab.local/", "medicoes"),
        ("https://api.lab.local", "/medicoes"),
        ("https://api.lab.local/", "/medicoes"),
    ],
)
def test_sempre_uma_barra_entre_base_e_caminho(base, caminho):
    assert ex.montar_url(base, caminho) == "https://api.lab.local/medicoes"


def test_caminho_com_varios_niveis():
    assert ex.montar_url(BASE + "/", "/linhas/A/tolerancias") == (
        "https://api.lab.local/linhas/A/tolerancias"
    )


def test_parametros_na_ordem_do_dicionario():
    url = ex.montar_url(BASE, "medicoes", {"linha": "A", "ensaio": "cof", "limite": 10})
    assert url == "https://api.lab.local/medicoes?linha=A&ensaio=cof&limite=10"


def test_valores_none_sao_ignorados():
    url = ex.montar_url(BASE, "medicoes", {"linha": None, "op": "123456", "nf": None})
    assert url == "https://api.lab.local/medicoes?op=123456"


def test_sem_parametros_restantes_nao_tem_interrogacao():
    assert ex.montar_url(BASE, "medicoes", {"linha": None}) == "https://api.lab.local/medicoes"
    assert ex.montar_url(BASE, "medicoes", {}) == "https://api.lab.local/medicoes"


def test_espacos_e_acentos_sao_codificados():
    url = ex.montar_url(BASE, "busca", {"texto": "filme PE", "ensaio": "tração"})
    assert url == "https://api.lab.local/busca?texto=filme+PE&ensaio=tra%C3%A7%C3%A3o"
