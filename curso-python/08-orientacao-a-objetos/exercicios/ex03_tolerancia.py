"""
Exercício 08.03 — Tolerância com mínimo, máximo ou os dois
Nível: ★☆☆

Contexto: Nem toda tolerância tem os dois limites. Espessura tem faixa (mín e máx),
tração só tem mínimo ("pelo menos 20 MPa") e COF às vezes só tem máximo.

Tarefa: complete a classe `Tolerancia`.
1. `__init__(self, minimo=None, maximo=None)` guarda `minimo` e `maximo` (None =
   sem limite daquele lado). Levante ValueError se os dois forem None, ou se os dois
   existirem e minimo > maximo.
2. `aprova(valor)` devolve True se o valor respeita os limites que existem
   (limites inclusos).
3. `descricao()` devolve:
   - com os dois limites: "0.10 a 0.30"
   - só mínimo: "mín. 20.00"
   - só máximo: "máx. 0.30"
   (números com 2 casas)

Exemplos:
    >>> Tolerancia(0.10, 0.30).aprova(0.31)
    False
    >>> Tolerancia(minimo=20).aprova(35.2)
    True
    >>> Tolerancia(maximo=0.3).descricao()
    'máx. 0.30'

Dica: teste "is None" / "is not None" (zero é um limite válido!).

Teste com:  python curso.py testar 08 ex03
"""


class Tolerancia:
    """Limites de aceitação de um ensaio."""

    def __init__(self, minimo: float | None = None, maximo: float | None = None) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def aprova(self, valor: float) -> bool:
        """True se o valor respeita os limites existentes."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    def descricao(self) -> str:
        """Texto da tolerância para o certificado."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
