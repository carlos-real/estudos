"""Por que classes? O mesmo dado como dicionário e como objeto.

Rode com:  python exemplos/01_dict_vs_classe.py
"""

# --- Com dicionário: nada impede um erro de digitação ----------------------
amostra = {"codigo": "AM-001", "ensaio": "espessura", "valor": 25.3}
amostra["valro"] = 25.1  # erro de digitação: cria uma chave NOVA, em silêncio
print("Dicionário:", amostra)
print("Valor usado no laudo:", amostra["valor"], "(a correção se perdeu)")


# --- Com classe: dados e comportamento juntos ------------------------------
class Amostra:
    def __init__(self, codigo: str, ensaio: str, valor: float) -> None:
        self.codigo = codigo
        self.ensaio = ensaio
        self.valor = valor

    def esta_entre(self, minimo: float, maximo: float) -> bool:
        return minimo <= self.valor <= maximo


a = Amostra("AM-001", "espessura", 25.3)
print("\nObjeto:", a.codigo, a.ensaio, a.valor)
print("Dentro de 22,5 a 27,5?", a.esta_entre(22.5, 27.5))
print("Tipo:", type(a).__name__, "| é Amostra?", isinstance(a, Amostra))
try:
    print(a.valro)  # o erro de digitação aparece na hora
except AttributeError as erro:
    print("Erro:", erro)
