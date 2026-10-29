# Módulo 02 — Decisões e repetições

> **Tempo estimado:** 10 a 12 horas · **Pré-requisitos:** módulos 00 e 01 · **Nível:** iniciante

## O que você vai aprender

Ao final deste módulo, você vai conseguir:

- comparar valores com `==`, `!=`, `<`, `>`, `<=` e `>=` e prever o resultado, inclusive com textos e floats;
- combinar condições com `and`, `or` e `not`, sem cair no erro `linha == "A" or "B"`;
- escrever `if`/`elif`/`else` na ordem certa para classificar um valor em faixas;
- usar a expressão condicional (`"OK" if dentro else "FORA"`);
- dizer quais valores são "falsos" (`0`, `0.0`, `""`, `None`, lista vazia) e quando usar `is None`;
- escrever um `match-case` com `|` e `_`, e saber quando ele é melhor que uma fila de `elif`;
- escrever um `while` com saída garantida, e reconhecer e interromper um loop infinito;
- percorrer uma string, um `range` e uma lista com `for`, sem errar o "um a mais, um a menos";
- usar `break` para parar uma busca e `continue` para pular dados ruins;
- implementar à mão os padrões contador, acumulador, busca e máximo/mínimo;
- escrever laços aninhados e calcular quantas vezes o laço de dentro roda;
- validar um dado digitado antes de convertê-lo, sem deixar o programa quebrar;
- fazer um teste de mesa para descobrir por que um laço não faz o que você queria.

## Por que isso importa

Até aqui, seus programas eram uma receita: linha 1, linha 2, linha 3, fim. A partir de agora eles **decidem** e **repetem**. É isso que faz um programa parecer inteligente.

Repare no projeto final, o validador de certificados. Ele é praticamente feito disto:

- **para cada** linha da planilha (repetição),
- **para cada** ensaio daquela amostra (repetição dentro de repetição),
- **se** o valor está fora da tolerância (decisão), marque como reprovado;
- **se** a OP tem especificação própria, use-a; **senão**, use o padrão da linha (decisão).

No mercado, lógica de programação é o primeiro filtro. Entrevistas técnicas para júnior quase sempre começam com "percorra esta lista e conte/encontre/some alguma coisa". Este módulo treina exatamente isso, à mão, sem atalhos. Atalhos como `sum()` e `max()` vêm no módulo 03, e você vai entendê-los muito melhor por ter feito o trabalho antes.

### Como estudar este módulo

O método é o mesmo do módulo 01 (PRIMM):

- 🔮 **Preveja antes de rodar:** escreva sua previsão **antes** de abrir a resposta.
- 🔧 **Modifique:** altere o exemplo e observe.
- **Exemplo resolvido:** leia o raciocínio passo a passo antes de tentar os parecidos.
- **Tente você:** mini exercício com resposta escondida.

Com laços, há uma técnica extra que vale ouro: o **teste de mesa** (seção 15). Quando um laço "não faz sentido", pegue papel e anote o valor de cada variável a cada volta.

## 1. Comparações: perguntas de sim ou não

Uma comparação é uma pergunta que o Python responde com `True` ou `False`, o tipo `bool` que você viu no módulo 01.

| Operador | Pergunta | Exemplo | Resultado |
|---|---|---|---|
| `==` | é igual? | `25 == 25.0` | `True` |
| `!=` | é diferente? | `"B" != "b"` | `True` |
| `<` | é menor? | `22.4 < 22.5` | `True` |
| `>` | é maior? | `27.6 > 27.5` | `True` |
| `<=` | é menor ou igual? | `22.5 <= 22.5` | `True` |
| `>=` | é maior ou igual? | `7 >= 7.5` | `False` |

```python
>>> espessura = 25.4
>>> espessura > 27.0
False
>>> espessura != 25
True
>>> resultado = espessura >= 23.0
>>> resultado
True
>>> type(resultado)
<class 'bool'>
```

O resultado de uma comparação é um valor como outro qualquer: dá para guardar numa variável, imprimir ou devolver com `return`.

> ⚠️ **Erro comum:** confundir `=` com `==`. Um `=` **guarda** um valor (atribuição). Dois `==` **perguntam** se são iguais. Escrever `if valor = 27:` dá `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`. O próprio Python sugere a correção.

### Comparação encadeada: igual à matemática

Para saber se um valor está numa faixa, o Python aceita a forma que você escreveria no caderno:

```python
>>> minimo = 23.0
>>> maximo = 27.0
>>> minimo <= 25.4 <= maximo
True
>>> minimo <= 27.0 <= maximo
True
>>> minimo <= 27.1 <= maximo
False
```

`23.0 <= valor <= 27.0` significa "valor maior ou igual a 23 **e** menor ou igual a 27". Repare que os limites contam como dentro, porque usamos `<=`. Na especificação de um cliente, isso faz diferença: confirme sempre se os limites são inclusivos.

### Comparando textos

Textos são comparados caractere por caractere, diferenciando maiúsculas e minúsculas:

```python
>>> "COF" == "cof"
False
>>> "COF" == "cof".upper()
True
>>> "abacaxi" < "banana"
True
```

> 🔮 **Preveja antes de rodar:** o que cada linha mostra?
>
> ```python
> print("10" < "9")
> print(10 < 9)
> print("25" == 25)
> ```

<details><summary>Resposta</summary>

```text
True
False
False
```

Na primeira linha os dois são **textos**: o Python compara o primeiro caractere de cada um, `"1"` com `"9"`, e `"1"` vem antes. Por isso `"10" < "9"` é `True`. É o mesmo motivo de alguns sistemas listarem `lote10` antes de `lote9`. Na segunda, números de verdade. Na terceira, texto nunca é igual a número, então dá `False` sem erro. Moral: converta antes de comparar (`float(texto)`).

</details>

E comparar texto com número usando `<` ou `>` nem funciona:

```python
>>> "25" < 30
Traceback (most recent call last):
  ...
TypeError: '<' not supported between instances of 'str' and 'int'
```

(Como no módulo 01, as linhas do meio dos tracebacks estão resumidas com `...`.)

### Comparando floats

Lembra do `0.1 + 0.2`? Ele volta aqui:

```python
>>> 0.1 + 0.2 == 0.3
False
>>> import math
>>> math.isclose(0.1 + 0.2, 0.3)
True
```

Para conferir se dois floats são "iguais", use `math.isclose`. Para faixas de tolerância (`<=` e `>=`), o problema quase nunca aparece, porque um erro na 17ª casa não muda o resultado de uma medição real.

**Tente você:** escreva uma comparação que diga se `peso_kg` está entre 980 e 1020, inclusive.

