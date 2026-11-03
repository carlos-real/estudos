import pytest

from _curso import carregar

ex = carregar(__file__, "ex12_revisao_testes_lotes")


# ---- A versão correta de dividir_em_lotes ------------------------------------
def dividir_correta(itens, tamanho):
    if tamanho < 1:
        raise ValueError("tamanho deve ser pelo menos 1")
    return [itens[i : i + tamanho] for i in range(0, len(itens), tamanho)]


# ---- Versões com bug: cada uma deve ser reprovada pelos seus testes ----------
def perde_a_sobra(itens, tamanho):
    """uma versão que descarta o último lote quando ele está incompleto"""
    if tamanho < 1:
        raise ValueError("tamanho deve ser pelo menos 1")
    lotes = []
    atual = []
    for item in itens:
        atual.append(item)
        if len(atual) == tamanho:
            lotes.append(atual)
            atual = []
    return lotes


def lote_vazio_no_final(itens, tamanho):
    """uma versão que acrescenta um lote vazio [] quando a divisão é exata"""
    if tamanho < 1:
        raise ValueError("tamanho deve ser pelo menos 1")
    lotes = [itens[i : i + tamanho] for i in range(0, len(itens), tamanho)]
    if len(itens) % tamanho == 0:
        lotes.append([])
    return lotes


def aceita_tamanho_invalido(itens, tamanho):
    """uma versão que devolve [] em vez de levantar ValueError para tamanho < 1"""
    if tamanho < 1:
        return []
    return [itens[i : i + tamanho] for i in range(0, len(itens), tamanho)]


def esvazia_a_lista_original(itens, tamanho):
    """uma versão que dá o resultado certo, mas ESVAZIA a lista recebida (pop)"""
    if tamanho < 1:
        raise ValueError("tamanho deve ser pelo menos 1")
    lotes = []
    while itens:
        lote = []
        while itens and len(lote) < tamanho:
            lote.append(itens.pop(0))
        lotes.append(lote)
    return lotes


def _seus_testes_reprovam(funcao) -> bool:
    """True se a função de testes do aluno acusou erro (assert ou pytest.raises)."""
    try:
        ex.testar_dividir_em_lotes(funcao)
    except (AssertionError, pytest.fail.Exception):
        return True
    return False


def test_seus_testes_aprovam_a_versao_correta():
    try:
        ex.testar_dividir_em_lotes(dividir_correta)
    except AssertionError as erro:
        pytest.fail(
            "Seus testes reprovaram a versão CORRETA de dividir_em_lotes. "
            f"Confira os valores esperados nos seus asserts. Detalhe: {erro}"
        )


@pytest.mark.parametrize(
    "versao_com_bug",
    [perde_a_sobra, lote_vazio_no_final, aceita_tamanho_invalido, esvazia_a_lista_original],
    ids=["perde-a-sobra", "lote-vazio-no-final", "tamanho-invalido", "altera-a-entrada"],
)
def test_seus_testes_reprovam_versao_com_bug(versao_com_bug):
    assert _seus_testes_reprovam(versao_com_bug), (
        f"Seus testes deixaram passar {versao_com_bug.__doc__}. "
        "Acrescente um caso que pegue esse defeito."
    )
