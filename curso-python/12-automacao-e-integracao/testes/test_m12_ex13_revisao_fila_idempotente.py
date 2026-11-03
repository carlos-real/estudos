import csv

from _curso import carregar

ex = carregar(__file__, "ex13_revisao_fila_idempotente")

PEDIDOS = [
    {"op": "123456", "nf": "98765"},
    {"op": "123789", "nf": "98766"},
    {"op": "124001", "nf": "98770"},
]


class EmissorFalso:
    """Imita o robô: devolve números de certificado em sequência e anota as chamadas."""

    def __init__(self, falhar_em=()):
        self.falhar_em = set(falhar_em)
        self.chamadas = []

    def __call__(self, pedido):
        self.chamadas.append(pedido["op"])
        if pedido["op"] in self.falhar_em:
            raise RuntimeError("a tela travou")
        return f"{len(self.chamadas):06d}"


def ler_csv(caminho):
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return list(csv.reader(arquivo, delimiter=";"))


def test_primeira_rodada_emite_tudo(tmp_path):
    registro = tmp_path / "emitidos.csv"
    emissor = EmissorFalso()
    resultado = ex.processar_fila(PEDIDOS, emissor, registro)
    assert resultado == {"emitidos": 3, "pulados": 0, "falhas": 0}
    assert emissor.chamadas == ["123456", "123789", "124001"]
    assert ler_csv(registro) == [
        ["op", "nf", "certificado"],
        ["123456", "98765", "000001"],
        ["123789", "98766", "000002"],
        ["124001", "98770", "000003"],
    ]


def test_segunda_rodada_nao_emite_de_novo(tmp_path):
    registro = tmp_path / "emitidos.csv"
    ex.processar_fila(PEDIDOS, EmissorFalso(), registro)
    emissor = EmissorFalso()
    resultado = ex.processar_fila(PEDIDOS, emissor, registro)
    assert resultado == {"emitidos": 0, "pulados": 3, "falhas": 0}
    assert emissor.chamadas == [], "Pedidos já registrados não podem chamar emitir()"
    assert len(ler_csv(registro)) == 4, "O registro não pode ganhar linhas repetidas"


def test_falha_nao_derruba_a_fila_e_nao_e_registrada(tmp_path):
    registro = tmp_path / "emitidos.csv"
    emissor = EmissorFalso(falhar_em={"123789"})
    resultado = ex.processar_fila(PEDIDOS, emissor, registro)
    assert resultado == {"emitidos": 2, "pulados": 0, "falhas": 1}
    assert emissor.chamadas == ["123456", "123789", "124001"]
    ops = [linha[0] for linha in ler_csv(registro)[1:]]
    assert ops == ["123456", "124001"]


def test_pedido_que_falhou_e_tentado_na_proxima_rodada(tmp_path):
    registro = tmp_path / "emitidos.csv"
    ex.processar_fila(PEDIDOS, EmissorFalso(falhar_em={"123789"}), registro)
    emissor = EmissorFalso()
    resultado = ex.processar_fila(PEDIDOS, emissor, registro)
    assert resultado == {"emitidos": 1, "pulados": 2, "falhas": 0}
    assert emissor.chamadas == ["123789"]


def test_repetido_dentro_da_mesma_fila(tmp_path):
    registro = tmp_path / "emitidos.csv"
    fila = [PEDIDOS[0], PEDIDOS[1], dict(PEDIDOS[0])]
    resultado = ex.processar_fila(fila, EmissorFalso(), registro)
    assert resultado == {"emitidos": 2, "pulados": 1, "falhas": 0}


def test_mesma_op_com_outra_nf_e_outro_pedido(tmp_path):
    registro = tmp_path / "emitidos.csv"
    fila = [{"op": "123456", "nf": "98765"}, {"op": "123456", "nf": "98799"}]
    assert ex.processar_fila(fila, EmissorFalso(), registro)["emitidos"] == 2


def test_respeita_registro_que_ja_existia(tmp_path):
    registro = tmp_path / "emitidos.csv"
    registro.write_text("op;nf;certificado\n124001;98770;000777\n", encoding="utf-8")
    emissor = EmissorFalso()
    resultado = ex.processar_fila(PEDIDOS, emissor, registro)
    assert resultado == {"emitidos": 2, "pulados": 1, "falhas": 0}
    assert "124001" not in emissor.chamadas


def test_fila_vazia_cria_registro_com_cabecalho(tmp_path):
    registro = tmp_path / "emitidos.csv"
    assert ex.processar_fila([], EmissorFalso(), registro) == {
        "emitidos": 0,
        "pulados": 0,
        "falhas": 0,
    }
    assert ler_csv(registro) == [["op", "nf", "certificado"]]