<details><summary>Resposta</summary>

```python
>>> peso_kg = 1003.5
>>> 980 <= peso_kg <= 1020
True
```

</details>

## 2. Combinando condições: and, or e not

| Operador | Resultado | Exemplo do laboratório |
|---|---|---|
| `a and b` | `True` só se **os dois** forem verdadeiros | espessura OK **e** COF OK |
| `a or b` | `True` se **pelo menos um** for verdadeiro | linha A **ou** linha B |
| `not a` | inverte: `True` vira `False` e vice-versa | **não** liberado |

A tabela completa (a "tabela-verdade"):

```text
  a      b     | a and b | a or b
 True   True   |  True   |  True
 True   False  |  False  |  True
 False  True   |  False  |  True
 False  False  |  False  |  False
```

```python
>>> espessura_ok = True
>>> cof_ok = False
>>> espessura_ok and cof_ok
False
>>> espessura_ok or cof_ok
True
>>> not cof_ok
True
>>> linha = "B"
>>> linha == "A" or linha == "B"
True
```

**Precedência:** `not` é resolvido primeiro, depois `and`, por último `or`. Igual ao módulo 01: na dúvida, parênteses. `(a and not b) or c` é muito mais legível que `a and not b or c`, mesmo que o resultado seja o mesmo.

### Curto-circuito: o Python para de olhar quando já sabe

Em `a and b`, se `a` é falso, o resultado já é falso, e o Python **nem avalia** `b`. Em `a or b`, se `a` é verdadeiro, ele nem olha `b`. Isso é útil para proteger contas perigosas:

```python
>>> pessoas = 0
>>> pessoas != 0 and 150 / pessoas > 30
False
```

Como `pessoas != 0` é falso, a divisão por zero nunca acontece. Se você inverter a ordem (`150 / pessoas > 30 and pessoas != 0`), vem `ZeroDivisionError`.

> 🔮 **Preveja antes de rodar:** a linha é `"C"`. O que este código imprime?
>
> ```python
> linha = "C"
> if linha == "A" or "B":
>     print("Tolerância de 5%")
> else:
>     print("Outra tolerância")
> ```

<details><summary>Resposta</summary>

Imprime `Tolerância de 5%`, que está **errado**. O Python não lê como "linha é A ou B". Ele lê `(linha == "A") or ("B")`. A primeira parte é `False`, mas a segunda é o texto `"B"`, que conta como verdadeiro (seção 5). Resultado: a condição é **sempre** verdadeira. O certo é repetir a comparação: `linha == "A" or linha == "B"`. Esse erro é tão comum que vale escrever num post-it.

</details>

> 💡 **Dica:** cuidado com o atalho `linha in "AB"`. Ele aceita `"A"` e `"B"`, mas também `""` (texto vazio) e `"AB"`, porque todos estão "dentro" de `"AB"`. No módulo 03 você vai ver o jeito certo com tuplas: `linha in ("A", "B")`.

## 3. if, elif e else: o programa decide

Pense num procedimento do laboratório escrito como fluxograma:

```text
           [COF medido]
                |
        COF < 0,20 ? ──sim──> "baixo: filme escorrega na envasadora"
                | não
        COF <= 0,40 ? ─sim──> "normal"
                | não
                └───────────> "alto: filme trava na máquina"
```

Em Python:

```python
cof = 0.47

if cof < 0.20:
    print("COF baixo: filme escorrega na envasadora")
elif cof <= 0.40:
    print("COF normal")
else:
    print("COF alto: filme trava na máquina")

print("Fim da avaliação")
```

Saída:

```text
COF alto: filme trava na máquina
Fim da avaliação
```

As regras:

- `if` testa a primeira condição. `elif` ("senão, se") testa a próxima. `else` ("senão") pega tudo que sobrou.
- Cada linha de condição termina com **dois-pontos** `:`.
- O bloco de cada caso é **recuado** (4 espaços). A indentação é que diz ao Python o que pertence a cada caso. O `print("Fim da avaliação")`, sem recuo, roda sempre.
- O Python testa **de cima para baixo** e executa **só o primeiro** bloco verdadeiro. Os outros são ignorados, mesmo que também fossem verdadeiros.
- `elif` e `else` são opcionais. Pode haver quantos `elif` você quiser e no máximo um `else`.

### Exemplo resolvido: a ordem dos elif importa

**Problema:** classificar a umidade relativa da sala de ensaios. Até 40%: "seca". Até 60%: "ideal". Acima de 60%: "úmida" (atrapalha o ensaio de COF).

**Primeira tentativa (errada):**

```python
umidade = 35
if umidade <= 60:
    print("ideal")
elif umidade <= 40:
    print("seca")
else:
    print("úmida")
```

Saída:

```text
ideal
```

35% deveria ser "seca". O que houve? `35 <= 60` é verdadeiro, então o primeiro bloco ganhou e o `elif` nem foi testado.

**Raciocínio da correção:** quando as faixas são "até X", testo da **menor** para a maior. Cada `elif` só é alcançado se os anteriores falharam, então nele eu já sei que o valor passou dos limites anteriores.

```python
umidade = 35
if umidade <= 40:
    print("seca")
elif umidade <= 60:  # aqui já sei que umidade > 40
    print("ideal")
else:  # aqui já sei que umidade > 60
    print("úmida")
```

Saída:

```text
seca
```

> 🔧 **Modifique:** teste com `40`, `41`, `60` e `61`. Os valores de fronteira são onde os bugs moram. Depois, reescreva testando da **maior** faixa para a menor (`if umidade > 60:` ...). As duas ordens funcionam, desde que você seja coerente.

### if dentro de if

Um bloco pode conter outro `if`. Use quando uma decisão só faz sentido depois de outra:

```python
cof = 0.32
liberado_pelo_cliente = True

if cof > 0.30:
    if liberado_pelo_cliente:
        print("COF acima do padrão, mas liberado pelo cliente.")
    else:
        print("COF acima do padrão: bloquear lote.")
else:
    print("COF dentro do padrão.")
```

Saída:

```text
COF acima do padrão, mas liberado pelo cliente.
```

> 💡 **Dica:** mais de dois ou três níveis de `if` aninhado fica difícil de ler. Muitas vezes `and` resolve: `if cof > 0.30 and not liberado_pelo_cliente:`. Outra saída é o **retorno antecipado** dentro de funções (seção 14).

> ⚠️ **Erro comum:** escrever `if aprovado == True:`. Funciona, mas é redundante: `aprovado` já é `True` ou `False`. Escreva `if aprovado:` e `if not aprovado:`.

**Tente você:** escreva um `if` que imprima `"par"` ou `"ímpar"` para um inteiro `n`.

