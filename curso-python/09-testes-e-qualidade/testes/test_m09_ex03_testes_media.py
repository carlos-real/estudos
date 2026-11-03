import pytest

from _curso import carregar

ex = carregar(__file__, "ex03_testes_media")


# ---- A versão correta de calcular_media --------------------------------------
def media_correta(valores):
    if not valores:
        raise ValueError("lista vazia")
    return sum(valores) / len(valores)


# ---- Versões com bug: cada uma deve ser reprovada pelos seus testes ----------
def media_com_divisao_inteira(valores):
    """uma versão que usa divisão inteira (//) e perde as casas decimais"""
    if not valores:
        raise ValueError("lista vazia")
    return sum(valores) // len(valores)


def media_que_ignora_o_sinal(valores):
    """uma versão que trata valores negativos como positivos"""
    if not valores:
        raise ValueError("lista vazia")
    return sum(abs(valor) for valor in valores) / len(valores)


def media_que_aceita_lista_vazia(valores):
    """uma versão que devolve 0.0 para lista vazia em vez de levantar ValueError"""
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


def _seus_testes_reprovam(funcao) -> bool:
    """True se a função de testes do aluno acusou erro (assert ou pytest.raises)."""
    try:
        ex.testar_calcular_media(funcao)
    except (AssertionError, pytest.fail.Exception):
        return True
    return False


def test_seus_testes_aprovam_a_versao_correta():
    try:
        ex.testar_calcular_media(media_correta)
    except AssertionError as erro:
        pytest.fail(
            "Seus testes reprovaram a versão CORRETA de calcular_media. "
            f"Confira os valores esperados nos seus asserts. Detalhe: {erro}"
        )


@pytest.mark.parametrize(
    "versao_com_bug",
    [media_com_divisao_inteira, media_que_ignora_o_sinal, media_que_aceita_lista_vazia],
    ids=["divisao-inteira", "ignora-sinal", "aceita-lista-vazia"],
)
def test_seus_testes_reprovam_versao_com_bug(versao_com_bug):
    assert _seus_testes_reprovam(versao_com_bug), (
        f"Seus testes deixaram passar {versao_com_bug.__doc__}. "
        "Acrescente um caso que pegue esse defeito."
    )
