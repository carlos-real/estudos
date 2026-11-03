import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_listar_planilhas")


def criar(pasta, *nomes):
    for nome in nomes:
        (pasta / nome).write_bytes(b"conteudo")


def test_lista_so_planilhas_em_ordem(tmp_path):
    criar(tmp_path, "Linha_B.xlsx", "linha_a.xlsx", "laudo.pdf", "notas.txt")
    assert ex.listar_planilhas(tmp_path) == ["linha_a.xlsx", "Linha_B.xlsx"]


def test_aceita_xlsm_e_extensao_maiuscula(tmp_path):
    criar(tmp_path, "RESUMO.XLSX", "macro.xlsm", "antigo.xls", "dados.csv")
    assert ex.listar_planilhas(tmp_path) == ["macro.xlsm", "RESUMO.XLSX"]


def test_ignora_arquivos_de_trava_do_excel(tmp_path):
    criar(tmp_path, "linha_c.xlsx", "~$linha_c.xlsx")
    assert ex.listar_planilhas(tmp_path) == ["linha_c.xlsx"], (
        "Arquivos que começam com ~$ são travas do Excel, não planilhas"
    )


def test_ignora_pastas_e_subpastas(tmp_path):
    criar(tmp_path, "linha_d.xlsx")
    (tmp_path / "backup.xlsx").mkdir()  # uma PASTA com nome de planilha
    sub = tmp_path / "2025"
    sub.mkdir()
    criar(sub, "antiga.xlsx")
    assert ex.listar_planilhas(tmp_path) == ["linha_d.xlsx"]


def test_pasta_sem_planilhas_devolve_lista_vazia(tmp_path):
    criar(tmp_path, "leia-me.txt")
    assert ex.listar_planilhas(tmp_path) == []


def test_pasta_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.listar_planilhas(tmp_path / "nao_existe")
