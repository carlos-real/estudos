import random

import pytest

from _curso import carregar

ex = carregar(__file__, "ex06_sorteio_amostras")

BOBINAS = [f"B{n:02d}" for n in range(1, 21)]


def test_sorteio_igual_ao_do_random_com_semente():
    esperado = random.Random(42).sample(BOBINAS, 3)
    assert ex.sortear_bobinas(BOBINAS, 3, semente=42) == esperado


def test_mesma_semente_mesmo_sorteio():
    primeiro = ex.sortear_bobinas(BOBINAS, 5, semente=7)
    segundo = ex.sortear_bobinas(BOBINAS, 5, semente=7)
    assert primeiro == segundo


def test_sorteio_sem_repeticao_e_da_populacao():
    sorteadas = ex.sortear_bobinas(BOBINAS, 20, semente=3)
    assert sorted(sorteadas) == BOBINAS


def test_sorteio_zero_bobinas():
    assert ex.sortear_bobinas(BOBINAS, 0, semente=1) == []


@pytest.mark.parametrize("quantidade", [21, -1])
def test_quantidade_invalida_gera_value_error(quantidade):
    with pytest.raises(ValueError):
        ex.sortear_bobinas(BOBINAS, quantidade, semente=1)


def test_sorteio_nao_altera_a_lista_original():
    copia = list(BOBINAS)
    ex.sortear_bobinas(copia, 5, semente=1)
    assert copia == BOBINAS


def esperado_por_linha(dados, por_linha, semente):
    gerador = random.Random(semente)
    return {
        linha: gerador.sample(dados[linha], min(por_linha, len(dados[linha])))
        for linha in sorted(dados)
    }


DADOS_LINHAS = {
    "C": ["C1", "C2", "C3", "C4"],
    "A": ["A1", "A2", "A3", "A4", "A5"],
    "B": ["B1"],
}


def test_sortear_por_linha_segue_as_regras():
    resultado = ex.sortear_por_linha(DADOS_LINHAS, 2, semente=11)
    assert resultado == esperado_por_linha(DADOS_LINHAS, 2, 11)


def test_sortear_por_linha_ordem_alfabetica_e_linha_pequena():
    resultado = ex.sortear_por_linha(DADOS_LINHAS, 3, semente=5)
    assert list(resultado) == ["A", "B", "C"]
    assert resultado["B"] == ["B1"], "Linha com menos bobinas: sorteie todas que houver"
    assert all(len(v) == 3 for k, v in resultado.items() if k != "B")


def test_embaralhar_ordem_com_semente():
    amostras = ["AM1", "AM2", "AM3", "AM4", "AM5", "AM6"]
    esperado = list(amostras)
    random.Random(99).shuffle(esperado)
    assert ex.embaralhar_ordem(amostras, semente=99) == esperado


def test_embaralhar_ordem_nao_altera_original():
    amostras = ["AM1", "AM2", "AM3", "AM4", "AM5", "AM6"]
    resultado = ex.embaralhar_ordem(amostras, semente=1)
    assert amostras == ["AM1", "AM2", "AM3", "AM4", "AM5", "AM6"]
    assert resultado is not amostras
    assert sorted(resultado) == amostras
