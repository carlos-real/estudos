# Quiz do módulo 03 — Coleções

Responda no papel **antes** de rodar qualquer código. Depois confira no REPL e no gabarito do final.

## Perguntas

**1.** O que este código imprime?

```python
m = [10, 20, 30, 40]
print(m[1:3], m[-1])
```

**2.** Qual destes remove um item de uma lista **e devolve o item removido**?

- a) `lista.remove(x)`
- b) `lista.pop()`
- c) `del lista[0]`
- d) `lista.clear()`

**3.** O que este código imprime?

```python
a = [1, 2]
b = a
b.append(3)
print(len(a))
```

**4.** O que este código imprime?

```python
x = [[1], [2]]
y = x.copy()
y[0].append(9)
y.append([3])
print(x)
```

**5.** Onde está o erro? O que acontece ao rodar e como corrigir?

```python
notas = [8, 6, 9]
notas = notas.sort()
print("Menor nota:", notas[0])
```

**6.** O que este código imprime?

```python
op, *resto = ("OP-1", "A", 500.0)
print(resto)
```

**7.** O que `{}` cria?

- a) um conjunto vazio
- b) um dicionário vazio
- c) uma tupla vazia
- d) um erro de sintaxe

**8.** O que este código imprime?

```python
d = {"A": 1}
print(d.get("B", 0) + d.get("A", 0))
```

**9.** O que este código imprime?

```python
print(sorted({"OP-3", "OP-1"} - {"OP-1", "OP-2"}))
```

**10.** O que este código imprime?

```python
print([v * 2 for v in range(5) if v % 2 == 0])
```

**11.** Este código roda sem erro e imprime `2`. Qual é o problema, e como evitá-lo?

```python
ops = ["OP-1", "OP-2", "OP-3"]
pesos = [500.0, 320.5]
total = {op: p for op, p in zip(ops, pesos)}
print(len(total))
```

**12.** O que este código imprime?

```python
bobinas = [("OP-2", 300), ("OP-1", 500), ("OP-3", 300)]
print(sorted(bobinas, key=lambda b: (b[1], b[0]))[0])
```

**13.** Qual destes pode ser chave de dicionário?

- a) `[1, 2]`
- b) `{"a": 1}`
- c) `("A", 1)`
- d) `{1, 2}`

**14.** O que este código imprime?

```python
amostras = [
    {"linha": "A", "esp": 50},
    {"linha": "B", "esp": 20},
    {"linha": "A", "esp": 52},
]
g = {}
for a in amostras:
    g.setdefault(a["linha"], []).append(a["esp"])
print(g)
```

**15.** O que este código imprime?

```python
print(all([]), any([]))
```

---

## Gabarito

<details><summary>Ver respostas</summary>

**1.** `[20, 30] 40`. O fatiamento `[1:3]` pega os índices 1 e 2 (o 3 não entra). `[-1]` é o último.

**2.** b) `pop()` devolve o item removido. `remove` e `clear` devolvem `None`; `del` é um comando, não devolve nada.

**3.** `3`. `b = a` não copia: as duas variáveis apontam para a mesma lista.

**4.** `[[1, 9], [2]]`. `copy()` é cópia **rasa**: a lista de fora é nova (por isso o `[3]` não aparece em `x`), mas as listas de dentro são as mesmas (por isso o `9` aparece).

**5.** `notas.sort()` ordena no lugar e devolve `None`; a atribuição guarda `None` em `notas`. A linha do `print` dá `TypeError: 'NoneType' object is not subscriptable`. Correção: `notas.sort()` sozinho na linha, ou `notas = sorted(notas)`.

**6.** `['A', 500.0]`. O `*resto` recolhe o que sobrou, sempre como **lista**.

**7.** b) um dicionário vazio. Conjunto vazio é `set()`.

**8.** `1`. `get("B", 0)` devolve o padrão `0` (a chave não existe) e `get("A", 0)` devolve `1`.

**9.** `['OP-3']`. A diferença `-` mantém o que está no primeiro conjunto e não está no segundo.

**10.** `[0, 4, 8]`. O filtro deixa passar 0, 2 e 4; cada um é multiplicado por 2.

**11.** O `zip` parou na lista mais curta e a `OP-3` sumiu **sem aviso**. Use `zip(ops, pesos, strict=True)` (dá `ValueError` se os tamanhos forem diferentes) ou confira `len(ops) == len(pesos)` antes.

**12.** `('OP-2', 300)`. A key ordena pelo peso (crescente) e, no empate de 300, pela OP: `OP-2` vem antes de `OP-3`.

**13.** c) `("A", 1)`. Chaves precisam ser imutáveis. Listas, dicionários e conjuntos mudam, então dão `TypeError: unhashable type`.

**14.** `{'A': [50, 52], 'B': [20]}`. É o padrão de agrupamento: `setdefault` cria a lista na primeira vez e devolve a lista existente nas seguintes.

**15.** `True False`. `all` de nada é `True` ("nenhum item falhou") e `any` de nada é `False` ("nenhum item passou"). Cuidado com isso ao conferir listas que podem vir vazias: `all(dentro_da_faixa(v) for v in [])` diz "aprovado" para um lote sem medição nenhuma!

</details>
