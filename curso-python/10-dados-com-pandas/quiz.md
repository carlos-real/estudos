# Quiz — Módulo 10: pandas, Excel e gráficos

Responda sem rodar. Depois confira no gabarito (e, na dúvida, rode no REPL). Em todas as
perguntas, considere `import pandas as pd`.

**1.** Um CSV salvo pelo Excel brasileiro tem a linha `024412;38,1;1.558,5`. Quais
parâmetros do `read_csv` fazem `1.558,5` virar o número `1558.5`?

- a) `decimal=","`
- b) `decimal=","` e `thousands="."`
- c) `sep=";"`
- d) `dtype=float`

**2.** O que este código imprime?

```python
s = pd.Series([3, 1, 2])
print(s[s > 1].tolist())
```

**3.** `df` tem 5 linhas, com índice 0, 1, 2, 3, 4. O que este código imprime?

```python
print(len(df.iloc[1:3]), len(df.loc[1:3]))
```

**4.** Onde está o erro?

```python
fora = df[df["linha"] == "A" and df["cof"] > 0.30]
```

**5.** Depois deste código, a coluna `status` da tabela `df` muda? Por quê? Como
escrever do jeito certo?

```python
df[df["cof"] > 0.35]["status"] = "FORA"
```

**6.** O que este código imprime?

```python
print(pd.Series([True, False, True, True]).mean())
```

**7.** O que este código imprime?

```python
t = pd.DataFrame({"linha": ["A", "B", "A"], "cof": [0.2, None, 0.4]})
print(t.groupby("linha").size().tolist(), t.groupby("linha")["cof"].count().tolist())
```

**8.** Você quer conferir medições contra especificações e **nenhuma medição pode
sumir**, mesmo sem especificação. Qual `how` usar no `merge`?

- a) `"inner"`
- b) `"left"` (medições à esquerda)
- c) `"right"` (medições à esquerda)
- d) tanto faz

**9.** O que este código imprime?

```python
a = pd.DataFrame({"op": ["1", "2", "3"]})
b = pd.DataFrame({"op": ["1", "3"], "cliente": ["x", "y"]})
print(len(a.merge(b, on="op")), len(a.merge(b, on="op", how="left")))
```

**10.** `pd.to_datetime(pd.Series(["03/07/2026"]))` (sem `format`) dá qual data?

- a) 3 de julho de 2026
- b) 7 de março de 2026
- c) erro
- d) depende do Windows estar em português

**11.** Onde está o problema? O arquivo abre no Excel brasileiro com tudo numa coluna só
e os decimais com ponto.

```python
df.to_csv("relatorio.csv")
```

**12.** O que este código imprime?

```python
s = pd.Series(["1,5", "n/d", "2"]).str.replace(",", ".")
print(pd.to_numeric(s, errors="coerce").isna().sum())
```

**13.** Qual gráfico responde melhor "a espessura da linha D está estável ao longo do
mês?"

- a) pizza
- b) histograma
- c) gráfico de controle (valores na ordem de produção, média e limites ± 3σ)
- d) barras com a média de cada mês

**14.** No gráfico de controle do LAM-62, nenhum ponto saiu dos limites de controle, mas
3 bobinas ficaram fora da especificação (62 µm ± 7%). O que isso significa?

- a) O gráfico está errado: se há bobinas fora, o processo está fora de controle.
- b) O processo está estável, mas a variação natural dele é grande demais para a
  tolerância do cliente.
- c) As 3 bobinas são causas especiais e basta investigá-las.
- d) Os limites de controle deveriam ser iguais aos de especificação.

---

## Gabarito

1. **b.** `thousands="."` remove o ponto de milhar e `decimal=","` trata a vírgula como
   decimal. Só com `decimal`, o `1.558,5` continua texto.
2. **`[3, 2]`.** A máscara `s > 1` é `[True, False, True]`; o filtro mantém a ordem.
3. **`2 3`.** `iloc` usa posições e exclui o fim (1 e 2); `loc` usa rótulos e inclui o
   fim (1, 2 e 3).
4. **`and` não funciona com Series** (dá `ValueError: The truth value of a Series is
   ambiguous`). Use `&` e parênteses:
   `df[(df["linha"] == "A") & (df["cof"] > 0.30)]`.
5. **Não muda.** É atribuição encadeada: `df[mascara]` gera uma tabela que se comporta
   como cópia, e o valor é gravado nela. O certo:
   `df.loc[df["cof"] > 0.35, "status"] = "FORA"`.
6. **`0.75`.** True vale 1 e False vale 0: a média é a proporção de True (3 de 4).
7. **`[2, 1] [2, 0]`.** `size()` conta linhas (A tem 2, B tem 1); `count()` conta valores
   não vazios de `cof` (o de B é `None`).
8. **b.** `how="left"` mantém todas as linhas da tabela da esquerda; quem não casa fica
   com `NaN` nas colunas da direita. Com `inner`, as medições sem especificação sumiriam.
9. **`2 3`.** O `inner` só mantém as OPs "1" e "3"; o `left` mantém as três (a "2" fica
   com `cliente` vazio).
10. **b.** Sem `format`, o pandas assume mês/dia/ano. Use sempre `format="%d/%m/%Y"`.
11. **Faltam os parâmetros brasileiros.** O certo é
    `df.to_csv("relatorio.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")`
    (o `index=False` ainda evita a coluna 0, 1, 2...).
12. **`1`.** `"1,5"` vira `1.5`, `"2"` vira `2.0` e `"n/d"` vira `NaN` (por causa de
    `errors="coerce"`): um ausente.
13. **c.** Estabilidade ao longo do tempo é exatamente a pergunta do gráfico de controle.
    O histograma mostra a distribuição, mas perde a ordem no tempo.
14. **b.** Limites de controle são a "voz do processo"; os de especificação, a "voz do
    cliente". Processo sob controle com peças fora de especificação indica **capacidade**
    insuficiente: é preciso reduzir a variação (ou renegociar a tolerância), não caçar
    causa especial.
