"""Classe, objeto, __init__, self, métodos, __str__ e __repr__.

Rode com:  python exemplos/02_classe_amostra.py
"""


class Amostra:
    """Uma amostra ensaiada no laboratório."""

    laboratorio = "CQ Embalagens"  # atributo de CLASSE: um só, compartilhado

    def __init__(self, codigo: str, ensaio: str, valor: float, unidade: str = "") -> None:
        self.codigo = codigo.strip().upper()  # atributos de INSTÂNCIA: um por objeto
        self.ensaio = ensaio
        self.valor = float(valor)
        self.unidade = unidade

    def esta_entre(self, minimo: float, maximo: float) -> bool:
        return minimo <= self.valor <= maximo

    def __str__(self) -> str:  # para pessoas: print() e f-string
        return f"{self.codigo} | {self.ensaio} = {self.valor:.2f} {self.unidade}".rstrip()

    def __repr__(self) -> str:  # para programadores: REPL, listas, logs
        return f"Amostra({self.codigo!r}, {self.ensaio!r}, {self.valor!r}, {self.unidade!r})"


a1 = Amostra(" am-001", "espessura", 25.3, "µm")
a2 = Amostra("AM-002", "cof", 0.32)
print(a1)
print(a2)
print([a1, a2])
print("a1 aprovada?", a1.esta_entre(22.5, 27.5))
print("Mesmo que:", Amostra.esta_entre(a1, 22.5, 27.5))  # o que o Python faz por trás
print("Laboratório:", a1.laboratorio, "|", Amostra.laboratorio)
