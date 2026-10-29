import pytest

from _curso import carregar

ex = carregar(__file__, "ex04_media_args")


def test_media_de_dois_valores():
    assert ex.media(50.0, 52.0) == pytest.approx(51.0)


def test_media_de_um_valor():
    assert ex.media(7.5) == pytest.approx(7.5)


def test_media_desempacotando_uma_lista():
    medicoes = [49.2, 51.5, 50.1]
    assert ex.media(*medicoes) == pytest.approx(50.2666666)


def test_media_sem_valores_devolve_none():
    assert ex.media() is None


def test_maior_desvio():
    assert ex.maior_desvio(50.0, 49.2, 51.5, 50.1) == 1.5


def test_maior_desvio_negativo_conta_em_modulo():
    assert ex.maior_desvio(50.0, 47.3, 50.4) == 2.7, "Use abs(): 47.3 está 2.7 abaixo."


def test_maior_desvio_sem_medicoes():
    assert ex.maior_desvio(50.0) == 0.0
