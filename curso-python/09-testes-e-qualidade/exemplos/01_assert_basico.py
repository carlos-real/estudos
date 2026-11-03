"""assert: a peça mais simples de um teste.

Rode:  python exemplos/01_assert_basico.py
"""


def calcular_limites(nominal: float, tolerancia_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) de nominal ± tolerância em %."""
    margem = nominal * tolerancia_pct / 100
    return nominal - margem, nominal + margem


# 1) assert verdadeiro: não acontece NADA (silêncio = sucesso)
assert calcular_limites(20.0, 5.0) == (19.0, 21.0)
print("1) assert verdadeiro passou em silêncio")

# 2) assert falso: levanta AssertionError
try:
    assert calcular_limites(20.0, 5.0) == (18.0, 22.0)
except AssertionError:
    print("2) assert falso levantou AssertionError (sem mensagem)")

# 3) assert com mensagem: depois da vírgula vem o texto que aparece no erro
try:
    minimo, maximo = calcular_limites(20.0, 5.0)
    assert minimo == 18.0, f"mínimo errado: esperava 18.0, veio {minimo}"
except AssertionError as erro:
    print(f"3) mensagem do erro: {erro}")

# 4) Cuidado com float: 0.1 + 0.2 não é exatamente 0.3
print(f"4) 0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}  (valor real: {0.1 + 0.2!r})")

# 5) Comparar float com tolerância (o pytest.approx faz isso por você)
assert abs((0.1 + 0.2) - 0.3) < 1e-9
print("5) com tolerância a comparação passa")
