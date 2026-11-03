import csv

import pytest

from _curso import carregar

ex = carregar(__file__, "ex14_revisao_conferir_pasta")


@pytest.fixture
def pasta(tmp_path):
    laudos = tmp_path / "laudos"
    laudos.mkdir()
    (laudos / "linha_A.csv").write_bytes(
        "lote;espessura\r\nA-1;25,4\r\nA-2;28,0\r\n".encode("utf-8-sig")
    )
    (laudos / "linha_B.csv").write_bytes(b"lote;espessura\r\nB-1;22,5\r\nB-2;27,5\r\n")
    # Erro na 2ª linha de dados: a 1ª (C-1) NÃO pode ir para a saída.
    (laudos / "linha_C.csv").write_bytes(b"lote;espessura\r\nC-1;24,0\r\nC-2;2O,1\r\n")
    (laudos / "linha_D.csv").write_bytes(b"lote;gramatura\r\nD-1;32,0\r\n")
    (laudos / "linha_E.csv").write_bytes("lote;espessura\r\nE-ção;25,0\r\n".encode("cp1252"))
    (laudos / "leia-me.txt").write_text("não sou CSV", encoding="utf-8")
    return laudos


def ler_saida(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.reader(arquivo, delimiter=";"))


def test_contagem_de_aprovados_e_reprovados(pasta, tmp_path):
    resumo = ex.conferir_pasta(pasta, 22.5, 27.5, tmp_path / "resultado.csv")
    assert resumo["aprovados"] == 3
    assert resumo["reprovados"] == 1


def test_arquivos_com_erro_listados_sem_parar(pasta, tmp_path):
    resumo = ex.conferir_pasta(pasta, 22.5, 27.5, tmp_path / "resultado.csv")
    assert sorted(resumo["com_erro"]) == ["linha_C.csv", "linha_D.csv", "linha_E.csv"]
    assert all(isinstance(m, str) and m for m in resumo["com_erro"].values())


def test_saida_no_padrao_do_excel(pasta, tmp_path):
    saida = tmp_path / "resultado.csv"
    ex.conferir_pasta(pasta, 22.5, 27.5, saida)
    assert saida.read_bytes().startswith(b"\xef\xbb\xbf")
    assert ler_saida(saida) == [
        ["arquivo", "lote", "espessura", "status"],
        ["linha_A.csv", "A-1", "25,40", "APROVADO"],
        ["linha_A.csv", "A-2", "28,00", "REPROVADO"],
        ["linha_B.csv", "B-1", "22,50", "APROVADO"],
        ["linha_B.csv", "B-2", "27,50", "APROVADO"],
    ]


def test_arquivo_com_erro_nao_deixa_linhas_pela_metade(pasta, tmp_path):
    saida = tmp_path / "resultado.csv"
    ex.conferir_pasta(pasta, 22.5, 27.5, saida)
    lotes = [linha[1] for linha in ler_saida(saida)]
    assert "C-1" not in lotes, "O arquivo com erro deve ficar de fora INTEIRO."


def test_pasta_sem_csv(tmp_path):
    vazia = tmp_path / "vazia"
    vazia.mkdir()
    saida = tmp_path / "resultado.csv"
    resumo = ex.conferir_pasta(vazia, 22.5, 27.5, saida)
    assert resumo == {"aprovados": 0, "reprovados": 0, "com_erro": {}}
    assert ler_saida(saida) == [["arquivo", "lote", "espessura", "status"]]
