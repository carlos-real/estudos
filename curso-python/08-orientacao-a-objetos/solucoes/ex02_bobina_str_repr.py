"""
Exercício 08.02 — Bobina com __str__ e __repr__
Nível: ★☆☆

Contexto: Ao imprimir uma bobina, o Python mostra algo como
<__main__.Bobina object at 0x7f...>, que não ajuda ninguém. Você quer um texto
amigável no relatório (print) e um texto técnico na depuração (REPL, listas, logs).

Tarefa: complete a classe `Bobina`.
1. `__init__(self, lote, numero, peso_kg)` guarda `lote` (str), `numero` (int) e
   `peso_kg` (float).
2. `codigo()` devolve o lote, um hífen e o número com 3 dígitos: "L2610-007".
3. `__str__` devolve o texto amigável: "Bobina L2610-007 (152.4 kg)" (peso com 1 casa).
4. `__repr__` devolve o texto técnico, que parece o código que cria o objeto:
   "Bobina(lote='L2610', numero=7, peso_kg=152.4)" (use !r nas f-strings).

Exemplos:
    >>> b = Bobina("L2610", 7, 152.4)
    >>> print(b)
    Bobina L2610-007 (152.4 kg)
    >>> b
    Bobina(lote='L2610', numero=7, peso_kg=152.4)
    >>> [b]
    [Bobina(lote='L2610', numero=7, peso_kg=152.4)]

Dica: f"{numero:03d}" completa com zeros à esquerda; f"{texto!r}" usa o repr (com aspas).

Teste com:  python curso.py testar 08 ex02
"""


class Bobina:
    """Uma bobina de filme produzida."""

    def __init__(self, lote: str, numero: int, peso_kg: float) -> None:
        self.lote = lote
        self.numero = int(numero)
        self.peso_kg = float(peso_kg)

    def codigo(self) -> str:
        """Código da bobina: lote-número (3 dígitos)."""
        return f"{self.lote}-{self.numero:03d}"

    def __str__(self) -> str:
        # Para PESSOAS: usado por print() e f"{bobina}".
        return f"Bobina {self.codigo()} ({self.peso_kg:.1f} kg)"

    def __repr__(self) -> str:
        # Para PROGRAMADORES: usado no REPL, dentro de listas e em logs.
        # Regra de ouro: se possível, parecer o código que recria o objeto.
        return f"Bobina(lote={self.lote!r}, numero={self.numero!r}, peso_kg={self.peso_kg!r})"
