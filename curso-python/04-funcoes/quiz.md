# Quiz do módulo 04 — Funções

Responda no papel **antes** de rodar qualquer código. Depois confira no REPL e no gabarito do final.

## Perguntas

**1.** O que este código imprime?

```python
def f(x):
    x * 2

print(f(3))
```

**2.** Qual destes cabeçalhos dá erro de sintaxe?

- a) `def f(a, b=1):`
- b) `def f(a=1, b):`
- c) `def f(*args):`
- d) `def f(a, *, b=2):`

**3.** O que este código imprime?

```python
def adicionar(x, lista=[]):
    lista.append(x)
    return lista

adicionar(1)
print(adicionar(2))
```

**4.** O que este código imprime?

```python
x = 10

def f():
    x = 5
    return x

f()
print(x)
```

**5.** Onde está o erro? O que acontece ao rodar e como corrigir sem usar `global`?

```python
contador = 0

def registrar():
    contador += 1

registrar()
```

**6.** O que este código imprime?

```python
def f(*args, **kwargs):
    return len(args), list(kwargs)

print(f(1, 2, a=3))
```

**7.** O que este código imprime?

```python
def limites(n, p=10):
    return n - n * p / 100, n + n * p / 100

mi, ma = limites(50, p=4)
print(mi, ma)
```

**8.** Qual destas funções é **pura**?

- a) `def f(lista): lista.append(1); return lista`
- b) `def f(lista): return lista + [1]`
- c) `def f(x): print(x); return x`
- d) `def f(x): global total; total += x; return total`

**9.** O que este código imprime?

```python
def criar(m):
    def f(x):
        return x * m
    return f

dobro = criar(2)
triplo = criar(3)
print(dobro(5), triplo(5))
```

**10.** O que este código imprime?

```python
print(sorted(["bb", "a", "ccc", "B"], key=lambda s: (len(s), s.lower())))
```

**11.** O que este código imprime?

```python
def g(lista):
    lista = lista + [9]
    return len(lista)

nums = [1, 2]
print(g(nums), nums)
```

**12.** Onde está o erro? O que acontece ao chamar `soma_ate(3)` e como corrigir?

```python
def soma_ate(n):
    """Soma 1 + 2 + ... + n."""
    return n + soma_ate(n - 1)
```

**13.** O que este código imprime?

```python
def f(a, b):
    return a - b

print(f(b=1, a=5))
```

**14.** Pensando em decomposição, qual destes nomes de função indica que ela deveria ser quebrada em duas?

- a) `calcular_media`
- b) `ler_planilha_e_enviar_email`
- c) `formatar_linha`
- d) `esta_na_faixa`

---

## Gabarito

<details><summary>Ver respostas</summary>

**1.** `None`. A função calcula `x * 2` mas não devolve: falta o `return`. Toda função sem `return` devolve `None`.

**2.** b) Um parâmetro sem valor padrão não pode vir depois de um com padrão: `SyntaxError: parameter without a default follows parameter with a default`.

**3.** `[1, 2]`. A lista padrão é criada uma vez só, no `def`, e as duas chamadas usam a mesma. Correção: `lista=None` e `if lista is None: lista = []`.

**4.** `10`. O `x = 5` dentro da função cria uma variável **local**. O `x` global não muda.

**5.** `UnboundLocalError: cannot access local variable 'contador' where it is not associated with a value`. O `+=` torna `contador` local na função inteira, e ela é lida antes de ter valor. Correção: `def registrar(contador): return contador + 1` e, fora, `contador = registrar(contador)`.

**6.** `(2, ['a'])`. `*args` recolhe os posicionais numa tupla `(1, 2)`; `**kwargs` recolhe os nomeados num dicionário `{"a": 3}`, e `list()` de um dicionário dá as chaves.

**7.** `48.0 52.0`. O `p=4` substitui o padrão 10; a função devolve uma tupla, desempacotada em `mi` e `ma`.

**8.** b) `lista + [1]` cria uma lista nova e não mexe em nada de fora. A a) altera a lista recebida, a c) imprime e a d) altera uma global: todas têm efeitos colaterais.

**9.** `10 15`. Cada chamada de `criar` gera uma função que "lembra" o seu próprio `m` (closure).

**10.** `['a', 'B', 'bb', 'ccc']`. A key ordena pelo tamanho; no empate (`"a"` e `"B"`, tamanho 1), compara em minúsculas: `"a"` antes de `"b"`.

**11.** `3 [1, 2]`. `lista + [9]` cria uma lista nova e move só a etiqueta local; `nums` não é tocada.

**12.** Não há caso base: a função se chama para sempre (`n` vai a 0, -1, -2...) até `RecursionError: maximum recursion depth exceeded`. Correção: começar com `if n == 0: return 0` (ou `if n <= 0`).

**13.** `4`. Argumentos nomeados casam pelo nome, não pela ordem: `a=5`, `b=1`.

**14.** b) O "e" no nome denuncia duas tarefas (ler e enviar), e uma delas nem é cálculo: são dois efeitos colaterais diferentes. Quebre em `ler_planilha` e `enviar_email`, com o cálculo numa função pura no meio.

</details>