<details><summary>Resposta</summary>

```python
n = 7
if n % 2 == 0:
    print("par")
else:
    print("ímpar")
```

O resto da divisão por 2 é 0 para os pares (módulo 01, seção 6).

</details>

## 4. Expressão condicional: um if numa linha

Quando a decisão serve só para **escolher entre dois valores**, existe uma forma curta:

```python
valor = 22.9
status = "OK" if 23.0 <= valor <= 27.0 else "FORA"
print(status)
print(f"Lote {'liberado' if status == 'OK' else 'retido'}")
```

Saída:

```text
FORA
Lote retido
```

Leia como em português: "status é `OK` **se** a condição for verdadeira, **senão** `FORA`". A forma geral é `valor_se_verdadeiro if condição else valor_se_falso`.

Use para escolhas simples. Se precisar de `elif` ou de mais de uma ação, volte ao `if` normal: legibilidade vem primeiro.

## 5. Truthy e falsy: o que conta como verdadeiro

O `if` aceita qualquer valor, não só `True` e `False`. O Python decide assim:

- **falsy** (contam como falso): `False`, `None`, `0`, `0.0`, `""` (texto vazio) e coleções vazias, como a lista vazia `[]`;
- **truthy** (contam como verdadeiro): todo o resto, inclusive `"0"`, `" "` (um espaço) e `-1`.

A função `bool()` mostra como o Python enxerga cada valor:

```python
>>> bool(0)
False
>>> bool("")
False
>>> bool(None)
False
>>> bool("0")
True
>>> bool(" ")
True
>>> bool(-1)
True
```

Isso permite testes curtos e muito usados:

```python
observacao = ""
if not observacao:
    print("Sem observação: usar o texto padrão da linha.")
```

Saída:

```text
Sem observação: usar o texto padrão da linha.
```

### None e o operador is

`None` significa "sem valor". Para perguntar se algo é `None`, use `is None` (ou `is not None`), e não `== None`. O `is` pergunta "é exatamente este objeto?", e só existe um `None`, então é a forma mais clara e segura:

```python
>>> especificacao = None
>>> especificacao is None
True
>>> especificacao is not None
False
```

> 🔮 **Preveja antes de rodar:** a balança mediu exatamente zero de variação de peso (a amostra não absorveu umidade nenhuma, ótimo resultado). O que é impresso?
>
> ```python
> variacao = 0.0
> if variacao:
>     print("Variação registrada:", variacao)
> else:
>     print("Sem medição!")
> ```

<details><summary>Resposta</summary>

Imprime `Sem medição!`, que está **errado**. `0.0` é falsy, então o `if variacao:` trata uma medição válida de zero como se não existisse. Quando "zero" é um valor legítimo e "ausente" é `None`, teste explicitamente: `if variacao is not None:`. Essa distinção vai importar muito ao ler planilhas (célula vazia vira `None`; célula com 0 vira `0`).

</details>

## 6. match-case: escolhendo entre vários casos

Quando você compara **a mesma variável** com uma lista de valores fixos, uma fila de `elif` fica repetitiva. O Python 3.10 trouxe o `match`:

```python
ensaio = " Gramatura "

match ensaio.strip().lower():
    case "espessura":
        unidade = "µm"
    case "gramatura":
        unidade = "g/m²"
    case "tração" | "tracao":
        unidade = "MPa"
    case "cof":
        unidade = "(adimensional)"
    case _:
        unidade = None

print("Unidade do ensaio:", unidade)
```

Saída:

```text
Unidade do ensaio: g/m²
```

- `match valor:` avalia o valor uma vez; cada `case` é um valor possível.
- `|` junta vários valores no mesmo caso (`"tração" | "tracao"` aceita com e sem acento).
- `case _:` é o "qualquer outra coisa", como o `else`. Se nenhum caso casar e não houver `_`, nada acontece.
- Só o primeiro caso que casar é executado (não existe o "vazamento" para o próximo, como em outras linguagens).

A mesma lógica com `if`:

```python
codigo = ensaio.strip().lower()
if codigo == "espessura":
    unidade = "µm"
elif codigo == "gramatura":
    unidade = "g/m²"
elif codigo == "tração" or codigo == "tracao":
    unidade = "MPa"
# ...e assim por diante
```

Quando usar cada um? `match` para "esta variável é qual destes valores fixos?" (menu de comandos, código de linha, tipo de ensaio). `if/elif` para faixas e condições variadas (`valor < minimo`, `cof > 0.30 and not liberado`).

> ⚠️ **Erro comum:** usar `match` no Python 3.9 ou anterior: dá `SyntaxError`. O curso pede Python 3.12+ (módulo 00), então você está coberto. Mas lembre disso se for rodar seu script num servidor antigo.

O match-case tem recursos bem mais poderosos (casar estruturas, capturar partes), que aparecem quando você conhecer listas e dicionários. Por ora, esta introdução cobre 90% do uso do dia a dia.

## 7. while: repetir enquanto for verdade

O `while` repete um bloco **enquanto** a condição for verdadeira. Pense na expedição: "**enquanto** houver bobina no palete, pegue a próxima e confira a etiqueta". Você não precisa saber de antemão quantas são.

Todo `while` saudável tem três partes:

```text
contador = 3               1) estado inicial
while contador > 0:        2) condição: testada ANTES de cada volta
    print("Faltam", contador)
    contador -= 1          3) atualização: aproxima a condição de ficar falsa
print("Partiu!")
```

```python
contador = 3
while contador > 0:
    print("Faltam", contador)
    contador -= 1
print("Partiu!")
```

Saída:

```text
Faltam 3
Faltam 2
Faltam 1
Partiu!
```

### Exemplo resolvido: quando comprar resina?

**Problema:** o estoque tem 5.000 kg de resina; a extrusora consome 380 kg por dia. O estoque de segurança é 1.000 kg. Em quantos dias o estoque cai abaixo do mínimo?

**Raciocínio:** é uma repetição "enquanto o estoque estiver acima ou igual ao mínimo, passe um dia". Preciso de um contador de dias (começa em 0) e de atualizar o estoque a cada volta. Quando o `while` terminar, o contador terá a resposta.

```python
estoque_kg = 5000.0
consumo_diario_kg = 380.0
estoque_seguranca_kg = 1000.0
dias = 0
while estoque_kg >= estoque_seguranca_kg:
    estoque_kg -= consumo_diario_kg
    dias += 1
print(f"Em {dias} dias o estoque cai para {estoque_kg:.0f} kg: hora de comprar.")
```

Saída:

```text
Em 11 dias o estoque cai para 820 kg: hora de comprar.
```

