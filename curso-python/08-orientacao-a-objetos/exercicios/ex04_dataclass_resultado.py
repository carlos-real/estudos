"""
Exercício 08.04 — Resultado de ensaio com @dataclass
Nível: ★☆☆

Contexto: Uma classe que só guarda dados precisa de __init__, __repr__ e __eq__,
quase sempre iguais. A @dataclass escreve tudo isso para você a partir da lista de
campos.

Tarefa: transforme `ResultadoEnsaio` numa dataclass (apague o __init__ provisório)
com os campos, nesta ordem:
    ensaio: str
    valor: float
    unidade: str = ""
    aprovado: bool = True
e escreva o método `rotulo()`, que devolve:
    "espessura: 25.30 µm (aprovado)"   ou   "cof: 0.32 (reprovado)"
(valor com 2 casas; sem unidade, não sobra espaço).

Exemplos:
    >>> r = ResultadoEnsaio("cof", 0.32, aprovado=False)
    >>> r
    ResultadoEnsaio(ensaio='cof', valor=0.32, unidade='', aprovado=False)
    >>> r.rotulo()
    'cof: 0.32 (reprovado)'
    >>> ResultadoEnsaio("cof", 0.32) == ResultadoEnsaio("cof", 0.32)
    True

Dica: from dataclasses import dataclass. Campos com valor padrão vêm depois dos
campos sem padrão.

Teste com:  python curso.py testar 08 ex04
"""


class ResultadoEnsaio:
    """Resultado de um ensaio, pronto para o certificado."""

    def __init__(
        self, ensaio: str, valor: float, unidade: str = "", aprovado: bool = True
    ) -> None:
        # __init__ provisório: apague-o e transforme a classe numa @dataclass
        # Escreva seu código aqui
        raise NotImplementedError("Implemente esta classe")

    def rotulo(self) -> str:
        """Texto do resultado para o certificado."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
