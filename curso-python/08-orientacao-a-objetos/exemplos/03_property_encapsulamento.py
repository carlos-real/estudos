"""Encapsulamento com _ e @property com validação.

Rode com:  python exemplos/03_property_encapsulamento.py
"""


class Amostra:
    def __init__(self, codigo: str, valor: float) -> None:
        self._codigo = codigo.upper()  # "_": interno, use a property
        self.valor = valor  # já passa pelo setter (validação desde o início)

    @property
    def codigo(self) -> str:
        return self._codigo  # sem setter: só leitura

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, novo: float) -> None:
        if novo < 0:
            raise ValueError(f"Valor não pode ser negativo: {novo}")
        self._valor = float(novo)

    @property
    def em_mils(self) -> float:
        """Propriedade calculada: espessura em mils (1 mil = 25,4 µm)."""
        return round(self._valor / 25.4, 3)


a = Amostra("am-001", 25.4)
print(a.codigo, a.valor, a.em_mils)
a.valor = 30  # parece atributo, mas chama o setter
print("Novo valor:", a.valor)
try:
    a.valor = -5
except ValueError as erro:
    print("a.valor = -5     ->", erro)
try:
    a.codigo = "X"
except AttributeError as erro:
    print("a.codigo = 'X'   ->", erro)
