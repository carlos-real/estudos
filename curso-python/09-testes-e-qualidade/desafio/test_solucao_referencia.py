"""Testes da solução de referência do desafio.

Rode (na pasta curso-python):
    python -m pytest 09-testes-e-qualidade/desafio -v
"""

import logging

import pytest
import solucao_referencia as ref
from solucao_referencia import FORA, LIBERADO, OK, SEM_REGRA, Medicao

LIMITES_TESTE = {("A", "espessura"): (19.0, 21.0), ("A", "cof"): (0.20, 0.35)}


@pytest.fixture
def csv_exemplo(tmp_path):
    """Um CSV pequeno, no formato da planilha, numa pasta temporária."""
    caminho = tmp_path / "medicoes.csv"
    caminho.write_text(
        "op;linha;ensaio;valor;observacao\n"
        "100;a;Espessura;20,5;\n"
        "101;A;cof;0,38;COF: liberado\n"
        "102;B;espessura;abc;\n",
        encoding="utf-8",
    )
    return caminho


# ---- Funções pequenas: fáceis de testar ---------------------------------------
@pytest.mark.parametrize(
    ("texto", "esperado"),
    [("20,3", 20.3), (" 0,38 ", 0.38), ("1.250,5", 1250.5), ("15", 15.0)],
)
def test_converter_numero_br(texto, esperado):
    assert ref.converter_numero_br(texto) == pytest.approx(esperado)


def test_converter_numero_br_invalido():
    with pytest.raises(ValueError):
        ref.converter_numero_br("abc")


@pytest.mark.parametrize(
    ("observacao", "esperado"),
    [
        ("COF: liberado", {"cof"}),
        ("COF: liberado; Selagem: LIBERADO", {"cof", "selagem"}),
        ("COF: reprovado", set()),
        ("", set()),
        ("sem dois pontos", set()),
    ],
)
def test_ensaios_liberados(observacao, esperado):
    assert ref.ensaios_liberados(observacao) == esperado


# ---- Regras de classificação --------------------------------------------------
@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(19.0, OK), (21.0, OK), (20.0, OK), (18.99, FORA), (21.01, FORA)],
)
def test_classificar_respeita_as_bordas(valor, esperado):
    medicao = Medicao("1", "A", "espessura", valor)
    assert ref.classificar(medicao, LIMITES_TESTE) == esperado


def test_classificar_sem_regra():
    medicao = Medicao("1", "Z", "espessura", 20.0)
    assert ref.classificar(medicao, LIMITES_TESTE) == SEM_REGRA


def test_fora_com_observacao_do_mesmo_ensaio_vira_liberado():
    medicao = Medicao("1", "A", "cof", 0.38, "COF: liberado")
    assert ref.classificar(medicao, LIMITES_TESTE) == LIBERADO


def test_observacao_de_outro_ensaio_nao_libera():
    medicao = Medicao("1", "A", "cof", 0.38, "Selagem: liberado")
    assert ref.classificar(medicao, LIMITES_TESTE) == FORA


# ---- Leitura do arquivo (tmp_path + caplog) -----------------------------------
def test_ler_medicoes_normaliza_campos(csv_exemplo):
    medicoes = ref.ler_medicoes(csv_exemplo)
    assert medicoes[0] == Medicao("100", "A", "espessura", 20.5, "")
    assert medicoes[1].observacao == "COF: liberado"


def test_ler_medicoes_ignora_valor_invalido_e_avisa_no_log(csv_exemplo, caplog):
    with caplog.at_level(logging.WARNING, logger="conferencia"):
        medicoes = ref.ler_medicoes(csv_exemplo)
    assert len(medicoes) == 2
    assert "linha 4 ignorada" in caplog.text


# ---- Relatório e programa completo (capsys) -----------------------------------
def test_resumir_conta_por_linha():
    classificadas = [
        (Medicao("1", "A", "espessura", 20.0), OK),
        (Medicao("2", "A", "espessura", 25.0), FORA),
        (Medicao("3", "A", "cof", 0.38), LIBERADO),
        (Medicao("4", "A", "tracao", 35.0), SEM_REGRA),
    ]
    assert ref.resumir(classificadas) == {"A": {"total": 3, "fora": 1, "liberadas": 1}}


def test_main_imprime_relatorio(csv_exemplo, capsys):
    codigo = ref.main(["--arquivo", str(csv_exemplo)])
    saida = capsys.readouterr().out
    assert codigo == 0
    assert "OP 100 | linha A | espessura | 20,50 | OK" in saida
    assert "OP 101 | linha A | cof | 0,38 | LIBERADO" in saida
    assert saida.strip().endswith("A: 2 medições, 0 fora (0,0%), 1 liberada(s)")
