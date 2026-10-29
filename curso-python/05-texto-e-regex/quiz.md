# Quiz — Módulo 05: Texto e expressões regulares

Responda sem rodar o código. Depois confira no gabarito e, na dúvida, teste no REPL.

**1.** O que este código imprime?

```python
print("lotes.csv".rstrip(".csv"))
```

- a) `lotes`
- b) `lote`
- c) `lotes.`
- d) Dá erro.

**2.** O que este código imprime?

```python
print(float("1.250"))
```

- a) `1250.0`
- b) `1.25`
- c) `1250`
- d) `ValueError`

**3.** Qual é o resultado de `" ".join("  embalagens   do  sul ".split())`?

- a) `' embalagens do sul '`
- b) `'embalagens   do  sul'`
- c) `'embalagens do sul'`
- d) `['embalagens', 'do', 'sul']`

**4.** Você quer saber se o texto **inteiro** digitado pelo operador é um código de OP.
Qual função usar?

- a) `re.search`
- b) `re.match`
- c) `re.fullmatch`
- d) `re.findall`

**5.** O que este código imprime?

```python
import re
print(re.findall(r"(\d+),(\d+)", "25,4 e 0,21"))
```

**6.** Onde está o erro? O que acontece ao rodar?

```python
import re
achado = re.search(r"NF:\s*(\d+)", "Nota ainda sem número")
print(achado.group(1))
```

**7.** O que este código imprime?

```python
print(f"[{'OK':^6}]")
```

**8.** Um relatório mostra `ExpediÃ§Ã£o`. O que provavelmente aconteceu?

- a) O arquivo estava em cp1252 e foi lido como UTF-8.
- b) O arquivo estava em UTF-8 e foi lido como cp1252.
- c) O texto tinha acentos decompostos (NFD).
- d) Faltou o `r` antes das aspas.

**9.** Quanto vale `len("ação".encode("utf-8"))`?

- a) 4
- b) 5
- c) 6
- d) 8

**10.** O que este código imprime?

```python
import re
texto = "OP-123456, OP 1234567, OP 654321"
print(re.findall(r"\bOP[ -]?(\d{6})\b", texto))
```

**11.** O que este código imprime?

```python
import re
print(re.sub(r"(\d{2})/(\d{2})", r"\2/\1", "05/03"))
```

**12.** Onde está o erro? Por que o primeiro `search` não acha nada?

```python
import re
padrao = re.compile(r"OP \d{6}", re.VERBOSE)
print(padrao.search("OP 123456"))   # None
print(padrao.search("OP123456"))    # acha!
```

**13.** Qual expressão transforma `1234.5` em `'1.234,50'`?

- a) `f"{1234.5:.2f}".replace(".", ",")`
- b) `f"{1234.5:,.2f}".replace(",", ".").replace(".", ",")`
- c) `f"{1234.5:,.2f}".translate(str.maketrans(",.", ".,"))`
- d) `str(1234.5).replace(".", ",")`

**14.** Para transformar o cabeçalho `"Gramatura (g/m²)"` em `"gramatura_g_m2"`, qual
normalização faz o `²` virar `2`?

- a) NFC
- b) NFD
- c) NFKD
- d) Nenhuma: precisa de `replace("²", "2")`.

---

## Gabarito

1. **b) `lote`.** `rstrip` recebe um **conjunto de caracteres**, não um sufixo. Ele tira
   do fim todos os `.`, `c`, `s`, `v` que encontrar, inclusive o `s` de "lotes". Para
   sufixo exato: `removesuffix(".csv")`.
2. **b) `1.25`.** Para o Python, o ponto é decimal. Um peso brasileiro de 1.250 kg vira
   1,25 kg sem erro nenhum. Por isso texto brasileiro sempre passa pela conversão.
3. **c) `'embalagens do sul'`.** `split()` sem argumento quebra em qualquer espaço e
   ignora repetições e pontas; `join` cola com um espaço só.
4. **c) `re.fullmatch`.** `search` acha o padrão em qualquer lugar; `match` só exige o
   começo. `fullmatch` exige que o texto inteiro case (o mesmo que `^...$`).
5. **`[('25', '4'), ('0', '21')]`.** Com dois grupos, `findall` devolve uma tupla por
   ocorrência, com o conteúdo de cada grupo.
6. **`AttributeError: 'NoneType' object has no attribute 'group'`.** O texto não tem
   "NF:", então `search` devolve `None`. Teste antes: `if achado: ...`.
7. **`[  OK  ]`.** `^6` centraliza "OK" em 6 caracteres (2 espaços de cada lado).
8. **b).** Cada letra acentuada virou duas letras estranhas: é UTF-8 lido como cp1252.
   O caso a) costuma dar `UnicodeDecodeError` ou o losango `�`. Conserto:
   `texto.encode("cp1252").decode("utf-8")`.
9. **c) 6.** "a" e "o" ocupam 1 byte cada; "ç" e "ã" ocupam 2 bytes cada em UTF-8.
10. **`['123456', '654321']`.** O `\b` depois dos dígitos impede casar os 6 primeiros
    dígitos de "1234567". O grupo faz o `findall` devolver só o número.
11. **`03/05`.** `\2` e `\1` reaproveitam os grupos na ordem trocada.
12. **No modo `VERBOSE`, espaços no padrão são ignorados.** O padrão vira `OP\d{6}`,
    que não aceita espaço. Para um espaço literal, use `\s`, `[ ]` ou `\ `.
13. **c).** A b) troca vírgula por ponto e depois **todos** os pontos por vírgula,
    dando `'1,234,50'`. A a) não tem separador de milhar (`'1234,50'`). A d) dá
    `'1234,5'`.
14. **c) NFKD.** A forma de compatibilidade simplifica caracteres "parecidos": `²` vira
    `2`, `ﬁ` vira `fi`. A NFD só separa letras e acentos.
