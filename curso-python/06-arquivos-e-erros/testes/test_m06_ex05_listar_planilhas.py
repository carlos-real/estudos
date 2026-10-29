import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_listar_planilhas")


def criar(pasta, *nomes):
    for nome in nomes:
        (pasta / nome).write_text("x", encoding="utf-8")


def test_lista_so_planilhas_em_ordem(tmp_path):
    criar(tmp_path, "linha_B.xlsx", "linha_A.csv", "resumo.xlsm", "foto.pdf", "notas.txt")
    assert ex.listar_planilhas(tmp_path) == ["linha_A.csv", "linha_B.xlsx", "resumo.xlsm"]


def test_extensao_em_maiusculas_tambem_vale(tmp_path):
    criar(tmp_path, "linha_C.CSV", "linha_D.XLSX")
    assert ex.listar_planilhas(tmp_path) == ["linha_C.CSV", "linha_D.XLSX"]


def test_ignora_temporarios_do_excel(tmp_path):
    criar(tmp_path, "linha_A.xlsx", "~$linha_A.xlsx")
    assert ex.listar_planilhas(tmp_path) == ["linha_A.xlsx"]


def test_ignora_subpastas(tmp_path):
    criar(tmp_path, "linha_A.csv")
    (tmp_path / "antigos.csv").mkdir()
    (tmp_path / "2024").mkdir()
    criar(tmp_path / "2024", "linha_Z.csv")
    assert ex.listar_planilhas(tmp_path) == ["linha_A.csv"]


def test_pasta_vazia(tmp_path):
    assert ex.listar_planilhas(tmp_path) == []


def test_pasta_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="Pasta não encontrada"):
        ex.listar_planilhas(tmp_path / "nao_existe")
