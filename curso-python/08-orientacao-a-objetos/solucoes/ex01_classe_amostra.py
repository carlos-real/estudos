"""
Exercício 08.01 — Sua primeira classe: Amostra
Nível: ★☆☆

Contexto: Até agora cada amostra do laboratório era um dicionário
{"codigo": ..., "ensaio": ..., "valor": ...}. Um erro de digitação na chave
("valro") passava despercebido. Uma classe junta os dados e o comportamento da
amostra num lugar só.

Tarefa: complete a classe `Amostra`.
1. `__init__(self, codigo, ensaio, valor, unidade="")` guarda os atributos:
   - `codigo`: sem espaços nas pontas e em MAIÚSCULAS ("am-001 " -> "AM-001");
   - `ensaio`: sem espaços nas pontas e em minúsculas;
   - `valor`: sempre float (25 vira 25.0);
   - `unidade`: como veio.
2. `descricao()` devolve "AM-001 | espessura = 25.30 µm" (valor com 2 casas). Sem
   unidade, termina no número: "AM-002 | cof = 0.25".
3. `esta_entre(minimo, maximo)` devolve True se minimo <= valor <= maximo.

Exemplos:
    >>> a = Amostra(" am-001 ", "Espessura", 25.3, "µm")
    >>> a.codigo, a.ensaio, a.valor
    ('AM-001', 'espessura', 25.3)
    >>> a.descricao()
    'AM-001 | espessura = 25.30 µm'
    >>> a.esta_entre(22.5, 27.5)
    True

Dica: dentro dos métodos, os dados do objeto estão em `self` (self.valor, ...).

Teste com:  python curso.py testar 08 ex01
"""


class Amostra:
    """Uma amostra ensaiada no laboratório."""

    def __init__(self, codigo: str, ensaio: str, valor: float, unidade: str = "") -> None:
        # O __init__ prepara o objeto recém-criado: normaliza e guarda em self.
        self.codigo = codigo.strip().upper()
        self.ensaio = ensaio.strip().lower()
        self.valor = float(valor)  # 25 (int) vira 25.0: o tipo fica sempre o mesmo
        self.unidade = unidade

    def descricao(self) -> str:
        """Texto curto para relatório."""
        texto = f"{self.codigo} | {self.ensaio} = {self.valor:.2f}"
        # Só acrescenta a unidade se houver uma (evita espaço sobrando no fim).
        return f"{texto} {self.unidade}" if self.unidade else texto

    def esta_entre(self, minimo: float, maximo: float) -> bool:
        """True se o valor está na faixa (limites inclusos)."""
        return minimo <= self.valor <= maximo