**Conferindo:** 5.000 − 11 × 380 = 820, abaixo de 1.000. Com 10 dias seriam 1.200, ainda acima. Bate.

> 🔧 **Modifique:** troque `consumo_diario_kg` para `0` e rode. O que acontece? (Use `Ctrl+C` para parar.) Depois, acrescente antes do `while` um `if` que avisa "consumo zero: o estoque nunca acaba" e evita o laço.

### Loop infinito

Se a condição nunca ficar falsa, o `while` roda para sempre. O programa parece travado, a ventoinha do notebook acelera. Causas típicas: esquecer a atualização (`contador -= 1`), atualizar na direção errada (`contador += 1`), ou um valor que torna a saída impossível (consumo zero, taxa zero).

Para interromper, aperte `Ctrl+C` no terminal. Com o exemplo do estoque e `consumo_diario_kg = 0.0`, o Python para e mostra:

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 5, in <module>
    while estoque_kg >= estoque_seguranca_kg:
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyboardInterrupt
```

`KeyboardInterrupt` não é bug do Python: é você interrompendo. A linha mostrada é onde o programa estava naquele instante, uma boa pista de qual laço não terminava.

> 💡 **Dica:** antes de escrever um `while`, responda: "o que, dentro do laço, faz a condição ficar falsa um dia?". Se não souber responder, há risco de loop infinito.

### while True com break: repetir até acontecer algo

Às vezes a condição de parada fica mais natural no meio do laço. O padrão é `while True:` (repetir sempre) com `break` (seção 10) para sair:

```python
while True:
    texto = input("Peso da bobina (ou 'fim'): ")
    if texto == "fim":
        break
    print("Registrado:", texto)
print("Encerrado.")
```

Uma execução:

```text
Peso da bobina (ou 'fim'): 125,5
Registrado: 125,5
Peso da bobina (ou 'fim'): 130
Registrado: 130
Peso da bobina (ou 'fim'): fim
Encerrado.
```

A palavra `"fim"` é uma **sentinela**: um valor especial que sinaliza "acabou". É o padrão de todo programa de terminal que lê dados até o usuário cansar, como o desafio deste módulo.

O exemplo `exemplos/04_while.py` tem ainda um "jogo de adivinhação" em que o computador acha um número de 1 a 100 em poucas tentativas, cortando a faixa pela metade a cada palpite (busca binária). Rode e veja quantas tentativas ele precisa.

## 8. for e range: repetir para cada item

O `for` percorre uma sequência, **um item por volta**. É o laço mais usado em Python. Com uma string, cada volta recebe um caractere:

```python
for letra in "COF":
    print("Letra:", letra)
```

Saída:

```text
Letra: C
Letra: O
Letra: F
```

A variável (`letra`) é criada pelo próprio `for` e recebe o próximo item a cada volta. Escolha um nome que diga o que ela é: `for letra in texto`, `for medicao in medicoes`.

### range: uma sequência de números

`range` gera números inteiros sob demanda. Ele tem três formas:

| Forma | Gera | Exemplo |
|---|---|---|
| `range(fim)` | 0, 1, ..., fim-1 | `range(3)` → 0, 1, 2 |
| `range(início, fim)` | início, ..., fim-1 | `range(1, 4)` → 1, 2, 3 |
| `range(início, fim, passo)` | de passo em passo | `range(20, 61, 10)` → 20, 30, 40, 50, 60 |

O **fim nunca entra**. É a fonte nº 1 de erros "um a mais, um a menos" (em inglês, *off-by-one*). Para ir de 1 a 10, use `range(1, 11)`.

```python
for bobina in range(1, 4):
    print(f"Bobina {bobina} de 3")
print("Contagem regressiva:", end=" ")
for n in range(5, 0, -1):
    print(n, end=" ")
print()
```

Saída:

```text
Bobina 1 de 3
Bobina 2 de 3
Bobina 3 de 3
Contagem regressiva: 5 4 3 2 1
```

> 🔮 **Preveja antes de rodar:** quais números são impressos?
>
> ```python
> for i in range(2, 11, 4):
>     print(i, end=" ")
> ```

<details><summary>Resposta</summary>

`2 6 10`. Começa em 2 e soma 4 a cada volta: 2, 6, 10. O próximo seria 14, que passa do fim (11). Repare que o 10 entrou porque é **menor** que 11; com `range(2, 10, 4)` ele não entraria.

</details>

> ⚠️ **Erro comum:** `range` só aceita inteiros. `range(2.5)` dá `TypeError: 'float' object cannot be interpreted as an integer`. E `for i in 10:` dá `TypeError: 'int' object is not iterable`: um número sozinho não é uma sequência; o certo é `for i in range(10):`.

### for ou while?

- **for**: quando você vai percorrer algo que já existe (os caracteres de um texto, os números de 1 a N, as medições de uma lista). O fim é garantido.
- **while**: quando você não sabe quantas voltas serão (até o estoque acabar, até o usuário digitar "fim", até o valor dobrar). Exige cuidado com a saída.

Na dúvida, prefira `for`: ele não tem como virar loop infinito.

## 9. Percorrendo uma lista recebida

Listas são o assunto do módulo 03. Para este módulo, bastam três linhas:

- `[24.8, 25.3, 25.1]` cria uma lista: vários valores, em ordem, entre colchetes;
- `for valor in valores:` percorre a lista, um valor por volta, do primeiro ao último;
- `len(valores)` diz quantos itens ela tem.

Nos exercícios, a lista chega pronta como **parâmetro da função**: você só percorre.

```python
pesos = [125.5, 130.2, 128.9]
total = 0.0
for peso in pesos:
    total += peso
print(f"{len(pesos)} bobinas, total {total:.1f} kg")
```

Saída:

```text
3 bobinas, total 384.6 kg
```

Precisa saber a **posição** de cada item (1ª, 2ª, 3ª)? Use um contador que aumenta a cada volta:

```python
medicoes = [24.8, 25.3, 25.1]
posicao = 0
for medicao in medicoes:
    posicao += 1
    print(f"Medição {posicao}: {medicao} µm")
```

Saída:

```text
Medição 1: 24.8 µm
Medição 2: 25.3 µm
Medição 3: 25.1 µm
```

(No módulo 03 você vai conhecer o `enumerate`, que faz isso sozinho.)

## 10. break e continue: controlando o laço por dentro

- `break` **encerra** o laço imediatamente. O programa segue na primeira linha depois do laço.
- `continue` **pula o resto desta volta** e vai direto para a próxima.

```python
medicoes = [25.1, 0.0, 24.8, 31.2, 25.0, -1.0, 26.9]

