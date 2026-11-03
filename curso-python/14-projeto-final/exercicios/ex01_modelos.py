"""
Exercício 14.01 — Modelos de dados do sistema
Nível: ★☆☆

Contexto: Todo o Validador de Certificados conversa por meio de "fichas": Tolerancia,
Especificacao, Medicao, Pedido, ResultadoValidacao e ItemFila. Os campos já estão
declarados abaixo. Leia com calma: eles aparecem em todas as etapas seguintes. Falta o
comportamento que impede uma ficha inválida de existir.

Tarefa: implemente três coisas.
1. Tolerancia.__post_init__: levante ValueError quando
   - tipo não for "fixa" nem "nominal";
   - tipo "fixa" vier sem mínimo E sem máximo (os dois None);
   - tipo "fixa" tiver mínimo maior que o máximo (quando os dois existem);
   - tipo "nominal" tiver percentual None, zero ou negativo.
2. Pedido.__post_init__: levante ValueError quando op ou nf estiverem vazios (ou só
   com espaços), ou quando peso_kg for zero ou negativo.
3. ResultadoValidacao.aprovado (propriedade): True quando a lista de motivos está
   vazia; False quando há pelo menos um motivo.

Exemplos:
    >>> Tolerancia("cof", "fixa", minimo=0.15, maximo=0.35)
    Tolerancia(caracteristica='cof', tipo='fixa', minimo=0.15, maximo=0.35, percentual=None)
    >>> Tolerancia("cof", "faixa")
    Traceback (most recent call last):
    ValueError: tipo de tolerância inválido: 'faixa'
    >>> ResultadoValidacao("24518", "PADRAO-A").aprovado
    True
    >>> ResultadoValidacao("24519", "PADRAO-A", ["espessura alta"]).aprovado
    False

Dica: no __post_init__ os campos já estão preenchidos (self.tipo, self.minimo...).
Uma propriedade é um método com @property em cima: lê-se sem parênteses.

Teste com:  python curso.py testar 14 ex01
"""

from dataclasses import dataclass, field

TIPOS_TOLERANCIA = ("fixa", "nominal")


@dataclass(frozen=True)
class Tolerancia:
    """Limite de uma característica: "fixa" (mínimo/máximo) ou "nominal" (± %)."""

    caracteristica: str
    tipo: str
    minimo: float | None = None
    maximo: float | None = None
    percentual: float | None = None

    def __post_init__(self) -> None:
        """Recusa tolerâncias sem sentido (levanta ValueError)."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta função")


@dataclass
class Especificacao:
    """Conjunto de tolerâncias. `linha` só é preenchida nos padrões de linha."""

    titulo: str
    texto: str = ""
    linha: str = ""
    tolerancias: dict[str, Tolerancia] = field(default_factory=dict)


@dataclass
class Medicao:
    """Uma linha da planilha de valores (uma OP)."""

    op: str
    aba: str
    linha: str
    valores: dict[str, float] = field(default_factory=dict)
    nominais: dict[str, float] = field(default_factory=dict)
    especificacao: str = ""
    observacao: str = ""
    produto: str = ""
    linha_excel: int = 0


@dataclass(frozen=True)
class Pedido:
    """Pedido de certificado vindo da expedição (um por e-mail)."""

    op: str
    nf: str
    peso_kg: float
    origem: str = ""

    def __post_init__(self) -> None:
        """Recusa pedido sem OP, sem NF ou com peso <= 0 (levanta ValueError)."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta função")


@dataclass
class ResultadoValidacao:
    """Resultado da conferência de uma OP contra uma especificação."""

    op: str
    especificacao: str
    motivos: list[str] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        """True quando não há nenhum motivo de reprovação."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta função")


@dataclass
class ItemFila:
    """Um pedido depois da triagem (situação "emitir", "bloqueado", ...)."""

    op: str
    nf: str
    peso_kg: float
    situacao: str
    especificacao: str = ""
    motivos: list[str] = field(default_factory=list)
    comprovante: str = ""
