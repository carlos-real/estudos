from pathlib import Path

import pytest

from _curso import carregar

ex = carregar(__file__, "ex14_cli")


@pytest.fixture
def arquivos(tmp_path):
    """Cria planilha, banco e pasta de e-mails falsos (só precisam existir)."""
    planilha = tmp_path / "valores.xlsx"
    regras = tmp_path / "regras.db"
    emails = tmp_path / "emails"
    planilha.write_bytes(b"")
    regras.write_bytes(b"")
    emails.mkdir()
    return planilha, regras, emails


def argumentos(planilha, regras, emails, *extras):
    return ["--planilha", str(planilha), "--regras", str(regras), "--emails", str(emails),
            *extras]  # fmt: skip


class ExecutarFalso:
    """Finge ser a série: guarda os argumentos recebidos e devolve um resumo."""

    def __init__(self, resumo=None):
        self.resumo = {"bloqueado": 4, "ensaio": 2} if resumo is None else resumo
        self.chamadas = []

    def __call__(self, **kwargs):
        self.chamadas.append(kwargs)
        return self.resumo


def test_parser_valores_padrao():
    args = ex.criar_parser().parse_args(
        ["--planilha", "v.xlsx", "--regras", "r.db", "--emails", "emails"]
    )
    assert args.planilha == Path("v.xlsx")
    assert args.regras == Path("r.db")
    assert args.emails == Path("emails")
    assert args.saida == Path("saida")
    assert args.emitir is False
    assert args.verbose is False


def test_parser_opcoes():
    args = ex.criar_parser().parse_args(
        ["--planilha", "v.xlsx", "--regras", "r.db", "--emails", "e", "--saida", "s",
         "--emitir", "-v"]
    )  # fmt: skip
    assert (args.saida, args.emitir, args.verbose) == (Path("s"), True, True)
    assert ex.criar_parser().prog == "validador"


def test_argumento_obrigatorio_faltando():
    with pytest.raises(SystemExit) as saida:
        ex.criar_parser().parse_args(["--planilha", "v.xlsx"])
    assert saida.value.code == 2


def test_main_chama_executar_em_modo_ensaio(arquivos, capsys):
    falso = ExecutarFalso()
    codigo = ex.main(argumentos(*arquivos), executar=falso)
    assert codigo == 0
    planilha, regras, emails = arquivos
    assert falso.chamadas == [
        {"planilha": planilha, "regras": regras, "emails": emails,
         "saida": Path("saida"), "ensaio": True}
    ]  # fmt: skip
    assert capsys.readouterr().out.splitlines() == ["Modo: ENSAIO", "bloqueado: 4", "ensaio: 2"]


def test_main_com_emitir(arquivos, capsys):
    falso = ExecutarFalso({"emitido": 3})
    assert ex.main(argumentos(*arquivos, "--emitir"), executar=falso) == 0
    assert falso.chamadas[0]["ensaio"] is False
    assert capsys.readouterr().out.splitlines() == ["Modo: REAL", "emitido: 3"]


def test_main_devolve_1_quando_ha_falha(arquivos):
    falso = ExecutarFalso({"emitido": 2, "falha": 1})
    assert ex.main(argumentos(*arquivos, "--emitir"), executar=falso) == 1


def test_main_falha_zero_nao_e_falha(arquivos):
    assert ex.main(argumentos(*arquivos), executar=ExecutarFalso({"ensaio": 1, "falha": 0})) == 0


def test_planilha_inexistente(arquivos, tmp_path, capsys):
    _, regras, emails = arquivos
    falso = ExecutarFalso()
    codigo = ex.main(argumentos(tmp_path / "nao.xlsx", regras, emails), executar=falso)
    assert codigo == 1
    assert falso.chamadas == [], "não chame executar se faltar arquivo"
    erro = capsys.readouterr().err
    assert "Erro: planilha não encontrada" in erro
    assert "nao.xlsx" in erro


def test_banco_inexistente(arquivos, tmp_path, capsys):
    planilha, _, emails = arquivos
    assert ex.main(argumentos(planilha, tmp_path / "x.db", emails), executar=ExecutarFalso()) == 1
    assert "Erro: banco de regras não encontrado" in capsys.readouterr().err


def test_emails_precisa_ser_pasta(arquivos, capsys):
    planilha, regras, _ = arquivos
    assert ex.main(argumentos(planilha, regras, planilha), executar=ExecutarFalso()) == 1
    assert "Erro: pasta de e-mails não encontrada" in capsys.readouterr().err
