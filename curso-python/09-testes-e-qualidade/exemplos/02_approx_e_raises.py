"""pytest.approx e pytest.raises também funcionam fora de um teste.

Isso é ótimo para testar hipóteses no REPL antes de escrever o teste de verdade.
Rode:  python exemplos/02_approx_e_raises.py
"""

import pytest

# approx: compara números com uma tolerância relativa padrão de 1 milionésimo
print("0.1 + 0.2 == approx(0.3)?", 0.1 + 0.2 == pytest.approx(0.3))
print("20.1 == approx(20.0)?     ", 20.1 == pytest.approx(20.0))

# Você pode escolher a tolerância: abs = absoluta, rel = relativa
print("20.1 == approx(20.0, abs=0.2)?", 20.1 == pytest.approx(20.0, abs=0.2))
print("20.1 == approx(20.0, rel=0.01)?", 20.1 == pytest.approx(20.0, rel=0.01))

# approx também entende listas, tuplas e dicionários de números
print("lista:", [0.1 + 0.2, 0.7 * 3] == pytest.approx([0.3, 2.1]))
print("dict: ", {"A": 0.1 + 0.2} == pytest.approx({"A": 0.3}))

# raises: confere que um bloco levanta a exceção esperada
with pytest.raises(ZeroDivisionError):
    print(10 / 0)  # a divisão falha antes de imprimir
print("raises: ZeroDivisionError capturado como esperado")

# match: confere também a mensagem (é uma expressão regular, usa re.search)
with pytest.raises(ValueError, match="could not convert"):
    float("12,5 kg")
print("raises + match: a mensagem bateu")

# excinfo: guarda a exceção para você inspecionar depois do bloco
with pytest.raises(ValueError) as excinfo:
    int("abc")
print("mensagem capturada:", excinfo.value)
