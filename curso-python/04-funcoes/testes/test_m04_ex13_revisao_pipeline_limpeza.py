import pytest

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_pipeline_limpeza")


def dobrar(x):
    return x * 2


def somar_um(x):
    return x + 1


def test_compor_aplica_da_esquerda_para_a_direita():
    assert ex.compor(dobrar, somar_um)(3) == 7, "dobrar primeiro (6), depois somar_um (7)."
    assert ex.compor(somar_um, dobrar)(3) == 8


def test_compor_tres_funcoes():
    assert ex.compor(somar_um, somar_um, dobrar)(1) == 6


def test_compor_uma_funcao_so():
    assert ex.compor(dobrar)(21) == 42


@pytest.mark.parametrize("valor", [5, "texto", [1, 2]])
def test_compor_sem_funcoes_e_identidade(valor):
    assert ex.compor()(valor) == valor


def test_compor_devolve_funcao_reutilizavel():
    pipeline = ex.compor(dobrar, somar_um)
    assert callable(pipeline)
    assert [pipeline(x) for x in (0, 1, 2)] == [1, 3, 5]


def test_compor_com_metodos_de_string():
    assert ex.compor(str.strip, str.upper)("  op-1 ") == "OP-1"


def test_trocar_espacos_por_hifen():
    assert ex.trocar_espacos_por_hifen("OP 4512") == "OP-4512"
    assert ex.trocar_espacos_por_hifen("sem") == "sem"


def test_limpar_codigos():
    codigos = [" op 4512", "OP-4512", "", "op-4513 ", "   ", "Op 4514"]
    assert ex.limpar_codigos(codigos) == ["OP-4512", "OP-4513", "OP-4514"]


def test_limpar_codigos_mantem_ordem_da_primeira_aparicao():
    assert ex.limpar_codigos(["op-9", "OP-1", "OP 9"]) == ["OP-9", "OP-1"]


def test_limpar_codigos_nao_altera_a_lista():
    codigos = [" op-1 ", "op-1"]
    ex.limpar_codigos(codigos)
    assert codigos == [" op-1 ", "op-1"]


def test_limpar_lista_vazia():
    assert ex.limpar_codigos([]) == []
