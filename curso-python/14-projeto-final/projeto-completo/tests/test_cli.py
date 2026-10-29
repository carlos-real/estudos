"""Testes de ponta a ponta: a CLI rodando sobre os dados de exemplo."""

import pytest

from validador_certificados import cli, serie
from validador_certificados.emissao import Emissor


def argumentos(pasta_dados, saida, *extras):
    return [
        "--planilha",
        str(pasta_dados / "planilha_valores.xlsx"),
        "--regras",
        str(pasta_dados / "regras.db"),
        "--emails",
        str(pasta_dados / "emails"),
        "--saida",
        str(saida),
        *extras,
    ]


def test_serie_de_exemplo_em_modo_ensaio(pasta_dados, tmp_path, capsys):
    codigo = cli.main(argumentos(pasta_dados, tmp_path))
    saida = capsys.readouterr()
    assert codigo == 0
    assert "modo ENSAIO" in saida.out
    assert "bloqueado                 4" in saida.out
    assert "ensaio                    2" in saida.out
    assert "e-mails fora do padrão    2" in saida.out
    assert "OP 24533 bloqueada: linha informada C diferente da aba Linha B" in saida.err
    assert len(list(tmp_path.glob("relatorio_*.xlsx"))) == 1
    assert len(list(tmp_path.glob("relatorio_*.csv"))) == 1
    assert "ENSAIO: emitiria certificado: OP 24518" in (tmp_path / "validador.log").read_text(
        encoding="utf-8"
    )
    assert not (tmp_path / "emitidos.csv").exists(), "ensaio não grava histórico"


def test_arquivo_inexistente_devolve_1(pasta_dados, tmp_path, capsys):
    args = argumentos(pasta_dados, tmp_path)
    args[1] = str(tmp_path / "nao_existe.xlsx")
    assert cli.main(args) == 1
    assert "planilha não encontrada" in capsys.readouterr().err


def test_emitir_de_verdade_ainda_indisponivel(pasta_dados, tmp_path, capsys):
    assert cli.main(argumentos(pasta_dados, tmp_path, "--emitir")) == 1
    assert "ainda não implementada" in capsys.readouterr().err


def test_argumento_obrigatorio_faltando(capsys):
    with pytest.raises(SystemExit) as saida:
        cli.main(["--planilha", "x.xlsx"])
    assert saida.value.code == 2


def test_modo_real_grava_historico_e_nao_repete(pasta_dados, tmp_path):
    class EmissorReal(Emissor):
        def emitir(self, item):
            return f"CQ-{item.op}"

    primeira = serie.executar_serie(
        pasta_dados / "planilha_valores.xlsx",
        pasta_dados / "regras.db",
        pasta_dados / "emails",
        tmp_path,
        EmissorReal(),
    )
    assert primeira.contagem == {"bloqueado": 4, "emitido": 2}
    segunda = serie.executar_serie(
        pasta_dados / "planilha_valores.xlsx",
        pasta_dados / "regras.db",
        pasta_dados / "emails",
        tmp_path,
        EmissorReal(),
    )
    assert segunda.contagem == {"bloqueado": 4, "ignorado": 2}
