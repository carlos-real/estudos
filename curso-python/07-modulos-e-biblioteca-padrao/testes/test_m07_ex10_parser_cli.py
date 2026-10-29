import argparse
from datetime import date

import pytest

from _curso import carregar

ex = carregar(__file__, "ex10_parser_cli")


def test_data_br_valida():
    assert ex.data_br("01/10/2026") == date(2026, 10, 1)


@pytest.mark.parametrize("texto", ["2026-10-01", "32/10/2026", "amanhã"])
def test_data_br_invalida_gera_argument_type_error(texto):
    with pytest.raises(argparse.ArgumentTypeError, match="dd/mm/aaaa"):
        ex.data_br(texto)


def test_parser_e_do_argparse_com_prog_validador():
    parser = ex.criar_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.prog == "validador"


def test_valores_padrao():
    args = ex.criar_parser().parse_args(["valores.xlsx"])
    assert args.planilha == "valores.xlsx"
    assert args.linha is None
    assert args.tolerancia == pytest.approx(5.0)
    assert args.desde is None
    assert args.verbose is False


def test_todas_as_opcoes():
    args = ex.criar_parser().parse_args(
        ["dados.xlsx", "--linha", "C", "--tolerancia", "7.5", "--desde", "01/10/2026", "-v"]
    )
    assert args.planilha == "dados.xlsx"
    assert args.linha == "C"
    assert args.tolerancia == pytest.approx(7.5)
    assert args.desde == date(2026, 10, 1)
    assert args.verbose is True


def test_verbose_forma_longa_e_linha_minuscula():
    args = ex.criar_parser().parse_args(["x.xlsx", "--verbose", "--linha", "d"])
    assert args.verbose is True
    assert args.linha == "D", "Use type=str.upper para aceitar letra minúscula"


@pytest.mark.parametrize(
    "argv",
    [
        [],  # falta a planilha
        ["x.xlsx", "--linha", "E"],  # linha inexistente
        ["x.xlsx", "--tolerancia", "muito"],  # não é número
    ],
)
def test_argumentos_invalidos_encerram_com_codigo_2(argv, capsys):
    parser = ex.criar_parser()
    with pytest.raises(SystemExit) as erro:
        parser.parse_args(argv)
    assert erro.value.code == 2
    assert "usage" in capsys.readouterr().err


def test_data_invalida_mostra_mensagem_amigavel(capsys):
    parser = ex.criar_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["x.xlsx", "--desde", "2026-10-01"])
    assert "dd/mm/aaaa" in capsys.readouterr().err
