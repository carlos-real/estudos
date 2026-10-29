# Quiz do módulo 01 — Fundamentos

Responda sem rodar o código. Anote suas respostas e só depois confira o gabarito no final (e rode os trechos no REPL para ver com seus olhos).

---

**1.** O que este código imprime?

```python
print("A", "B", sep="", end="-")
print("C")
```

a) `A B-C`
b) `AB-C`
c) `AB` numa linha e `-C` na outra
d) `A B C`

**2.** Qual é o tipo do resultado de `7 / 7`?

a) `int`
b) `float`
c) `str`
d) `bool`

**3.** O que este código imprime?

```python
print(17 // 5, 17 % 5)
```

**4.** Qual expressão calcula corretamente a média de `a`, `b` e `c`?

a) `a + b + c / 3`
b) `(a + b + c) / 3`
c) `a + b + (c / 3)`
d) `(a + b) + c / 3`

**5.** O que este código imprime?

```python
x = 10
x += 5
x *= 2
print(x)
```

**6.** Onde está o erro? Qual mensagem aparece e como corrigir?

```python
quantidade = 8
print("Bobinas: " + quantidade)
```

**7.** O que `print("25" * 2)` imprime?

a) `50`
b) `2525`
c) `25 25`
d) dá erro

**8.** Qual destas conversões dá `ValueError`?

a) `int("42")`
b) `float("25.4")`
c) `int("25.4")`
d) `float("7")`

**9.** O que este código imprime?

```python
codigo = "  lote-07 "
codigo.strip().upper()
print(codigo)
```

a) `LOTE-07`
b) `lote-07`
c) o texto original, sem nenhuma mudança (com os espaços e em minúsculas)
d) dá erro

**10.** O que este código imprime?

```python
print(f"{1234.5:,.2f} | {0.075:.1%} | {5:03d}")
```

**11.** O que `round(2.5)` e `round(3.5)` devolvem, nessa ordem?

a) `3` e `4`
b) `2` e `4`
c) `2` e `3`
d) `3` e `3`

**12.** Qual é o jeito certo de verificar se `0.1 + 0.2` é "igual" a `0.3`?

a) imprimir `0.1 + 0.2` e conferir no olho
b) `math.isclose(0.1 + 0.2, 0.3)`
c) `int(0.1 + 0.2)`
d) `str(0.1 + 0.2)`

**13.** A expedição tem 43 bobinas e cabem 6 por caixa. Qual expressão dá o número de caixas necessárias?

a) `43 // 6`
b) `round(43 / 6)`
c) `math.ceil(43 / 6)`
d) `43 % 6`

**14.** O que acontece ao rodar este código?

```python
def area(largura, comprimento):
    print(largura * comprimento)


total = area(2, 3) + 1
```

**15.** Qual nome de variável segue as convenções do Python?

a) `PesoLiquido`
b) `peso-liquido`
c) `peso_liquido_kg`
d) `pesoLíquido`

---

## Gabarito

1. **b) `AB-C`.** `sep=""` junta os valores sem espaço, e `end="-"` troca a quebra de linha por um hífen. Por isso o `C` do segundo `print` fica colado na mesma linha.

2. **b) `float`.** A divisão `/` sempre devolve float, mesmo quando a conta é exata: `7 / 7` dá `1.0`. Para um inteiro, use `//`.

3. **`3 2`.** O 5 cabe 3 vezes inteiro no 17 (`17 // 5 = 3`) e sobram 2 (`17 % 5 = 2`). Prova real: 3 × 5 + 2 = 17.

4. **b) `(a + b + c) / 3`.** Sem os parênteses, a divisão é feita antes da soma, e só o `c` é dividido por 3. As opções a, c e d calculam a mesma coisa errada.

5. **`30`.** `x` começa em 10, `x += 5` faz virar 15 e `x *= 2` faz virar 30.

6. **Linha 2: `TypeError: can only concatenate str (not "int") to str`.** O `+` não junta texto com número. Corrija com `"Bobinas: " + str(quantidade)` ou, melhor, `f"Bobinas: {quantidade}"`.

7. **b) `2525`.** `"25"` é texto, e texto multiplicado por inteiro é repetido. Se fosse o número `25 * 2`, daria `50`.

8. **c) `int("25.4")`.** `int()` não aceita texto com casas decimais: dá `ValueError: invalid literal for int() with base 10: '25.4'`. Use `float("25.4")`.

9. **c) o texto original, sem mudança.** Strings são imutáveis: `strip()` e `upper()` criaram um texto novo (`"LOTE-07"`), mas ninguém guardou o resultado. O certo seria `codigo = codigo.strip().upper()`.

10. **`1,234.50 | 7.5% | 005`.** `:,.2f` põe separador de milhar (padrão americano) e 2 casas; `:.1%` multiplica por 100 e mostra 1 casa; `:03d` completa com zeros até 3 dígitos.

11. **b) `2` e `4`.** No empate (.5), o `round` vai para o número **par** mais próximo (arredondamento do banqueiro).

12. **b) `math.isclose(0.1 + 0.2, 0.3)`.** `0.1 + 0.2` dá `0.30000000000000004` por causa da representação binária do float. `math.isclose` considera "praticamente iguais" e devolve `True`. Olhar no olho (a) não serve para um programa; c e d nem comparam nada.

13. **c) `math.ceil(43 / 6)`.** `43 / 6` dá 7,17. Sete caixas não bastam (sobra 1 bobina), então é preciso arredondar **sempre para cima**: 8. `43 // 6` e `round(43 / 6)` dão 7, e `43 % 6` dá 1, que é a sobra, não o total de caixas.

14. **Imprime `6` e depois dá `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`.** A função imprime o resultado, mas não tem `return`, então devolve `None`. E `None + 1` não existe. Se o resultado vai ser usado em outra conta, a função precisa de `return largura * comprimento`.

15. **c) `peso_liquido_kg`.** snake_case, sem acento e com a unidade no nome. `PesoLiquido` é o estilo de nomes de classe (módulo 08); `peso-liquido` é lido como `peso - liquido` (uma subtração); `pesoLíquido` mistura estilo de outra linguagem com acento.
