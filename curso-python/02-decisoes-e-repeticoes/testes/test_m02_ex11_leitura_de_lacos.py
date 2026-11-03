import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_leitura_de_lacos")

DICA = "Faça o teste de mesa (anote as variáveis a cada volta) e confira no REPL."


def test_previsao_trecho_a():
    assert ex.previsao_a() == 12, f"Trecho A: quais números range(1, 10, 3) gera? {DICA}"


def test_previsao_trecho_b():
    assert ex.previsao_b() == 4, (
        f"Trecho B: quantas vezes o while roda até n chegar a 1? {DICA}"
    )


def test_previsao_trecho_c():
    assert ex.previsao_c() == "BBN", f"Trecho C: o continue pula as vogais. {DICA}"


def test_previsao_trecho_d():
    assert ex.previsao_d() == 3, f"Trecho D: o break para no PRIMEIRO valor < 23. {DICA}"


@pytest.mark.parametrize(
    ("notas", "esperado"),
    [
        ([8, 6, 9], 8.5),
        ([7], 7.0),
        ([10, 7, 6.9], 8.5),
        ([7, 7, 7, 10], 7.75),
    ],
)
def test_media_aprovadas(notas, esperado):
    resultado = ex.media_aprovadas(notas)
    assert resultado == pytest.approx(esperado), (
        f"media_aprovadas({notas}) devolveu {resultado!r}; esperado {esperado}. "
        "Os acumuladores estão sendo zerados dentro do laço?"
    )


@pytest.mark.parametrize("notas", [[5, 6], []])
def test_sem_aprovados_devolve_zero(notas):
    assert ex.media_aprovadas(notas) == 0.0, (
        "Sem aprovados, devolva 0.0 (não divida por zero)."
    )
