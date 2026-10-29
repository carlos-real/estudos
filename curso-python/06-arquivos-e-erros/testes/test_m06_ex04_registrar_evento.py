from _curso import carregar

ex = carregar(__file__, "ex04_registrar_evento")


def test_cria_arquivo_com_a_linha(tmp_path):
    log = tmp_path / "robo.log"
    ex.registrar_evento(log, "08:00", "Início")
    assert log.read_text(encoding="utf-8") == "08:00 | Início\n"


def test_acrescenta_sem_apagar(tmp_path):
    log = tmp_path / "robo.log"
    log.write_text("linha antiga\n", encoding="utf-8")
    ex.registrar_evento(log, "08:00", "Início")
    ex.registrar_evento(log, "08:01", "OP 123456 emitida")
    assert log.read_text(encoding="utf-8") == (
        "linha antiga\n08:00 | Início\n08:01 | OP 123456 emitida\n"
    ), "Use o modo 'a' (append): o modo 'w' apaga o que já existia."


def test_cria_pastas_que_faltam(tmp_path):
    log = tmp_path / "logs" / "2025" / "outubro" / "robo.log"
    ex.registrar_evento(log, "08:00", "Início")
    ex.registrar_evento(log, "08:05", "Fim")
    assert log.read_text(encoding="utf-8").splitlines() == ["08:00 | Início", "08:05 | Fim"]


def test_grava_em_utf8(tmp_path):
    log = tmp_path / "robo.log"
    ex.registrar_evento(log, "08:00", "Certificado de laminação: µm")
    assert log.read_bytes() == "08:00 | Certificado de laminação: µm\n".encode()
