import pytest

from _curso import carregar

ex = carregar(__file__, "ex01_situacao_aluno")


@pytest.mark.parametrize(
    ("media", "esperado"),
    [
        (9.5, "Aprovado"),
        (7.0, "Aprovado"),
        (10, "Aprovado"),
        (6.99, "Recuperação"),
        (5.0, "Recuperação"),
        (4.99, "Reprovado"),
        (0, "Reprovado"),
    ],
)
def test_faixas_de_nota(media, esperado):
    resultado = ex.situacao(media)
    assert resultado == esperado, f"situacao({media}) devolveu {resultado!r}."


@pytest.mark.parametrize("media", [-0.5, -10, 10.1, 11])
def test_nota_fora_de_0_a_10_e_invalida(media):
    assert ex.situacao(media) == "Nota inválida"


def test_nota_alta_nao_cai_em_recuperacao():
    resultado = ex.situacao(9)
    assert resultado == "Aprovado", (
        f"situacao(9) devolveu {resultado!r}. "
        "Confira a ORDEM dos elif: teste >= 7 antes de >= 5."
    )