print("Medições válidas:", end=" ")
for valor in medicoes:
    if valor <= 0:
        continue
    print(valor, end=" ")
print()

posicao = 0
for valor in medicoes:
    posicao += 1
    if valor > 27:
        print(f"Primeira acima de 27 µm: {valor} (posição {posicao}).")
        break
print("Fim da inspeção.")
```

Saída:

```text
Medições válidas: 25.1 24.8 31.2 25.0 26.9
Primeira acima de 27 µm: 31.2 (posição 4).
Fim da inspeção.
```

No primeiro laço, `continue` pula as falhas de leitura (zero e negativo) sem imprimir. No segundo, `break` encerra a busca assim que acha o primeiro valor acima de 27: não faz sentido continuar olhando.

> 🔮 **Preveja antes de rodar:** o que é impresso?
>
> ```python
> codigo = ""
> for caractere in "OP-12.3":
>     if caractere == "-" or caractere == ".":
>         continue
>     if caractere == "3":
>         break
>     codigo += caractere
> print(codigo)
> ```

<details><summary>Resposta</summary>

`OP12`. O `-` e o `.` são pulados pelo `continue`. As letras `O`, `P`, `1` e `2` são acumuladas. Quando chega o `3`, o `break` encerra o laço **antes** de acumular o `3`.

</details>

> 💡 **Dica:** dentro de uma função, `return` também encerra o laço (e a função inteira). Em buscas, `return posicao` no momento em que acha é muitas vezes mais claro do que `break` mais uma variável auxiliar.

## 11. Contadores e acumuladores

Dois padrões aparecem em quase todo laço:

- **contador**: começa em `0` e soma `1` quando algo acontece (`quantidade += 1`);
- **acumulador**: começa num valor neutro e incorpora cada item (`soma += valor`).

O valor inicial do acumulador é o "neutro" da operação: `0` para somar, `1` para multiplicar, `""` (texto vazio) para juntar textos.

### Exemplo resolvido: média das bobinas acima de 100 kg

**Problema:** da lista de pesos, quero a média só das bobinas com mais de 100 kg (as menores são pontas de bobina e não entram).

**Raciocínio:**

1. Média = soma ÷ quantidade. Preciso de um acumulador (`soma`) e de um contador (`quantidade`).
2. Os dois começam **antes** do laço; senão seriam zerados a cada volta.
3. Dentro do laço: se o peso passa de 100, somo e conto.
4. Depois do laço: se ninguém foi contado, não dá para dividir.

```python
pesos = [125.5, 48.0, 130.2, 128.9, 75.3]
soma = 0.0
quantidade = 0
for peso in pesos:
    if peso > 100:
        soma += peso
        quantidade += 1
if quantidade > 0:
    print(f"Média de {quantidade} bobinas: {soma / quantidade:.2f} kg")
else:
    print("Nenhuma bobina acima de 100 kg.")
```

Saída:

```text
Média de 3 bobinas: 128.20 kg
```

> 🔧 **Modifique:** mova as linhas `soma = 0.0` e `quantidade = 0` para **dentro** do `for` (logo abaixo dele) e rode. O resultado muda para quê? Por quê? Esse é um dos bugs mais comuns de iniciante, e o exercício 11 pede que você o reconheça.

> ⚠️ **Erro comum:** calcular a média de uma lista vazia. Com zero itens, `soma / quantidade` vira `0 / 0` e dá `ZeroDivisionError: division by zero`. Sempre trate o caso "nada para calcular" antes de dividir.

Acumulador de texto também é muito útil para montar relatórios:

```python
relatorio = ""
for linha in "ABC":
    relatorio += f"[Linha {linha}] "
print(relatorio)
```

Saída:

```text
[Linha A] [Linha B] [Linha C]
```

## 12. Padrões clássicos: buscar, contar, maior e menor

Quase todo problema com laços é uma variação de poucos padrões. Reconhecê-los é metade da solução.

### Contar com condição

"Quantas medições ficaram fora da faixa?" → contador que só aumenta quando a condição é verdadeira:

```python
medicoes = [24.8, 25.3, 22.7, 25.4, 27.6]
fora = 0
for valor in medicoes:
    if valor < 23 or valor > 27:
        fora += 1
print(f"{fora} de {len(medicoes)} fora ({fora / len(medicoes):.0%})")
```

Saída:

```text
2 de 5 fora (40%)
```

### Buscar

"Existe alguma bobina acima de 140 kg? Em que posição?" → percorrer até achar e parar. Antes do laço, um valor que significa "não achei":

```python
pesos = [125.5, 130.2, 142.8, 128.9, 151.0]
achou_em = 0  # 0 = não achou
posicao = 0
for peso in pesos:
    posicao += 1
    if peso > 140:
        achou_em = posicao
        break
print("Primeira acima de 140 kg na posição:", achou_em)
```

Saída:

```text
Primeira acima de 140 kg na posição: 3
```

Sem o `break`, o laço continuaria e `achou_em` terminaria com a posição da **última** bobina acima de 140 (a 5ª). Às vezes é isso que se quer; leia o enunciado com atenção.

### Maior e menor

"Qual a bobina mais pesada?" → guardar o "campeão até agora" e trocar sempre que aparecer alguém melhor. O detalhe é o valor inicial: comece com `None` ("ainda não vi ninguém"):

```python
pesos = [125.5, 130.2, 142.8, 128.9]
mais_pesada = None
for peso in pesos:
    if mais_pesada is None or peso > mais_pesada:
        mais_pesada = peso
print("Mais pesada:", mais_pesada, "kg")
```

Saída:

```text
Mais pesada: 142.8 kg
```

Na primeira volta, `mais_pesada is None` é verdadeiro e o primeiro peso vira o campeão. O `or` faz curto-circuito: o Python nem tenta `peso > None`, que daria `TypeError`.

> 🔮 **Preveja antes de rodar:** e se o "campeão" começasse em `0`?
>
> ```python
> temperaturas = [-18.5, -21.0, -19.2]  # câmara fria do ensaio de impacto
> maior = 0
> for t in temperaturas:
>     if t > maior:
>         maior = t
> print(maior)
> ```

<details><summary>Resposta</summary>

Imprime `0`, um valor que **nem está na lista**. Como todas as temperaturas são negativas, nenhuma é maior que 0, e o valor inicial nunca é trocado. Começar com `None` (ou com o primeiro item da lista, o que você vai aprender no módulo 03) evita esse bug.

</details>

**Tente você:** adapte o código da bobina mais pesada para achar a **mais leve**.

<details><summary>Resposta</summary>

```python
pesos = [125.5, 130.2, 142.8, 128.9]
mais_leve = None
for peso in pesos:
    if mais_leve is None or peso < mais_leve:
        mais_leve = peso
