from _curso import carregar

ex = carregar(__file__, "ex06_nome_disponivel")


def test_nome_livre_volta_igual(tmp_path):
    assert ex.nome_disponivel(tmp_path, "certificado_123456.pdf") == (
        tmp_path / "certificado_123456.pdf"
    )


def test_nome_ocupado_ganha_numero_2(tmp_path):
    (tmp_path / "certificado_123456.pdf").write_bytes(b"x")
    assert ex.nome_disponivel(tmp_path, "certificado_123456.pdf") == (
        tmp_path / "certificado_123456 (2).pdf"
    )


def test_pula_numeros_ja_usados(tmp_path):
    for nome in ["relatorio.xlsx", "relatorio (2).xlsx", "relatorio (3).xlsx"]:
        (tmp_path / nome).write_bytes(b"x")
    assert ex.nome_disponivel(tmp_path, "relatorio.xlsx") == tmp_path / "relatorio (4).xlsx"


def test_arquivo_sem_extensao(tmp_path):
    (tmp_path / "LEIAME").write_text("x", encoding="utf-8")
    assert ex.nome_disponivel(tmp_path, "LEIAME") == tmp_path / "LEIAME (2)"


def test_nome_com_varios_pontos_usa_a_ultima_extensao(tmp_path):
    (tmp_path / "laudo.v1.pdf").write_bytes(b"x")
    assert ex.nome_disponivel(tmp_path, "laudo.v1.pdf") == tmp_path / "laudo.v1 (2).pdf"


def test_nao_cria_arquivo(tmp_path):
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    ex.nome_disponivel(tmp_path, "a.txt")
    ex.nome_disponivel(tmp_path, "b.txt")
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.txt"], (
        "A função só escolhe o nome; quem grava é quem chama"
    )
