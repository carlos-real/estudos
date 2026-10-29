from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex11_cli_relatorio")

CSV = """data;op;linha;ensaio;valor;resultado
01/10/2026;OP1;A;espessura;20,4;aprovado
01/10/2026;OP1;A;cof;0,21;aprovado
02/10/2026;OP2;C;espessura;44,0;reprovado
05/10/2026;OP3;A;espessura;20,1;aprovado
06/10/2026;OP4;C;espessura;40,0;aprovado
07/10/2026;OP5;A;espessura;19,8;aprovado
08/10/2026;OP6;B;espessura;25,0;aprovado
"""


@pytest.fixture
def arquivo(tmp_path):
    caminho = tmp_path / "ensaios.csv"
    caminho.write_text(CSV, encoding="utf-8")
    return caminho


def test_ler_registros_converte_tipos(arquivo):
    registros = ex.ler_registros(arquivo)
    assert len(registros) == 7
    primeiro = registros[0]
    assert primeiro["data"] == date(2026, 10, 1)
    assert primeiro["op"] == "OP1"
    assert primeiro["linha"] == "A"
    assert primeiro["ensaio"] == "espessura"
    assert primeiro["valor"] == pytest.approx(20.4), "Troque a vírgula decimal por ponto"


def test_ler_registros_arquivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        ex.ler_registros(tmp_path / "nao_existe.csv")


def test_parser_padroes_sem_variavel_de_ambiente(arquivo):
    args = ex.criar_parser({}).parse_args([str(arquivo)])
    assert args.arquivo == arquivo
    assert args.ensaio == "espessura"
    assert args.cv_max == pytest.approx(5.0)


def test_parser_cv_max_vem_do_ambiente(arquivo):
    args = ex.criar_parser({"LAB_CV_MAX": "3.5"}).parse_args([str(arquivo)])
    assert args.cv_max == pytest.approx(3.5)


def test_parser_argumento_vence_o_ambiente(arquivo):
    args = ex.criar_parser({"LAB_CV_MAX": "3.5"}).parse_args([str(arquivo), "--cv-max", "8"])
    assert args.cv_max == pytest.approx(8.0)


def test_parser_usa_os_environ_quando_ambiente_e_none(arquivo, monkeypatch):
    monkeypatch.setenv("LAB_CV_MAX", "2.5")
    args = ex.criar_parser().parse_args([str(arquivo)])
    assert args.cv_max == pytest.approx(2.5)


def test_main_relatorio_com_alerta(arquivo, capsys):
    codigo = ex.main([str(arquivo)], ambiente={})
    saida = capsys.readouterr().out.splitlines()
    assert saida == [
        "Linha A: n=3 média=20.10 desvio=0.30 CV=1.49%",
        "Linha B: n=1 média=25.00 desvio=0.00 CV=0.00%",
        "Linha C: n=2 média=42.00 desvio=2.83 CV=6.73% ALERTA",
    ]
    assert codigo == 1


def test_main_sem_alerta_devolve_zero(arquivo, capsys):
    codigo = ex.main([str(arquivo), "--cv-max", "10"], ambiente={})
    assert "ALERTA" not in capsys.readouterr().out
    assert codigo == 0


def test_main_outro_ensaio(arquivo, capsys):
    codigo = ex.main([str(arquivo), "--ensaio", "cof"], ambiente={})
    assert capsys.readouterr().out.splitlines() == [
        "Linha A: n=1 média=0.21 desvio=0.00 CV=0.00%"
    ]
    assert codigo == 0


def test_main_arquivo_inexistente(tmp_path, capsys):
    faltando = tmp_path / "faltando.csv"
    codigo = ex.main([str(faltando)], ambiente={})
    capturado = capsys.readouterr()
    assert codigo == 2
    assert "Arquivo não encontrado" in capturado.err, "Mensagens de erro vão para o stderr"
    assert capturado.out == ""


def test_main_ensaio_sem_registros(arquivo, capsys):
    codigo = ex.main([str(arquivo), "--ensaio", "tracao"], ambiente={})
    assert codigo == 2
    assert "Nenhum registro de tracao" in capsys.readouterr().err
