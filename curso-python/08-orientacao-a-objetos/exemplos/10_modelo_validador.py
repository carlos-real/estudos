"""No mundo real: o modelo de objetos do Validador de Certificados.

Junta tudo do módulo: Enum (linhas e situações), dataclasses imutáveis
(Tolerancia, Medicao, Pedido), @classmethod (Tolerancia.por_nominal), composição
(LinhaDeProducao tem Especificacao), @property (Certificado.aprovado) e __str__.

Regras do laboratório:
- cada linha tem tolerâncias FIXAS e uma especificação PADRÃO;
- uma OP pode ter especificação PRÓPRIA (título + texto), que vale no lugar da padrão;
- a observação "COF: liberado" na planilha libera um ensaio reprovado (decisão da
  qualidade), e o certificado sai com a anotação.

Rode com:  python exemplos/10_modelo_validador.py
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Linha(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Situacao(Enum):
    APROVADO = "aprovado"
    LIBERADO = "liberado pela qualidade"
    REPROVADO = "reprovado"


@dataclass(frozen=True)
class Tolerancia:
    minimo: float | None = None
    maximo: float | None = None

    @classmethod
    def por_nominal(cls, nominal: float, percentual: float) -> "Tolerancia":
        margem = nominal * percentual / 100
        return cls(round(nominal - margem, 4), round(nominal + margem, 4))

    def aprova(self, valor: float) -> bool:
        acima_do_minimo = self.minimo is None or valor >= self.minimo
        abaixo_do_maximo = self.maximo is None or valor <= self.maximo
        return acima_do_minimo and abaixo_do_maximo


@dataclass
class Especificacao:
    titulo: str
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)
    texto: str = ""


class LinhaDeProducao:
    def __init__(self, linha: Linha, fixas: dict[str, Tolerancia], padrao: Especificacao):
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


@dataclass(frozen=True)
class Medicao:
    op: str
    ensaio: str
    valor: float
    unidade: str = ""


@dataclass(frozen=True)
class Pedido:
    op: str
    nf: str
    cliente: str
    peso_kg: float
    linha: Linha


@dataclass(frozen=True)
class Resultado:
    medicao: Medicao
    situacao: Situacao

    def __str__(self) -> str:
        m = self.medicao
        return f"{m.ensaio}: {m.valor:g} {m.unidade}".rstrip() + f" ({self.situacao.value})"


@dataclass
class Certificado:
    pedido: Pedido
    especificacao: Especificacao
    emissao: date
    resultados: list[Resultado] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return bool(self.resultados) and all(
            r.situacao is not Situacao.REPROVADO for r in self.resultados
        )

    def __str__(self) -> str:
        p = self.pedido
        linhas = [
            f"CERTIFICADO {p.op} | NF {p.nf} | {p.cliente} | {p.peso_kg:g} kg",
            f"  Especificação: {self.especificacao.titulo}  ({self.emissao:%d/%m/%Y})",
        ]
        linhas += [f"  - {r}" for r in self.resultados]
        linhas.append(f"  => {'PODE EMITIR' if self.aprovado else 'BLOQUEADO'}")
        return "\n".join(linhas)


def avaliar(
    pedido: Pedido,
    linha: LinhaDeProducao,
    medicoes: list[Medicao],
    liberados: set[tuple[str, str]],
    emissao: date,
) -> Certificado:
    """Monta o certificado: cada medição vira um Resultado com a sua Situacao."""
    tolerancias = linha.tolerancias_para(pedido.op)
    certificado = Certificado(pedido, linha.especificacao_para(pedido.op), emissao)
    for medicao in medicoes:
        if medicao.op != pedido.op or medicao.ensaio not in tolerancias:
            continue
        if tolerancias[medicao.ensaio].aprova(medicao.valor):
            situacao = Situacao.APROVADO
        elif (pedido.op, medicao.ensaio) in liberados:
            situacao = Situacao.LIBERADO
        else:
            situacao = Situacao.REPROVADO
        certificado.resultados.append(Resultado(medicao, situacao))
    return certificado


# --- Regras (no projeto final vêm do SQLite) ---------------------------------
fixas = {"cof": Tolerancia(0.10, 0.30), "tração": Tolerancia(minimo=20)}
linhas = {
    Linha.A: LinhaDeProducao(
        Linha.A,
        fixas,
        Especificacao("Filme PE 20 µm", {"espessura": Tolerancia.por_nominal(20, 10)}),
    ),
    Linha.B: LinhaDeProducao(
        Linha.B,
        fixas,
        Especificacao("Filme PE 25 µm", {"espessura": Tolerancia.por_nominal(25, 10)}),
    ),
}
linhas[Linha.B].cadastrar(
    "OP245106",
    Especificacao(
        "Café Montanha", {"espessura": Tolerancia(24.0, 26.0)}, "Espessura 25 ± 1 µm"
    ),
)

# --- Dados do dia (no projeto final vêm da planilha e dos e-mails) ----------
pedidos = [
    Pedido("OP245101", "123456", "Alimentos Bom Sabor", 1250.5, Linha.A),
    Pedido("OP245106", "123457", "Café Montanha", 980.0, Linha.B),
    Pedido("OP245118", "123460", "Pet Nutri", 2010.75, Linha.B),
]
medicoes = [
    Medicao("OP245101", "espessura", 20.4, "µm"),
    Medicao("OP245101", "cof", 0.21),
    Medicao("OP245101", "tração", 31.0, "MPa"),
    Medicao("OP245106", "espessura", 26.3, "µm"),
    Medicao("OP245106", "cof", 0.28),
    Medicao("OP245118", "espessura", 25.1, "µm"),
    Medicao("OP245118", "cof", 0.33),
]
liberados = {("OP245118", "cof")}  # veio da observação "COF: liberado" na planilha

for pedido in pedidos:
    certificado = avaliar(
        pedido, linhas[pedido.linha], medicoes, liberados, date(2026, 10, 29)
    )
    print(certificado, end="\n\n")
