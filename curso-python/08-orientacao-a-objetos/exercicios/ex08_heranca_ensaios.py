"""
Exercício 08.08 — Tipos de ensaio com herança e polimorfismo
Nível: ★★☆

Contexto: Todo ensaio tem nome, valor e unidade, e gera uma linha de laudo. O que
muda é a REGRA de aprovação: espessura tem faixa, tração tem mínimo, COF tem
máximo. A classe-mãe guarda o que é comum; cada filha define a sua regra.

Tarefa:
1. `Ensaio.__init__(self, nome, valor, unidade="")` guarda os três atributos
   (valor como float).
2. `Ensaio.aprovado()` já está pronta: levanta NotImplementedError, porque cada tipo
   de ensaio define a sua regra. NÃO mexa nela.
3. `Ensaio.laudo()` devolve "espessura: 25.30 µm -> APROVADO" (ou REPROVADO), valor
   com 2 casas, sem espaço sobrando quando não há unidade ("cof: 0.32 -> REPROVADO").
   Ela chama self.aprovado(), e cada filha responde do seu jeito (polimorfismo).
4. As filhas chamam `super().__init__(nome, valor, unidade)` e guardam seus limites:
   - `EnsaioFaixa(nome, valor, minimo, maximo, unidade="")`: minimo <= valor <= maximo;
   - `EnsaioMinimo(nome, valor, minimo, unidade="")`: valor >= minimo;
   - `EnsaioMaximo(nome, valor, maximo, unidade="")`: valor <= maximo.
5. `reprovados(ensaios)` devolve os nomes dos ensaios reprovados, na ordem.

Exemplos:
    >>> EnsaioFaixa("espessura", 25.3, 22.5, 27.5, "µm").laudo()
    'espessura: 25.30 µm -> APROVADO'
    >>> EnsaioMaximo("cof", 0.32, 0.30).laudo()
    'cof: 0.32 -> REPROVADO'
    >>> reprovados([EnsaioMinimo("tração", 18, 20, "MPa"), EnsaioMaximo("cof", 0.2, 0.3)])
    ['tração']

Teste com:  python curso.py testar 08 ex08
"""


class Ensaio:
    """Base de todos os ensaios: dados comuns e o laudo."""

    def __init__(self, nome: str, valor: float, unidade: str = "") -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprovado(self) -> bool:
        """Cada tipo de ensaio define a sua regra (as filhas sobrescrevem)."""
        raise NotImplementedError("Cada tipo de ensaio define a sua regra de aprovação")

    def laudo(self) -> str:
        """Linha do laudo. Funciona para QUALQUER filha: é o polimorfismo."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


class EnsaioFaixa(Ensaio):
    """Ensaio com mínimo e máximo (espessura, gramatura)."""

    def __init__(
        self, nome: str, valor: float, minimo: float, maximo: float, unidade: str = ""
    ) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprovado(self) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


class EnsaioMinimo(Ensaio):
    """Ensaio com valor mínimo (tração, selagem)."""

    def __init__(self, nome: str, valor: float, minimo: float, unidade: str = "") -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprovado(self) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


class EnsaioMaximo(Ensaio):
    """Ensaio com valor máximo (COF)."""

    def __init__(self, nome: str, valor: float, maximo: float, unidade: str = "") -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprovado(self) -> bool:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")


def reprovados(ensaios: list[Ensaio]) -> list[str]:
    """Nomes dos ensaios reprovados, na ordem."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
