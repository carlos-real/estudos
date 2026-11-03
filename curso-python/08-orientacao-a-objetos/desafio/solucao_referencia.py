"""Solução de referência do desafio do módulo 08: Validador de Certificados (modelo OO).

Lê as regras (dados/regras.json), os pedidos da expedição (dados/pedidos.csv) e as
medições do laboratório (dados/medicoes.csv), avalia cada OP com as tolerâncias da
linha (fixas + especificação padrão ou própria da OP), aplica as observações de
liberação ("COF: liberado") e mostra quais certificados podem ser emitidos.

Rode com (na pasta curso-python):
    python 08-orientacao-a-objetos/desafio/solucao_referencia.py --data 29/10/2026
    python 08-orientacao-a-objetos/desafio/solucao_referencia.py --op OP245118
    python 08-orientacao-a-objetos/desafio/solucao_referencia.py --saida saida/certificados

Com --saida, grava um .txt por certificado emitível (a pasta saida/ está no .gitignore).
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"


# --- Enums ------------------------------------------------------------------
class Linha(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Situacao(Enum):
    APROVADO = "aprovado"
    LIBERADO = "liberado pela qualidade"
    PENDENTE = "pendente de decisão"
    REPROVADO = "reprovado"
    INFORMATIVO = "informativo (sem tolerância)"

    @property
    def bloqueia(self) -> bool:
        return self in (Situacao.REPROVADO, Situacao.PENDENTE)


# --- Regras -----------------------------------------------------------------
@dataclass(frozen=True)
class Tolerancia:
    minimo: float | None = None
    maximo: float | None = None

    def __post_init__(self) -> None:
        if self.minimo is None and self.maximo is None:
            raise ValueError("Tolerância sem limites")
        if self.minimo is not None and self.maximo is not None and self.minimo > self.maximo:
            raise ValueError(f"Mínimo {self.minimo} maior que máximo {self.maximo}")

    @classmethod
    def por_nominal(cls, nominal: float, percentual: float) -> "Tolerancia":
        margem = nominal * percentual / 100
        return cls(round(nominal - margem, 4), round(nominal + margem, 4))

    @classmethod
    def de_dict(cls, dados: dict) -> "Tolerancia":
        """{'nominal': 25, 'percentual': 10} ou {'minimo': 0.1, 'maximo': 0.3}."""
        if "nominal" in dados:
            return cls.por_nominal(dados["nominal"], dados["percentual"])
        return cls(dados.get("minimo"), dados.get("maximo"))

    def aprova(self, valor: float) -> bool:
        if self.minimo is not None and valor < self.minimo:
            return False
        return self.maximo is None or valor <= self.maximo

    def __str__(self) -> str:
        def br(numero: float) -> str:
            return f"{numero:g}".replace(".", ",")

        if self.minimo is not None and self.maximo is not None:
            return f"{br(self.minimo)} a {br(self.maximo)}"
        if self.minimo is not None:
            return f"mín. {br(self.minimo)}"
        return f"máx. {br(self.maximo)}"


@dataclass
class Especificacao:
    titulo: str
    texto: str = ""
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)

    @classmethod
    def de_dict(cls, dados: dict) -> "Especificacao":
        tolerancias = {nome: Tolerancia.de_dict(t) for nome, t in dados["tolerancias"].items()}
        return cls(dados["titulo"], dados.get("texto", ""), tolerancias)


class LinhaDeProducao:
    """Composição: a linha TEM tolerâncias fixas, uma especificação padrão e as das OPs."""

    def __init__(
        self, linha: Linha, fixas: dict[str, Tolerancia], padrao: Especificacao
    ) -> None:
        self.linha = linha
        self.fixas = dict(fixas)
        self.padrao = padrao
        self._por_op: dict[str, Especificacao] = {}

    def cadastrar(self, op: str, especificacao: Especificacao) -> None:
        self._por_op[op] = especificacao

    def especificacao_para(self, op: str) -> Especificacao:
        return self._por_op.get(op, self.padrao)

    def tolerancias_para(self, op: str) -> dict[str, Tolerancia]:
        return {**self.fixas, **self.especificacao_para(op).tolerancias}


# --- Dados do dia -----------------------------------------------------------
@dataclass(frozen=True)
class Pedido:
    op: str
    nf: str
    cliente: str
    peso_kg: float
    linha: Linha


@dataclass(frozen=True)
class Medicao:
    op: str
    ensaio: str
    valor: float
    unidade: str = ""
    observacao: str = ""


@dataclass(frozen=True)
class Resultado:
    medicao: Medicao
    tolerancia: Tolerancia | None
    situacao: Situacao

    def linha_do_certificado(self) -> str:
        m = self.medicao
        medida = f"{numero_br(m.valor)} {m.unidade}".rstrip()
        faixa = f" [tol.: {self.tolerancia}]" if self.tolerancia else ""
        return f"- {m.ensaio}: {medida}{faixa} -> {self.situacao.value}"


@dataclass
class Certificado:
    pedido: Pedido
    especificacao: Especificacao
    emissao: date
    resultados: list[Resultado] = field(default_factory=list)

    @property
    def numero(self) -> str:
        return f"CQ-{self.emissao:%Y%m%d}-{self.pedido.op}"

    @property
    def pode_emitir(self) -> bool:
        avaliados = [r for r in self.resultados if r.situacao is not Situacao.INFORMATIVO]
        return bool(avaliados) and not any(r.situacao.bloqueia for r in self.resultados)

    @property
    def pendencias(self) -> list[str]:
        return [
            f"{r.medicao.ensaio} {r.situacao.value}"
            for r in self.resultados
            if r.situacao.bloqueia
        ]

    def texto(self) -> str:
        p = self.pedido
        linhas = [
            f"CERTIFICADO DE QUALIDADE Nº {self.numero}",
            f"Cliente: {p.cliente}",
            f"OP: {p.op} | NF: {p.nf} | Linha: {p.linha.value} | "
            f"Peso: {numero_br(p.peso_kg)} kg",
            f"Especificação: {self.especificacao.titulo}",
        ]
        if self.especificacao.texto:
            linhas.append(f"  {self.especificacao.texto}")
        linhas.append(f"Emissão: {self.emissao:%d/%m/%Y}")
        linhas += [r.linha_do_certificado() for r in self.resultados]
        return "\n".join(linhas)

    def salvar(self, pasta: Path) -> Path:
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"{self.numero}.txt"
        destino.write_text(self.texto() + "\n", encoding="utf-8")
        return destino


class Validador:
    """Junta regras e medições e produz os certificados."""

    def __init__(self, linhas: dict[Linha, LinhaDeProducao], medicoes: list[Medicao]) -> None:
        self.linhas = linhas
        self.medicoes = medicoes

    def certificar(self, pedido: Pedido, emissao: date) -> Certificado:
        linha = self.linhas[pedido.linha]
        tolerancias = linha.tolerancias_para(pedido.op)
        certificado = Certificado(pedido, linha.especificacao_para(pedido.op), emissao)
        for medicao in (m for m in self.medicoes if m.op == pedido.op):
            tolerancia = tolerancias.get(medicao.ensaio)
            certificado.resultados.append(
                Resultado(medicao, tolerancia, situacao_da_medicao(medicao, tolerancia))
            )
        return certificado


def situacao_da_medicao(medicao: Medicao, tolerancia: Tolerancia | None) -> Situacao:
    if tolerancia is None:
        return Situacao.INFORMATIVO
    if tolerancia.aprova(medicao.valor):
        return Situacao.APROVADO
    decisao = decisao_da_observacao(medicao)
    if decisao == "liberado":
        return Situacao.LIBERADO
    if decisao == "pendente":
        return Situacao.PENDENTE
    return Situacao.REPROVADO


def decisao_da_observacao(medicao: Medicao) -> str:
    """'COF: liberado' na medição de cof -> 'liberado'. Outro ensaio ou vazio -> ''."""
    if ":" not in medicao.observacao:
        return ""
    ensaio, decisao = medicao.observacao.split(":", 1)
    if ensaio.strip().lower() != medicao.ensaio.lower():
        return ""
    return decisao.strip().lower()


# --- Leitura dos arquivos ---------------------------------------------------
def numero_br(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_numero_br(texto: str) -> float:
    return float(texto.strip().replace(".", "").replace(",", "."))


def carregar_regras(caminho: Path) -> tuple[dict[Linha, LinhaDeProducao], dict]:
    """Devolve (linhas de produção, especificações próprias das OPs ainda em dict)."""
    with open(caminho, encoding="utf-8") as arquivo:
        regras = json.load(arquivo)
    linhas = {}
    for nome, dados in regras["linhas"].items():
        fixas = {ensaio: Tolerancia.de_dict(t) for ensaio, t in dados["fixas"].items()}
        linha = Linha(nome)
        linhas[linha] = LinhaDeProducao(linha, fixas, Especificacao.de_dict(dados["padrao"]))
    return linhas, regras.get("especificacoes_op", {})


def ler_pedidos(caminho: Path) -> list[Pedido]:
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return [
            Pedido(
                r["op"], r["nf"], r["cliente"], ler_numero_br(r["peso_kg"]), Linha(r["linha"])
            )
            for r in csv.DictReader(arquivo, delimiter=";")
        ]


def ler_medicoes(caminho: Path) -> list[Medicao]:
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return [
            Medicao(
                r["op"], r["ensaio"], ler_numero_br(r["valor"]), r["unidade"], r["observacao"]
            )
            for r in csv.DictReader(arquivo, delimiter=";")
        ]


# --- Linha de comando -------------------------------------------------------
def data_br(texto: str) -> date:
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"data inválida: {texto!r} (use dd/mm/aaaa)"
        ) from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="validador", description="Valida OPs e certifica.")
    parser.add_argument("--dados", type=Path, default=PASTA_DADOS, help="pasta dos arquivos")
    parser.add_argument("--data", type=data_br, help="data de emissão (padrão: hoje)")
    parser.add_argument("--op", help="avalia só esta OP")
    parser.add_argument("--saida", type=Path, help="grava os certificados emitíveis aqui")
    args = parser.parse_args(argv)

    try:
        linhas, especificacoes_op = carregar_regras(args.dados / "regras.json")
        pedidos = ler_pedidos(args.dados / "pedidos.csv")
        medicoes = ler_medicoes(args.dados / "medicoes.csv")
    except FileNotFoundError as erro:
        print(f"Arquivo não encontrado: {erro.filename}", file=sys.stderr)
        return 2

    # A especificação própria vale para a linha onde a OP foi produzida.
    linha_da_op = {p.op: p.linha for p in pedidos}
    for op, dados in especificacoes_op.items():
        if op in linha_da_op:
            linhas[linha_da_op[op]].cadastrar(op, Especificacao.de_dict(dados))

    if args.op:
        pedidos = [p for p in pedidos if p.op == args.op.upper()]
        if not pedidos:
            print(f"OP {args.op} não está nos pedidos.", file=sys.stderr)
            return 2

    validador = Validador(linhas, medicoes)
    emissao = args.data or date.today()
    emitiveis, bloqueados = [], []
    for pedido in pedidos:
        certificado = validador.certificar(pedido, emissao)
        print(certificado.texto())
        if certificado.pode_emitir:
            print("=> PODE EMITIR\n")
            emitiveis.append(certificado)
        else:
            print(f"=> BLOQUEADO: {', '.join(certificado.pendencias)}\n")
            bloqueados.append(certificado)

    print(f"Resumo: {len(emitiveis)} para emitir, {len(bloqueados)} bloqueado(s).")
    if args.saida:
        for certificado in emitiveis:
            print("Gravado:", certificado.salvar(args.saida))
    return 0


if __name__ == "__main__":
    sys.exit(main())