print("Mais leve:", mais_leve, "kg")
```

Só mudam o nome e o sinal: `<` no lugar de `>`.

</details>

## 13. Laços aninhados

Um laço dentro de outro: para **cada** volta do laço de fora, o de dentro roda **inteiro**. Pense num plano de amostragem: para cada linha de produção, coletar em cada turno.

```python
coletas = 0
for linha in "ABCD":
    for turno in range(1, 4):
        coletas += 1
        print(f"{linha}{turno}", end=" ")
    print()  # quebra a linha depois dos 3 turnos
print("Total de coletas:", coletas)
```

Saída:

```text
A1 A2 A3
B1 B2 B3
C1 C2 C3
D1 D2 D3
Total de coletas: 12
```

O total de voltas do laço de dentro é **(voltas do laço de fora) × (voltas do laço de dentro)**: 4 × 3 = 12. Com 4 linhas × 3 turnos × 20 medições, seriam 240 voltas no laço mais interno. Laços aninhados multiplicam o trabalho: com dados grandes, isso começa a pesar.

> 🔮 **Preveja antes de rodar:** quantas vezes `"*"` é impresso, e em que formato?
>
> ```python
> for i in range(1, 4):
>     for j in range(i):
>         print("*", end="")
>     print()
> ```

<details><summary>Resposta</summary>

Seis asteriscos, em forma de escada:

```text
*
**
***
```

O laço de dentro depende do de fora: na volta `i = 1`, `range(1)` roda 1 vez; com `i = 2`, 2 vezes; com `i = 3`, 3 vezes. Total: 1 + 2 + 3 = 6.

</details>

Um clássico: a tabuada, montando cada linha com um acumulador de texto (`exemplos/08_lacos_aninhados.py`):

```python
for n in range(1, 4):
    linha = ""
    for i in range(1, 5):
        linha += f"{n}x{i}={n * i:<4}"
    print(linha)
```

Saída:

```text
1x1=1   1x2=2   1x3=3   1x4=4
2x1=2   2x2=4   2x3=6   2x4=8
3x1=3   3x2=6   3x3=9   3x4=12
```

> 🔧 **Modifique:** faça a tabuada ir até 10 nos dois laços. Quantas contas o programa faz?

## 14. Validação de dados: não confie na entrada

Dado digitado, lido de planilha ou de e-mail **vai** vir errado um dia: vazio, com letra, negativo, absurdo. Um programa profissional confere antes de usar. Três ideias:

**1. Verifique o formato antes de converter.** Sem `try/except` (que é do módulo 06), você pode olhar caractere por caractere. Exemplo: aceitar só inteiros positivos para a quantidade de bobinas.

```python
def eh_inteiro_positivo(texto: str) -> bool:
    """True se o texto (sem espaços nas pontas) tem só dígitos e não é zero."""
    limpo = texto.strip()
    if not limpo:  # texto vazio é falsy
        return False
    for caractere in limpo:
        if caractere not in "0123456789":
            return False  # basta UM caractere ruim para reprovar
    return int(limpo) > 0


print(eh_inteiro_positivo(" 12 "), eh_inteiro_positivo("7.5"), eh_inteiro_positivo("0"))
```

Saída:

```text
True False False
```

Repare na lógica de "reprovar no primeiro defeito": o laço procura um caractere ruim e devolve `False` assim que acha. Se chegar ao fim sem achar, o texto passou na inspeção.

**2. Verifique se o valor faz sentido.** Um texto pode ser um número válido e ainda assim absurdo: espessura negativa, palete com 50 bobinas, umidade de 130%.

**3. Retorno antecipado (cláusulas de guarda).** Dentro de funções, trate os casos ruins primeiro e saia logo. O caminho "feliz" fica no fim, sem aninhamento:

```python
def validar_quantidade(texto: str) -> str:
    if not eh_inteiro_positivo(texto):
        return "digite um inteiro maior que zero"
    quantidade = int(texto)  # seguro: já sabemos que só tem dígitos
    if quantidade > 12:
        return "um palete leva no máximo 12 bobinas"
    return f"OK, {quantidade} bobinas"
```

O exemplo `exemplos/09_validacao.py` roda essas funções com várias entradas, boas e ruins.

### Laço de validação: perguntar até vir certo

Combinando `while True`, validação e `break`, você obtém o padrão de todo formulário de terminal:

```python
while True:
    texto = input("Quantidade de bobinas: ")
    if eh_inteiro_positivo(texto) and int(texto) <= 12:
        quantidade = int(texto)
        break
    print("  Valor inválido: digite um inteiro de 1 a 12.")
print("Palete com", quantidade, "bobinas.")
```

Uma execução:

```text
Quantidade de bobinas: doze
  Valor inválido: digite um inteiro de 1 a 12.
Quantidade de bobinas: 15
  Valor inválido: digite um inteiro de 1 a 12.
Quantidade de bobinas: 8
Palete com 8 bobinas.
```

> 💡 **Dica:** escreva mensagens de erro que digam **o que fazer**, não só o que deu errado. "Digite um inteiro de 1 a 12" ajuda o operador; "Erro: entrada inválida" não.

## 15. Depurando laços: o teste de mesa

Laço com resultado estranho? Antes de mudar código no chute, **simule à mão**. Faça uma tabela com uma coluna por variável e uma linha por volta. Exemplo para este trecho:

```python
total = 0
n = 1
while n < 20:
    total += n
    n *= 3
print(total, n)
```

Saída:

```text
13 27
```

O teste de mesa que explica a saída:

```text
volta |  n  | n < 20? | total depois
------+-----+---------+-------------
  1   |   1 |   sim   |   0 + 1 = 1
  2   |   3 |   sim   |   1 + 3 = 4
  3   |   9 |   sim   |   4 + 9 = 13
  -   |  27 |   não   |   (sai do laço)
```

Parece trabalho manual demais? É o que os programadores experientes fazem de cabeça. Fazer no papel agora é o que vai permitir fazer de cabeça depois.

Ferramentas que ajudam:

- **print dentro do laço:** `print(f"{n=} {total=}")` mostra cada volta. Apague depois.
- **Python Tutor** (pythontutor.com): cole o código e veja, passo a passo, as variáveis mudando. Excelente para laços.
- **Depurador do VS Code:** clique à esquerda do número da linha para criar um ponto de parada (bolinha vermelha) e rode com F5. O módulo 09 ensina a fundo.

## Lendo mensagens de erro deste módulo

Os erros típicos de decisões e laços, como aparecem rodando um script `teste.py`:

**Esqueceu os dois-pontos:**

```text
  File "C:\curso-python\teste.py", line 2
    if valor > 27
                 ^
