import csv

import pytest

from _curso import carregar

ex = carregar(__file__, "ex08_escrever_csv_br")

LINHAS = [
    {"lote": "A-0153", "espessura": 25.4, "amostras": 3, "obs": "COF: liberado"},
    {"lote": "A-0154", "espessura": 1250.5, "amostras": 5, "obs": None},
]


def ler_de_volta(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.reader(arquivo, delimiter=";"))


def test_devolve_quantidade_de_linhas(tmp_path):
    assert ex.escrever_csv_br(tmp_path / "saida.csv", LINHAS) == 2


def test_conteudo_no_padrao_brasileiro(tmp_path):
    destino = tmp_path / "saida.csv"
    ex.escrever_csv_br(destino, LINHAS)
    assert ler_de_volta(destino) == [
        ["lote", "espessura", "amostras", "obs"],
        ["A-0153", "25,40", "3", "COF: liberado"],
        ["A-0154", "1250,50", "5", ""],
    ]


def test_arquivo_com_bom_e_ponto_e_virgula(tmp_path):
    destino = tmp_path / "saida.csv"
    ex.escrever_csv_br(destino, LINHAS)
    dados = destino.read_bytes()
    assert dados.startswith(b"\xef\xbb\xbf"), "Use encoding='utf-8-sig' (BOM para o Excel)."
    assert b"lote;espessura;amostras;obs" in dados


def test_sem_linhas_em_branco_entre_registros(tmp_path):
    destino = tmp_path / "saida.csv"
    ex.escrever_csv_br(destino, LINHAS)
    assert b"\r\r\n" not in destino.read_bytes(), "Abra o arquivo com newline=''."
    assert destino.read_bytes().count(b"\r\n") == 3


def test_casas_decimais_configuraveis(tmp_path):
    destino = tmp_path / "cof.csv"
    ex.escrever_csv_br(destino, [{"lote": "A", "cof": 0.2}], casas=3)
    assert ler_de_volta(destino)[1] == ["A", "0,200"]


def test_ponto_e_virgula_no_texto_vai_entre_aspas(tmp_path):
    destino = tmp_path / "obs.csv"
    ex.escrever_csv_br(destino, [{"lote": "A", "obs": "Selagem; refazer"}])
    assert ler_de_volta(destino)[1] == ["A", "Selagem; refazer"]


def test_lista_vazia_levanta_erro_e_nao_cria_arquivo(tmp_path):
    destino = tmp_path / "vazio.csv"
    with pytest.raises(ValueError, match="nada para gravar"):
        ex.escrever_csv_br(destino, [])
    assert not destino.exists()
