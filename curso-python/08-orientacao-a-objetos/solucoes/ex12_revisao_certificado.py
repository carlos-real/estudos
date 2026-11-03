"""
Exercício 08.12 — Revisão: o certificado de qualidade
Nível: ★★★

Revisão de: módulo 05 (números no formato brasileiro e f-strings), módulo 06
(gravar arquivo com pathlib e exceção personalizada) e módulo 07 (datas), junto com
dataclass, @property e @classmethod deste módulo.

Contexto: O certificado é o produto final do seu sistema. Ele junta OP, NF,
cliente, peso, data de emissão e os resultados dos ensaios. Só pode ser emitido se
todos os ensaios estiverem aprovados.

Já estão prontos: `ResultadoEnsaio` (dataclass imutável) e a exceção
`CertificadoReprovadoError`. Tarefa: transforme `Certificado` numa dataclass com os
campos, nesta ordem:
    op: str
    nf: str
    cliente: str
    peso_kg: float
    emissao: date
    resultados: list[ResultadoEnsaio] = (lista vazia nova para cada certificado:
                                         field(default_factory=list))
e implemente:
1. `__post_init__`: op e nf sem espaços nas pontas; vazios -> ValueError;
   peso_kg <= 0 -> ValueError.
2. `numero` (property): "CQ-20261029-OP245101" (data AAAAMMDD + OP).
3. `aprovado` (property): True se houver resultados e todos estiverem aprovados.
4. `texto()`: o certificado, linha a linha, EXATAMENTE assim (números com vírgula
   decimal e ponto de milhar, 2 casas; unidade só se houver):
       CERTIFICADO DE QUALIDADE Nº CQ-20261029-OP245101
       Cliente: Alimentos Bom Sabor
       OP: OP245101 | NF: 123456 | Peso: 1.250,50 kg
       Emissão: 29/10/2026
       Resultados:
       - espessura: 25,10 µm (aprovado)
       - cof: 0,22 (aprovado)
       Situação: APROVADO
   (ou "Situação: REPROVADO"; as linhas são unidas com "\\n", sem "\\n" no fim)
5. `salvar(pasta)`: grava texto() em pasta/"<numero>.txt" (UTF-8), criando a pasta
   se preciso, e devolve o Path do arquivo.
6. `emitir(...)` (classmethod, mesmos parâmetros dos campos): sem resultados ->
   ValueError; algum reprovado -> CertificadoReprovadoError com a mensagem
   "OP245101 reprovada em: cof, espessura" (nomes em ordem alfabética); senão
   devolve o certificado.

Dica: f"{1250.5:,.2f}" dá '1,250.50'; troque os separadores (módulo 05).

Teste com:  python curso.py testar 08 ex12
"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class ResultadoEnsaio:
    """Resultado de um ensaio (pronto)."""

    ensaio: str
    valor: float
    unidade: str
    aprovado: bool


class CertificadoReprovadoError(Exception):
    """Tentativa de emitir certificado com ensaio reprovado (pronta)."""


def formatar_br(valor: float) -> str:
    """1250.5 -> '1.250,50' (módulo 05)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@dataclass
class Certificado:
    """Certificado de qualidade de uma OP expedida."""

    op: str
    nf: str
    cliente: str
    peso_kg: float
    emissao: date
    # default_factory=list cria uma lista NOVA para cada certificado.
    # (resultados: list = [] daria erro: a dataclass recusa padrão mutável.)
    resultados: list[ResultadoEnsaio] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Roda logo depois do __init__ gerado: o lugar certo para validar.
        self.op = self.op.strip()
        self.nf = self.nf.strip()
        if not self.op or not self.nf:
            raise ValueError("OP e NF são obrigatórias")
        if self.peso_kg <= 0:
            raise ValueError(f"Peso inválido: {self.peso_kg}")

    @property
    def numero(self) -> str:
        return f"CQ-{self.emissao:%Y%m%d}-{self.op}"

    @property
    def aprovado(self) -> bool:
        # all([]) é True: sem o "bool(self.resultados) and", um certificado vazio
        # sairia aprovado.
        return bool(self.resultados) and all(r.aprovado for r in self.resultados)

    def texto(self) -> str:
        linhas = [
            f"CERTIFICADO DE QUALIDADE Nº {self.numero}",
            f"Cliente: {self.cliente}",
            f"OP: {self.op} | NF: {self.nf} | Peso: {formatar_br(self.peso_kg)} kg",
            f"Emissão: {self.emissao:%d/%m/%Y}",
            "Resultados:",
        ]
        for r in self.resultados:
            medida = formatar_br(r.valor) + (f" {r.unidade}" if r.unidade else "")
            situacao = "aprovado" if r.aprovado else "reprovado"
            linhas.append(f"- {r.ensaio}: {medida} ({situacao})")
        linhas.append(f"Situação: {'APROVADO' if self.aprovado else 'REPROVADO'}")
        return "\n".join(linhas)

    def salvar(self, pasta: Path) -> Path:
        pasta = Path(pasta)
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"{self.numero}.txt"
        destino.write_text(self.texto(), encoding="utf-8")
        return destino

    @classmethod
    def emitir(
        cls,
        op: str,
        nf: str,
        cliente: str,
        peso_kg: float,
        emissao: date,
        resultados: list[ResultadoEnsaio],
    ) -> "Certificado":
        """Cria o certificado só se TODOS os ensaios estiverem aprovados."""
        if not resultados:
            raise ValueError("Sem resultados de ensaio não há certificado")
        reprovados = sorted(r.ensaio for r in resultados if not r.aprovado)
        if reprovados:
            raise CertificadoReprovadoError(f"{op} reprovada em: {', '.join(reprovados)}")
        return cls(op, nf, cliente, peso_kg, emissao, list(resultados))
