import pytest

from _curso import carregar

ex = carregar(__file__, "ex14_revisao_resumo_serie")


@pytest.mark.parametrize("texto", ["25,4", " 25.4 ", "25", "0", ",5", "1250.75"])
def test_eh_numero_aceita_numeros(texto):
    assert ex.eh_numero(texto) is True, f"eh_numero({texto!r}) deveria ser True."


@pytest.mark.parametrize(
    "texto", ["", "   ", "abc", "25,4,1", "25.4.1", ".", "-3", "1e3", "25 kg", "2 5"]
)
def test_eh_numero_rejeita_textos_invalidos(texto):
    assert ex.eh_numero(texto) is False, f"eh_numero({texto!r}) deveria ser False."


def test_serie_aprovada():
    resultado = ex.resumo_serie(["24,8", "25,3", "25,1"], 23, 27)
    assert resultado == (
        "válidas=3 | inválidas=0 | média=25.07 | mín=24.80 | máx=25.30 | fora=0 | APROVADO"
    )


def test_serie_reprovada_com_vazias_e_invalidas():
    leituras = ["24,8", "", "erro", "28,0", " 25.1 "]
    resultado = ex.resumo_serie(leituras, 23, 27)
    assert resultado == (
        "válidas=3 | inválidas=1 | média=25.97 | mín=24.80 | máx=28.00 | fora=1 | REPROVADO"
    ), f"Devolvido: {resultado!r}"


def test_serie_com_invalida_e_sem_fora_fica_para_revisar():
    resultado = ex.resumo_serie(["24,8", "abc", "25,0"], 23, 27)
    assert resultado == (
        "válidas=2 | inválidas=1 | média=24.90 | mín=24.80 | máx=25.00 | fora=0 | REVISAR"
    )


def test_limites_sao_inclusivos():
    resultado = ex.resumo_serie(["23", "27"], 23, 27)
    assert resultado.endswith("fora=0 | APROVADO"), f"Devolvido: {resultado!r}"


def test_sem_leituras():
    assert ex.resumo_serie([], 23, 27) == "Nenhuma leitura válida (inválidas=0)"


def test_so_vazias_e_invalidas():
    resultado = ex.resumo_serie(["", "x", "  ", "-1"], 23, 27)
    assert resultado == "Nenhuma leitura válida (inválidas=2)"
