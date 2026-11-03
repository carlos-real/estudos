"""
Exercício 08.11 — Especificação e linha de produção (composição)
Nível: ★★★

Contexto: Esta é a regra central do Validador de Certificados. Cada linha de
produção (A, B, C, D) tem tolerâncias FIXAS (ex.: COF de 0,10 a 0,30) e uma
especificação PADRÃO (ex.: espessura 25 µm ± 10%). Algumas OPs têm especificação
PRÓPRIA (título + texto, pedida pelo cliente), que vale no lugar da padrão.
Uma linha "TEM UMA" especificação; ela não "É UMA" especificação. Isso é
composição, não herança.

A classe `Tolerancia` já está pronta. Tarefa:
1. `Especificacao(titulo, tolerancias, texto="")`: guarda `titulo`, `texto` e uma
   CÓPIA do dicionário {ensaio: Tolerancia} em `tolerancias` (mudar o dicionário
   original depois não pode afetar a especificação).
   - `avaliar(medidas)`: recebe {ensaio: valor} e devolve {ensaio: aprovado?} para
     cada ensaio DA ESPECIFICAÇÃO, na ordem dela. Ensaio da especificação que falta
     nas medidas -> KeyError. Medidas a mais são ignoradas.
   - `aprova(medidas)`: True se todos os ensaios foram aprovados.
2. `LinhaDeProducao(nome, fixas, padrao)`: `fixas` é {ensaio: Tolerancia} (guarde
   uma cópia) e `padrao` é uma Especificacao.
   - `cadastrar(op, especificacao)`: guarda a especificação própria da OP.
   - `tem_especificacao_propria(op)`: True/False.
   - `especificacao_para(op)`: a própria da OP, ou a padrão da linha.
   - `tolerancias_para(op)`: junta as fixas com as da especificação da OP (se o mesmo
     ensaio aparecer nas duas, vale a da especificação).
   - `avaliar(op, medidas)`: como Especificacao.avaliar, mas com tolerancias_para(op)
     (ordem: primeiro as fixas, depois os ensaios novos da especificação).

Exemplo:
    >>> padrao = Especificacao("Filme PE 25 µm", {"espessura": Tolerancia(22.5, 27.5)})
    >>> linha = LinhaDeProducao("B", {"cof": Tolerancia(0.10, 0.30)}, padrao)
    >>> linha.avaliar("OP245102", {"espessura": 25.4, "cof": 0.33})
    {'cof': False, 'espessura': True}
    >>> linha.cadastrar("OP245110", Especificacao("Cliente X", {"cof": Tolerancia(0.1, 0.4)}))
    >>> linha.avaliar("OP245110", {"cof": 0.33})
    {'cof': True}

Dica: {**a, **b} junta dois dicionários (b vence nos repetidos); dict(x) copia.

Teste com:  python curso.py testar 08 ex11
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tolerancia:
    """Faixa de aceitação (pronta: não precisa mexer)."""

    minimo: float
    maximo: float

    def aprova(self, valor: float) -> bool:
        return self.minimo <= valor <= self.maximo


class Especificacao:
    """Título, texto e tolerâncias de um produto."""

    def __init__(
        self, titulo: str, tolerancias: dict[str, Tolerancia], texto: str = ""
    ) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def avaliar(self, medidas: dict[str, float]) -> dict[str, bool]:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprova(self, medidas: dict[str, float]) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


class LinhaDeProducao:
    """Linha com tolerâncias fixas, especificação padrão e especificações por OP."""

    def __init__(self, nome: str, fixas: dict[str, Tolerancia], padrao: Especificacao) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def cadastrar(self, op: str, especificacao: Especificacao) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def tem_especificacao_propria(self, op: str) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def especificacao_para(self, op: str) -> Especificacao:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def tolerancias_para(self, op: str) -> dict[str, Tolerancia]:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def avaliar(self, op: str, medidas: dict[str, float]) -> dict[str, bool]:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