SyntaxError: expected ':'
```

Todo `if`, `elif`, `else`, `while`, `for`, `match`, `case` e `def` termina com `:`. O mesmo erro aparece se você escrever `else if` (que não existe em Python) em vez de `elif`.

**Usou `=` no lugar de `==`:**

```text
  File "C:\curso-python\teste.py", line 2
    if valor = 27:
       ^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Esqueceu de recuar o bloco:**

```text
  File "C:\curso-python\teste.py", line 3
    print("Acima")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 2
```

O Python esperava um bloco recuado depois do `if` da linha 2. Coloque 4 espaços antes do `print`.

**Comparou texto com número:**

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 2, in <module>
    if leitura < 30:
       ^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'str' and 'int'
```

`leitura` é um texto (veio de `input()` ou de uma planilha). Converta com `float()` antes de comparar.

**Tentou percorrer um número:**

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 2, in <module>
    for i in 10:
             ^^
TypeError: 'int' object is not iterable
```

"Iterable" é "algo que dá para percorrer". Um número não é; use `range(10)`.

**Variável criada só dentro de um `if` que não rodou:**

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 4, in <module>
    print(status)
          ^^^^^^
NameError: name 'status' is not defined
```

O código era `if valor > 27: status = "ACIMA"` e o valor era 25: o bloco não rodou e `status` nunca foi criada. Dentro de uma função, o mesmo problema aparece com outro nome. Com uma função `rotulo(valor)` que tem esse mesmo `if` e termina com `return status`, chamada como `print(rotulo(25))`:

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 7, in <module>
    print(rotulo(25))
          ~~~~~~^^^^
  File "C:\curso-python\teste.py", line 4, in rotulo
    return status
           ^^^^^^
UnboundLocalError: cannot access local variable 'status' where it is not associated with a value
```

Repare que há dois blocos `File`: o erro aconteceu dentro de `rotulo` (linha 4), chamada pela linha 7. O traceback mostra o caminho inteiro, do mais externo para o mais interno.

Correção nos dois casos: garanta um valor em **todos** os caminhos, com um `else` ou com um valor inicial antes do `if`.

**Média de lista vazia:**

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 7, in <module>
    print(soma / quantidade)
          ~~~~~^~~~~~~~~~~~
ZeroDivisionError: division by zero
```

O laço não rodou nenhuma vez e `quantidade` ficou 0. Teste `if quantidade == 0:` antes de dividir.

**Interrompeu com Ctrl+C:** `KeyboardInterrupt` (seção 7). Se aconteceu sem querer, procure o `while` cuja condição nunca fica falsa.

## Boas práticas

- **Condições legíveis:** prefira `if aprovado:` a `if aprovado == True:`, e `if not texto:` a `if len(texto) == 0:`.
- **Nomeie condições complexas:** `dentro_da_faixa = minimo <= valor <= maximo` e depois `if dentro_da_faixa and cof_ok:`. O código vira frase.
- **Trate os casos ruins primeiro** (retorno antecipado). Menos aninhamento, menos bug.
- **Ordem dos `elif`:** coerente (da menor faixa para a maior, ou o contrário) e teste os valores de fronteira.
- **Acumuladores e contadores antes do laço**, nunca dentro.
- **Todo `while` com saída garantida**, e com proteção para os casos em que a saída seria impossível.
- **`for` sempre que possível;** `while` quando o número de voltas é desconhecido.
- **`is None`** para testar ausência de valor; não confie em truthy/falsy quando `0` é um valor válido.
- **Não use `max()`, `min()` e `sum()` ainda** nos exercícios: o objetivo é dominar o padrão. No dia a dia (e a partir do módulo 03), use-os.

## No mundo real

Um caso completo de linha de produção: as leituras do micrômetro chegam (com falhas de leitura registradas como 0 ou negativo), o programa classifica cada uma, diz ao operador o que fazer, aplica a regra "3 seguidas fora = pare a linha" e emite o veredito. É o `exemplos/10_inspecao_serie.py`.

```python
def acao_do_operador(situacao: str) -> str:
    """O que o operador da extrusora deve fazer para cada situação."""
    match situacao:
        case "ABAIXO":
            return "abrir a matriz"
        case "ACIMA":
            return "fechar a matriz"
        case _:
            return ""


linha = "C"
nominal = 25.0
tolerancia = 8.0  # especificação da OP (ou o padrão da linha)
leituras = [24.9, 25.3, 0.0, 26.1, -1.0, 27.4, 25.0, 22.8, 22.5, 22.9, 25.1]

if tolerancia <= 0:
    print("Tolerância inválida na especificação. Nada a fazer.")
else:
    minimo = nominal - nominal * tolerancia / 100
    maximo = nominal + nominal * tolerancia / 100
    print(f"Linha {linha} | {nominal} µm ± {tolerancia:.0f}% -> {minimo:.2f} a {maximo:.2f}")

    posicao = 0
    validas = 0
    soma = 0.0
    fora = 0
    seguidas = 0
    parar_linha = False
    for valor in leituras:
        posicao += 1
        if valor <= 0:
            print(f"  #{posicao:<2} falha de leitura, ignorada")
            continue
        validas += 1
        soma += valor
        if valor < minimo:
            situacao = "ABAIXO"
        elif valor > maximo:
            situacao = "ACIMA"
        else:
            situacao = "ok"
        if situacao == "ok":
            seguidas = 0
        else:
            fora += 1
            seguidas += 1
        print(f"  #{posicao:<2} {valor:>6.2f} µm  {situacao:<7}{acao_do_operador(situacao)}")
        if seguidas == 3:
            parar_linha = True
            print("  >>> 3 leituras seguidas fora: PARE A LINHA e chame o líder.")
            break

    print("-" * 50)
    if validas == 0:
        print("Nenhuma leitura válida.")
    else:
        media = soma / validas
        if parar_linha:
            veredito = "REPROVADO (processo fora de controle)"
        elif fora > 0:
            veredito = "CONDICIONAL (pontos isolados fora)"
        else:
            veredito = "APROVADO"
        print(f"Válidas: {validas} | média {media:.2f} µm | fora: {fora}")
        print(f"Veredito: {veredito}")
