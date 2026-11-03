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

from dataclasses import dataclass
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


class Certificado:
    """Certificado de qualidade de uma OP expedida."""

    def __init__(
        self,
        op: str,
        nf: str,
        cliente: str,
        peso_kg: float,
        emissao: date,
        resultados: list[ResultadoEnsaio] | None = None,
    ) -> None:
        # __init__ provisório: apague-o e transforme a classe numa dataclass
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta classe")

    @property
    def numero(self) -> str:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def aprovado(self) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def texto(self) -> str:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def salvar(self, pasta: Path) -> Path:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

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
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
