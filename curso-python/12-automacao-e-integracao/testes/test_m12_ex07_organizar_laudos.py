from _curso import carregar

ex = carregar(__file__, "ex07_organizar_laudos")

LAUDOS = [
    "laudo_123789_A_2026-04-02.pdf",
    "laudo_123456_B_2026-03-10.pdf",
    "laudo_123456_B_2026-03-28.pdf",
]
INTRUSOS = [
    "laudo_12345_B_2026-03-10.pdf",  # OP com 5 dígitos
    "laudo_123456_E_2026-03-10.pdf",  # linha inexistente
    "laudo_123456_B_2026-03-10.docx",  # extensão errada
    "copia de laudo_123456_B_2026-03-10.pdf",
    "anotacoes.txt",
]


def preparar(tmp_path):
    origem = tmp_path / "entrada"
    destino = tmp_path / "laudos"
    origem.mkdir()
    for nome in LAUDOS + INTRUSOS:
        (origem / nome).write_text(nome, encoding="utf-8")
    return origem, destino


PLANO_ESPERADO = [
    ("laudo_123456_B_2026-03-10.pdf", "linha_B/2026-03/laudo_123456_B_2026-03-10.pdf"),
    ("laudo_123456_B_2026-03-28.pdf", "linha_B/2026-03/laudo_123456_B_2026-03-28.pdf"),
    ("laudo_123789_A_2026-04-02.pdf", "linha_A/2026-04/laudo_123789_A_2026-04-02.pdf"),
]


def test_ensaio_devolve_o_plano_em_ordem(tmp_path):
    origem, destino = preparar(tmp_path)
    assert ex.organizar_laudos(origem, destino) == PLANO_ESPERADO


def test_ensaio_nao_mexe_em_nada(tmp_path):
    origem, destino = preparar(tmp_path)
    plano = ex.organizar_laudos(origem, destino, ensaio=True)
    assert len(plano) == 3
    assert not destino.exists(), "Em ensaio, nenhuma pasta deve ser criada"
    assert len(list(origem.iterdir())) == len(LAUDOS + INTRUSOS)


def test_execucao_real_move_os_arquivos(tmp_path):
    origem, destino = preparar(tmp_path)
    assert ex.organizar_laudos(origem, destino, ensaio=False) == PLANO_ESPERADO
    movido = destino / "linha_B" / "2026-03" / "laudo_123456_B_2026-03-10.pdf"
    assert movido.read_text(encoding="utf-8") == "laudo_123456_B_2026-03-10.pdf"
    assert (destino / "linha_A" / "2026-04" / "laudo_123789_A_2026-04-02.pdf").exists()
    restantes = sorted(p.name for p in origem.iterdir())
    assert restantes == sorted(INTRUSOS), "Só os laudos válidos devem sair da origem"


def test_nao_sobrescreve_arquivo_existente(tmp_path):
    origem, destino = preparar(tmp_path)
    pasta = destino / "linha_B" / "2026-03"
    pasta.mkdir(parents=True)
    (pasta / "laudo_123456_B_2026-03-10.pdf").write_text("VERSÃO ANTIGA", encoding="utf-8")

    plano = ex.organizar_laudos(origem, destino, ensaio=False)

    nomes = [nome for nome, _ in plano]
    assert "laudo_123456_B_2026-03-10.pdf" not in nomes
    assert len(plano) == 2
    assert (pasta / "laudo_123456_B_2026-03-10.pdf").read_text(encoding="utf-8") == (
        "VERSÃO ANTIGA"
    )
    assert (origem / "laudo_123456_B_2026-03-10.pdf").exists(), "O original fica na origem"


def test_ignora_pasta_com_nome_de_laudo(tmp_path):
    origem, destino = preparar(tmp_path)
    (origem / "laudo_999999_C_2026-05-01.pdf").mkdir()
    nomes = [nome for nome, _ in ex.organizar_laudos(origem, destino)]
    assert "laudo_999999_C_2026-05-01.pdf" not in nomes
    assert len(nomes) == 3
