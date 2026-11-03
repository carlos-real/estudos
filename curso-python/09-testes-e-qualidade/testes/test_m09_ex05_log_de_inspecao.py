import logging

import pytest

from _curso import carregar

ex = carregar(__file__, "ex05_log_de_inspecao")

NOME_DO_LOGGER = "lab.inspecao.teste"


@pytest.fixture
def logger(caplog):
    """Logger usado nos testes, já com o caplog capturando a partir de INFO."""
    caplog.set_level(logging.INFO, logger=NOME_DO_LOGGER)
    return logging.getLogger(NOME_DO_LOGGER)


def test_valor_dentro_devolve_true_e_registra_info(logger, caplog):
    assert ex.registrar_resultado(logger, "123", 25.4, 24.0, 26.0) is True
    assert len(caplog.records) == 1, "registre exatamente uma mensagem por chamada"
    registro = caplog.records[0]
    assert registro.levelname == "INFO"
    assert registro.getMessage() == "OP 123: 25.40 dentro de [24.00, 26.00]"


def test_valor_fora_devolve_false_e_registra_warning(logger, caplog):
    assert ex.registrar_resultado(logger, "124", 27.1, 24.0, 26.0) is False
    assert len(caplog.records) == 1, "registre exatamente uma mensagem por chamada"
    registro = caplog.records[0]
    assert registro.levelname == "WARNING"
    assert registro.getMessage() == "OP 124: 27.10 FORA de [24.00, 26.00]"


@pytest.mark.parametrize("valor", [24.0, 26.0])
def test_bordas_estao_dentro(logger, caplog, valor):
    assert ex.registrar_resultado(logger, "125", valor, 24.0, 26.0) is True
    assert caplog.records[0].levelname == "INFO"


def test_abaixo_do_minimo_esta_fora(logger, caplog):
    assert ex.registrar_resultado(logger, "126", 23.99, 24.0, 26.0) is False
    assert caplog.records[0].getMessage() == "OP 126: 23.99 FORA de [24.00, 26.00]"


def test_usa_o_logger_recebido(logger, caplog):
    ex.registrar_resultado(logger, "127", 25.0, 24.0, 26.0)
    assert caplog.records[0].name == NOME_DO_LOGGER, (
        "use o logger recebido no parâmetro, não logging.info()"
    )


def test_nao_usa_print(logger, capsys):
    ex.registrar_resultado(logger, "128", 25.0, 24.0, 26.0)
    assert capsys.readouterr().out == "", "o resultado vai para o log, não para o print"