```

Saída:

```text
Linha C | 25.0 µm ± 8% -> 23.00 a 27.00
  #1   24.90 µm  ok
  #2   25.30 µm  ok
  #3  falha de leitura, ignorada
  #4   26.10 µm  ok
  #5  falha de leitura, ignorada
  #6   27.40 µm  ACIMA  fechar a matriz
  #7   25.00 µm  ok
  #8   22.80 µm  ABAIXO abrir a matriz
  #9   22.50 µm  ABAIXO abrir a matriz
  #10  22.90 µm  ABAIXO abrir a matriz
  >>> 3 leituras seguidas fora: PARE A LINHA e chame o líder.
--------------------------------------------------
Válidas: 8 | média 24.61 µm | fora: 4
Veredito: REPROVADO (processo fora de controle)
```

Repare em quantos padrões trabalham juntos: `continue` para falhas de leitura, contador de posição, acumulador de soma, contador de fora, contador de **seguidas** que zera quando aparece uma leitura boa, `break` quando a regra dispara, `if/elif/else` para classificar, `match` para a ação e uma cascata de `if` para o veredito. Nenhum é difícil sozinho. Juntá-los é o que você vai treinar nos exercícios e no desafio.

## Resumo

| Assunto | Sintaxe essencial |
|---|---|
| Comparar | `==  !=  <  >  <=  >=` · faixa: `minimo <= x <= maximo` · floats: `math.isclose(a, b)` |
| Combinar | `a and b` · `a or b` · `not a` (precedência: `not` → `and` → `or`) |
| Decidir | `if cond:` · `elif cond:` · `else:` (só o 1º bloco verdadeiro roda) |
| Escolher valor | `x = "OK" if cond else "FORA"` |
| Falsy | `False  None  0  0.0  ""  []` · ausência: `x is None` / `x is not None` |
| match | `match valor:` · `case "C":` · vários valores no mesmo caso com a barra vertical · `case _:` |
| while | estado inicial → `while cond:` → atualização · `while True:` + `break` · `Ctrl+C` interrompe |
| for | `for letra in texto:` · `for valor in valores:` · `len(valores)` |
| range | `range(fim)` · `range(início, fim)` · `range(início, fim, passo)` (fim exclusivo) |
| Controle | `break` encerra o laço · `continue` pula para a próxima volta |
| Padrões | contador `n += 1` · acumulador `soma += x` · busca com `break` · maior: `if maior is None or x > maior:` |
| Aninhados | voltas internas = voltas de fora × voltas de dentro |
| Validação | conferir formato e faixa antes de usar · retorno antecipado · laço "pergunte até vir certo" |

## Você domina este módulo se...

- [ ] explico, sem consultar, por que `linha == "A" or "B"` é sempre verdadeiro e escrevo a forma correta;
- [ ] escrevo um `if/elif/else` de faixas e testo os valores de fronteira por conta própria;
- [ ] digo quais destes são falsy sem rodar: `0`, `"0"`, `""`, `" "`, `None`, `0.0`, `[]`, e sei quando `is None` é obrigatório;
- [ ] escrevo de memória um laço que calcula soma, quantidade, média, maior e menor de uma lista, tratando a lista vazia;
- [ ] prevejo quais números um `range(a, b, passo)` gera, inclusive com passo negativo;
- [ ] explico a diferença entre `break`, `continue` e `return` dentro de um laço;
- [ ] olho para um `while` e digo se ele pode virar loop infinito, e como evitar;
- [ ] faço o teste de mesa de um laço de 4 ou 5 voltas e acerto o valor final das variáveis.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_situacao_aluno` | ★☆☆ | `if/elif/else`, ordem das faixas, validação |
| 02 | `ex02_dentro_da_faixa` | ★☆☆ | comparação encadeada, expressão condicional |
| 03 | `ex03_ano_bissexto` | ★☆☆ | `and`, `or`, `not`, `%` |
| 04 | `ex04_tolerancia_da_linha` | ★☆☆ | `match-case`, vários valores por caso, `case _`, `None` |
| 05 | `ex05_contar_vogais` | ★☆☆ | `for` em string, contador, `in` |
| 06 | `ex06_fatorial` | ★☆☆ | `for` com `range`, acumuladores de soma e produto |
| 07 | `ex07_classificar_medicao` | ★★☆ | limites de tolerância, `elif`, cláusula de guarda |
| 08 | `ex08_media_das_medicoes` | ★★☆ | lista recebida, `continue`, média, `None` |
| 09 | `ex09_amplitude` | ★★☆ | padrão maior/menor com `None`, função chamando função |
| 10 | `ex10_anos_para_dobrar` | ★★☆ | `while`, proteção contra loop infinito |
| 11 | `ex11_leitura_de_lacos` | ★★☆ | **leitura de código:** prever saídas e consertar um bug |
| 12 | `ex12_sequencia_fora` | ★★★ | busca com dois contadores, regra de "N seguidas" |
| 13 | `ex13_revisao_tabela_limites` | ★★★ | **revisão** (módulos 00 a 02): laços aninhados, `match`, f-strings, tolerância |
| 14 | `ex14_revisao_resumo_serie` | ★★★ | **revisão** (módulos 00 a 02): validação de texto, conversão, contadores, máximo/mínimo, formatação |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de `raise NotImplementedError`, e rode na pasta `curso-python`:

```text
python curso.py testar 02 ex01
```

Para testar o módulo inteiro: `python curso.py testar 02`. Os exercícios 13 e 14 são de **revisão**: misturam este módulo com o módulo 01 (f-strings, conversões, limpeza de texto). Se travar neles, releia as seções 8, 9 e 11 do módulo 01. Depois de passar em cada exercício, compare com `solucoes/`.

## Desafio do módulo

**Inspetor de série no terminal:** um programa interativo que pergunta a linha e o nominal (validando as respostas), lê as medições até o operador digitar `fim`, classifica cada uma na hora, manda parar a linha se 3 seguidas saírem da faixa e emite o veredito com média, mínimo, máximo e porcentagem fora. Tem um modo demonstração que roda sem digitação. Enunciado completo em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md) (15 perguntas, gabarito comentado no final).

## Para ir além

- Tutorial oficial, "Mais ferramentas de controle de fluxo" (`if`, `for`, `range`, `break`, `continue`, `match`): <https://docs.python.org/pt-br/3/tutorial/controlflow.html>
- Valores verdade e operadores booleanos: <https://docs.python.org/pt-br/3/library/stdtypes.html#truth-value-testing>
- Comparações: <https://docs.python.org/pt-br/3/library/stdtypes.html#comparisons>
- PEP 636, tutorial do match-case (em inglês, com muitos exemplos): <https://peps.python.org/pep-0636/>
- Python Tutor, para visualizar laços passo a passo: <https://pythontutor.com/>
- Leitura extra: os problemas iniciais do site Exercism (trilha de Python) treinam exatamente os padrões deste módulo: <https://exercism.org/tracks/python>
