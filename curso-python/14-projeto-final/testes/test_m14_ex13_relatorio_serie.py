import csv

from _curso import carregar

ex = carregar(__file__, "ex13_relatorio_serie")

ITENS = [
    ex.ItemFila("24518", "123456", 1250.5, "ensaio", "PADRAO-A", [], "ENSAIO-24518-123456"),
    ex.ItemFila(
        "24519", "123457", 980.0, "bloqueado", "PADRAO-A", ["espessura alta", "COF sem lib."]
    ),
    ex.ItemFila("24533", "123801", 860.4, "bloqueado", "", ["linha divergente"]),
]


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.reader(arquivo, delimiter=";"))


def test_resumir_conta_por_situacao():
    assert ex.resumir(ITENS) == {"bloqueado": 2, "ensaio": 1}


def test_resumir_em_ordem_alfabetica():
    itens = [ex.ItemFila("1", "1", 1.0, s) for s in ["falha", "ensaio", "bloqueado", "ensaio"]]
    assert list(ex.resumir(itens).items()) == [("bloqueado", 1), ("ensaio", 2), ("falha", 1)]


def test_resumir_lista_vazia():
    assert ex.resumir([]) == {}


def test_csv_cabecalho_e_linhas(tmp_path):
    caminho = ex.escrever_relatorio_csv(ITENS, tmp_path / "serie.csv")
    assert caminho == tmp_path / "serie.csv"
    linhas = ler_csv(caminho)
    assert linhas[0] == ex.COLUNAS
    assert linhas[1] == [
        "24518",
        "123456",
        "1250,50",
        "PADRAO-A",
        "ENSAIO",
        "",
        "ENSAIO-24518-123456",
    ]
    assert linhas[2][4:6] == ["BLOQUEADO", "espessura alta | COF sem lib."]
    assert linhas[3][2] == "860,40"
    assert len(linhas) == 4


def test_csv_tem_bom_para_o_excel(tmp_path):
    caminho = ex.escrever_relatorio_csv(ITENS, tmp_path / "serie.csv")
    assert caminho.read_bytes().startswith(b"\xef\xbb\xbf"), "use encoding='utf-8-sig'"


def test_csv_cria_a_pasta(tmp_path):
    caminho = ex.escrever_relatorio_csv([], tmp_path / "saida" / "2026-10" / "serie.csv")
    assert caminho.exists()
    assert ler_csv(caminho) == [ex.COLUNAS]


def test_csv_sem_linhas_em_branco(tmp_path):
    caminho = ex.escrever_relatorio_csv(ITENS, tmp_path / "serie.csv")
    texto = caminho.read_text(encoding="utf-8-sig")
    assert "\n\n" not in texto and "\r\r" not in texto, "abra o arquivo com newline=''"
