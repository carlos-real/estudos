# Quiz — Módulo 06: Arquivos e tratamento de erros

Responda sem rodar o código. Depois confira no gabarito e, na dúvida, teste no REPL.

**1.** Num traceback, onde está a informação mais importante para começar?

- a) Na primeira linha (`Traceback (most recent call last):`).
- b) Na última linha: o tipo da exceção e a mensagem.
- c) No meio, nas linhas de bibliotecas do Python.
- d) Em nenhum lugar: é preciso usar o depurador.

**2.** O que este código imprime?

```python
def f(texto):
    try:
        valor = int(texto)
    except ValueError:
        return "A"
    else:
        return "B"
    finally:
        print("C", end=" ")

print(f("7"), f("x"))
```

**3.** Onde está o problema deste código?

```python
def media(valores):
    try:
        return sum(valores) / len(valroes)
    except:
        return 0
```

**4.** O que é impresso?

```python
try:
    {"a": 1}["b"]
except LookupError as erro:
    print("pegou", type(erro).__name__, erro)
```

- a) Nada: `KeyError` não é capturado por `LookupError`.
- b) `pegou KeyError 'b'`
- c) `pegou LookupError b`
- d) `pegou KeyError b`

**5.** Qual é a forma correta de criar uma exceção própria para "valor fora da
tolerância", filha de uma base `ErroDeQualidade`?

- a) `ValorForaDaTolerancia = Exception("fora da tolerância")`
- b) `class ValorForaDaTolerancia(ErroDeQualidade): """Medição fora da faixa."""`
- c) `def ValorForaDaTolerancia(): raise ErroDeQualidade`
- d) `class ErroDeQualidade(ValorForaDaTolerancia): pass`

**6.** Para que serve o `from erro` em `raise ArquivoInvalido("...") from erro`?

**7.** Depois de rodar este código, o que tem dentro de `log.txt`?

```python
with open("log.txt", "w", encoding="utf-8") as a: a.write("1\n")
with open("log.txt", "a", encoding="utf-8") as a: a.write("2\n")
with open("log.txt", "w", encoding="utf-8") as a: a.write("3\n")
with open("log.txt", "a", encoding="utf-8") as a: a.write("4\n")
```

**8.** Com `p = Path("laudos") / "2025" / "linha_A.final.csv"`, quanto valem `p.name`,
`p.stem` e `p.suffix`?

**9.** Um CSV salvo pelo Excel como "CSV UTF-8" é lido com
`open(caminho, encoding="utf-8")` e `csv.DictReader(..., delimiter=";")`. Na hora de
acessar `linha["lote"]`, dá `KeyError: 'lote'`, embora a coluna exista. Qual é a causa
mais provável e a correção?

**10.** O que este código imprime?

```python
import csv
print(list(csv.reader(['A-1;"COF: liberado; ok";25,4'], delimiter=";")))
```

**11.** Por que se usa `newline=""` ao abrir um arquivo para gravar com o módulo `csv`?

- a) Para o arquivo não ter quebras de linha.
- b) Para o `csv` controlar as quebras de linha; sem isso, no Windows aparece uma linha
  em branco entre os registros.
- c) Para gravar em UTF-8.
- d) Porque o modo `"w"` exige.

**12.** O que este código imprime?

```python
import json
print(json.dumps({"faixa": (1, 2), "ok": None, "x": True}))
```

**13.** Você vai processar 40 CSVs de laudo de uma pasta. Um deles tem um número
digitado errado. O que é mais adequado?

- a) Um `try/except` em volta do `for` inteiro, para parar tudo no primeiro erro.
- b) `except:` sozinho dentro do `for`, ignorando qualquer problema em silêncio.
- c) `try/except` com os tipos esperados **dentro** do `for`, registrando o arquivo e a
  mensagem, e seguindo com os demais.
- d) Corrigir o arquivo à mão antes de rodar, porque programas não devem tratar erros.

**14.** Por que gravar primeiro em `regras.json.tmp` e depois fazer
`tmp.replace(destino)`?

---

## Gabarito

1. **b).** Leia de baixo para cima: a última linha diz **o que** aconteceu; as de cima,
   onde. Procure a primeira linha que é do seu código.
2. **`C C B A`.** O `finally` roda antes de cada função devolver seu valor, então os
   dois "C" aparecem primeiro (durante as chamadas). Depois o `print` mostra os
   retornos: `"B"` para `"7"` (veio pelo `else`) e `"A"` para `"x"`.
3. **O `except:` pega-tudo esconde o bug.** `valroes` é um erro de digitação
   (`NameError`), mas a função devolve `0` como se fosse uma média. Capture só o erro
   esperado (aqui, `ZeroDivisionError` para lista vazia).
4. **b) `pegou KeyError 'b'`.** `KeyError` é filha de `LookupError`, então é capturada.
   O `type(erro).__name__` mostra o tipo real, e a mensagem de um `KeyError` é a chave
   com aspas.
5. **b).** Uma exceção é uma classe filha de `Exception` (ou de outra exceção). A d)
   inverte a família.
6. **Encadear os erros.** O erro original (por exemplo, o `json.JSONDecodeError`) fica
   guardado em `__cause__`, e o traceback mostra os dois: o erro técnico e o erro com
   contexto que você criou.
7. **`3\n4\n`.** O terceiro `open` em `"w"` apagou o `1` e o `2`; o último `"a"`
   acrescentou o `4`.
8. **`'linha_A.final.csv'`, `'linha_A.final'` e `'.csv'`.** O `suffix` é só a última
   extensão; o `stem` é o nome sem ela.
9. **O BOM.** O "CSV UTF-8" do Excel começa com o BOM, que lido como `"utf-8"` fica
   grudado no primeiro nome de coluna (`'\ufefflote'`). Abra com `encoding="utf-8-sig"`.
10. **`[['A-1', 'COF: liberado; ok', '25,4']]`.** O `csv` respeita as aspas: o `;` de
    dentro da observação não separa colunas. Com `split(";")` sairiam 4 pedaços.
11. **b).** O módulo `csv` grava o fim de linha `\r\n` por conta própria. Sem
    `newline=""`, no Windows o Python ainda troca o `\n` por `\r\n` e fica `\r\r\n`.
12. **`{"faixa": [1, 2], "ok": null, "x": true}`.** Tupla vira lista, `None` vira
    `null` e `True` vira `true`.
13. **c).** Os laudos são independentes: um arquivo ruim não deve impedir a
    conferência dos outros 39, mas também não pode sumir em silêncio.
14. **Gravação atômica.** Se der erro (ou o programa cair) no meio da gravação, só o
    temporário fica estragado; o `regras.json` antigo continua inteiro. O `replace` troca
    um pelo outro de uma vez.
