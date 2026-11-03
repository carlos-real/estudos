import pytest

from _curso import carregar

ex = carregar(__file__, "ex07_testes_classificar")


# ---- A versão correta de classificar -----------------------------------------
def classificar_correta(valor, minimo, maximo):
    if minimo > maximo:
        raise ValueError("mínimo maior que o máximo")
    if valor < minimo:
        return "ABAIXO"
    if valor > maximo:
        return "ACIMA"
    return "OK"


# ---- Versões com bug: cada uma deve ser reprovada pelos seus testes ----------
def borda_minima_fora(valor, minimo, maximo):
    """uma versão que considera o valor igual ao MÍNIMO como fora (usa <=)"""
    if minimo > maximo:
        raise ValueError("mínimo maior que o máximo")
    if valor <= minimo:
        return "ABAIXO"
    if valor > maximo:
        return "ACIMA"
    return "OK"


def borda_maxima_fora(valor, minimo, maximo):
    """uma versão que considera o valor igual ao MÁXIMO como fora (usa >=)"""
    if minimo > maximo:
        raise ValueError("mínimo maior que o máximo")
    if valor < minimo:
        return "ABAIXO"
    if valor >= maximo:
        return "ACIMA"
    return "OK"


def rotulos_trocados(valor, minimo, maximo):
    """uma versão que troca os rótulos ABAIXO e ACIMA"""
    if minimo > maximo:
        raise ValueError("mínimo maior que o máximo")
    if valor < minimo:
        return "ACIMA"
    if valor > maximo:
        return "ABAIXO"
    return "OK"


def sem_validar_tolerancia(valor, minimo, maximo):
    """uma versão que NÃO levanta ValueError quando mínimo > máximo"""
    if valor < minimo:
        return "ABAIXO"
    if valor > maximo:
        return "ACIMA"
    return "OK"


def _seus_testes_reprovam(funcao) -> bool:
    """True se a função de testes do aluno acusou erro (assert ou pytest.raises)."""
    try:
        ex.testar_classificar(funcao)
    except (AssertionError, pytest.fail.Exception):
        return True
    return False


def test_seus_testes_aprovam_a_versao_correta():
    try:
        ex.testar_classificar(classificar_correta)
    except AssertionError as erro:
        pytest.fail(
            "Seus testes reprovaram a versão CORRETA de classificar. "
            f"Confira os valores esperados nos seus asserts. Detalhe: {erro}"
        )


@pytest.mark.parametrize(
    "versao_com_bug",
    [borda_minima_fora, borda_maxima_fora, rotulos_trocados, sem_validar_tolerancia],
    ids=["borda-minima", "borda-maxima", "rotulos-trocados", "sem-validacao"],
)
def test_seus_testes_reprovam_versao_com_bug(versao_com_bug):
    assert _seus_testes_reprovam(versao_com_bug), (
        f"Seus testes deixaram passar {versao_com_bug.__doc__}. "
        "Acrescente um caso que pegue esse defeito."
    )
