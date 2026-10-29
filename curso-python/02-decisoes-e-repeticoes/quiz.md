# Quiz do módulo 02 — Decisões e repetições

Responda sem rodar o código. Para os laços, faça o teste de mesa no papel. Só depois confira o gabarito no final (e rode os trechos no REPL).

---

**1.** O que este código imprime?

```python
print(7 >= 7, 7 > 7, "a" == "A")
```

**2.** Qual condição verifica corretamente se `linha` é `"A"` ou `"B"`?

a) `linha == "A" or "B"`
b) `linha == "A" or linha == "B"`
c) `linha == ("A" or "B")`
d) `linha in "AB"`

**3.** A média é 8,5. O que este código imprime?

```python
nota = 8.5
if nota >= 5:
    print("Recuperação")
elif nota >= 7:
    print("Aprovado")
else:
    print("Reprovado")
```

**4.** Quais destes valores são falsy (contam como falso num `if`)?

`0`   `"0"`   `""`   `" "`   `None`   `[]`   `-1`

**5.** O que este código imprime?

```python
status = "OK" if 0 else "FORA"
print(status)
```

**6.** Quais números `range(10, 0, -3)` gera?

a) 10, 7, 4, 1
b) 10, 7, 4, 1, 0
c) 10, 7, 4
d) nenhum: `range` não aceita passo negativo

**7.** Quantas vezes o `print` é executado?

```python
for linha in "AB":
    for turno in range(3):
        print(linha, turno)
```

**8.** O que este código imprime?

```python
total = 0
for n in range(1, 6):
    if n == 4:
        break
    if n % 2 == 0:
        continue
    total += n
print(total)
```

**9.** Onde está o defeito? O que acontece ao rodar?

```python
contador = 10
while contador > 0:
    print(contador)
    contador += 1
```

**10.** O que este código imprime?

```python
soma = 0
for valor in [10, 20, 30]:
    soma = 0
    soma += valor
print(soma)
```

**11.** O código abaixo deveria mostrar o maior valor da lista. O que ele imprime, e qual é o defeito?

```python
valores = [-5, -2, -9]
maior = 0
for v in valores:
    if v > maior:
        maior = v
print(maior)
```

**12.** O código abaixo dá erro quando o usuário digita `25`. Qual erro e por quê?

```python
leitura = input("Espessura: ")
if leitura < 30:
    print("Abaixo de 30")
```

**13.** O que este código imprime?

```python
codigo = "b"
match codigo.upper():
    case "A" | "B":
        print("5%")
    case "C":
        print("8%")
    case _:
        print("?")
```

**14.** Uma variável `variacao` pode valer `None` (não medido) ou um número, inclusive `0.0`. Qual teste diz corretamente se ela **foi medida**?

a) `if variacao:`
b) `if variacao != 0:`
c) `if variacao is not None:`
d) `if variacao == "":`

**15.** O que este código imprime?

```python
x = 0
while x < 10:
    x += 3
print(x)
```

---

## Gabarito

1. **`True False False`.** 7 é maior **ou igual** a 7 (verdade), mas não é estritamente maior. E texto diferencia maiúsculas de minúsculas.

2. **b) `linha == "A" or linha == "B"`.** A opção a) é sempre verdadeira, porque `"B"` sozinho é truthy. A c) calcula `"A" or "B"` primeiro (dá `"A"`), então só aceita `"A"`. A d) aceita `"A"` e `"B"`, mas também `""` e `"AB"`, porque ambos estão "dentro" de `"AB"`.

3. **`Recuperação`.** O Python testa de cima para baixo e executa só o primeiro bloco verdadeiro. Como `8.5 >= 5` é verdade, o `elif nota >= 7` nem é testado. A ordem correta testa `>= 7` antes de `>= 5`.

4. **`0`, `""`, `None` e `[]`.** `"0"` e `" "` são textos **não vazios** (truthy), e `-1` é um número diferente de zero (truthy).

5. **`FORA`.** `0` é falsy, então a expressão condicional escolhe o valor do `else`.

6. **a) 10, 7, 4, 1.** Começa em 10 e soma -3 a cada passo. O próximo seria -2, que já passou do fim (0). O fim nunca entra, e passo negativo é permitido.

7. **6 vezes.** O laço de dentro roda inteiro (3 voltas) para cada volta do de fora (2 linhas): 2 × 3 = 6.

8. **`4`.** Teste de mesa: n=1 é ímpar, total = 1; n=2 é par, `continue` pula; n=3 é ímpar, total = 4; n=4 dispara o `break` antes de qualquer outra coisa. O 5 nunca é visto.

9. **Loop infinito.** O contador começa em 10 e **aumenta** (`+= 1`), então `contador > 0` nunca fica falso. O programa imprime números sem parar até você apertar `Ctrl+C`. O certo é `contador -= 1`.

10. **`30`.** O acumulador é zerado **dentro** do laço, a cada volta. No fim, só sobra o último valor. `soma = 0` deve ficar antes do `for` (e aí o resultado seria 60).

11. **Imprime `0`**, um valor que nem está na lista. Como todos os valores são negativos, nenhum é maior que o valor inicial 0. O certo é começar com `maior = None` e testar `if maior is None or v > maior:`. Resposta correta: -2.

12. **`TypeError: '<' not supported between instances of 'str' and 'int'`.** `input()` sempre devolve texto (`"25"`), e o Python não compara texto com número usando `<`. Converta antes: `leitura = float(input("Espessura: "))` (e, num programa de verdade, valide antes de converter).

13. **`5%`.** `"b".upper()` vira `"B"`, que casa com o caso `"A" | "B"`.

14. **c) `if variacao is not None:`.** A opção a) trata `0.0` (uma medição válida) como "não medido", porque `0.0` é falsy. A b) também rejeita o zero. A d) compara com texto vazio, que não tem nada a ver com `None`.

15. **`12`.** x passa por 3, 6, 9 e 12. Com 9 a condição `9 < 10` ainda é verdadeira, então soma mais 3. Só com 12 o laço termina. O `while` testa a condição **antes** de cada volta, não depois de cada soma.
