# Módulo 01 — Fundamentos

> **Tempo estimado:** 8 a 10 horas · **Pré-requisitos:** módulo 00 (Python, VS Code e terminal funcionando) · **Nível:** iniciante

## O que você vai aprender

Ao final deste módulo, você vai conseguir:

- mostrar informações na tela com `print()`, controlando o separador (`sep`) e o final da linha (`end`);
- criar variáveis com nomes claros e explicar o que acontece quando uma variável recebe outro valor;
- dizer o tipo de qualquer valor (`int`, `float`, `str`, `bool`, `None`) e conferir com `type()`;
- calcular com `+ - * / // % **` e prever o resultado de uma expressão sem parênteses;
- atualizar totais e contadores com `+=`, `-=`, `*=` e `/=`;
- limpar e examinar textos com `len`, `upper`, `lower`, `strip`, `replace` e `in`;
- converter texto em número (e o contrário) com `int()`, `float()` e `str()`, sabendo quando isso dá erro;
- ler o que o usuário digita com `input()`;
- montar textos com f-strings e formatar números com `:.2f`, `:,.2f`, `:.1%`, `:03d` e alinhamento;
- explicar por que `0.1 + 0.2` não dá `0.3` e decidir quando e como arredondar;
- usar `math.sqrt`, `math.pi`, `math.ceil` e `math.floor`;
- escrever uma função com `def` e `return`, o molde de todos os exercícios do curso;
- ler e corrigir os erros mais comuns: `NameError`, `TypeError`, `ValueError`, `SyntaxError`, `IndentationError` e `ZeroDivisionError`.

## Por que isso importa

Todo programa, do script de 10 linhas ao sistema de uma multinacional, é feito das mesmas peças: valores, nomes para esses valores, contas e textos. Este módulo é o alfabeto. Sem ele, nada do resto faz sentido. Com ele firme, todo o resto fica mais fácil.

Pense no projeto final, o validador de certificados. Ele vai precisar:

- ler `"25,4"` de uma célula da planilha e transformar em número → **conversões** (seção 9);
- calcular os limites de "25 µm ± 10%" → **operadores** (seção 6);
- transformar `" op-12345 "` em `"OP12345"` para cruzar com o e-mail da expedição → **strings** (seção 8);
- escrever "Espessura média: 25.07 µm" no relatório → **f-strings** (seção 11);
- não se enganar com a 17ª casa decimal ao somar pesos → **float e round** (seção 12).

No mercado é igual. Os primeiros testes de código em processos seletivos para estágio e júnior cobram exatamente isto: manipular texto, fazer contas e formatar a saída sem tropeçar.

> 💡 **Dica:** estude com o VS Code aberto. Apareceu código? Digite e rode. Ler código sem rodar é como ler sobre natação.

### Como estudar este módulo (método PRIMM)

Você vai ver quatro tipos de caixa ao longo da aula:

- 🔮 **Preveja antes de rodar:** leia o código e **escreva** (no papel ou num comentário) o que acha que vai sair. Só depois rode e compare. Errar a previsão é ótimo: mostra exatamente o que você ainda não entendeu.
- 🔧 **Modifique:** mude um detalhe do exemplo e veja o efeito. É assim que o conhecimento "gruda".
- **Exemplo resolvido:** um problema resolvido passo a passo, com o raciocínio. Leia antes de tentar os parecidos.
- **Tente você:** um mini exercício com a resposta escondida. Tente antes de abrir.

## 1. Dois jeitos de rodar Python: REPL e script

No módulo 00 você conheceu os dois. Recapitulando, porque esta aula usa os dois o tempo todo.

**REPL** é o modo conversa. No PowerShell, digite `python` (no Linux/macOS, `python3`). Aparece o sinal `>>>`. Você digita uma linha, aperta Enter e o Python responde na hora:

```python
>>> 2 + 3
5
>>> "laudo".upper()
'LAUDO'
```

Repare: no REPL você não precisa de `print` para ver o resultado. Ele mostra o valor de cada expressão (textos aparecem entre aspas). Para sair, digite `exit()`.

**Script** é um arquivo `.py` com várias linhas, executado de uma vez:

```text
PS C:\curso-python> python 01-fundamentos\exemplos\01_print.py
```

No script, só aparece na tela o que você mandar imprimir com `print`.

Nesta aula, blocos que começam com `>>>` são sessões de REPL. Os outros blocos são scripts, e a saída vem logo abaixo, marcada como **Saída**.

> 💡 **Dica:** o REPL é o seu laboratório de bancada. Ficou em dúvida sobre o que uma linha faz? Não fique adivinhando: abra o REPL e teste. Leva 5 segundos.

## 2. print: o programa falando com você

`print()` mostra valores na tela. Pense nele como o visor de um equipamento: é por onde o programa conta o que está acontecendo.

```python
print("Olá, laboratório!")
print("OP", 12345, "liberada")
print("Espessura:", 25.4, "µm")
```

Saída:

```text
Olá, laboratório!
OP 12345 liberada
Espessura: 25.4 µm
```

Você pode passar vários valores separados por vírgula. O `print` coloca um espaço entre eles e quebra a linha no final.

Dois controles úteis:

- `sep=` troca o separador entre os valores;
- `end=` troca o que vai no fim (o padrão é uma quebra de linha).

```python
print("A", "B", "C", "D", sep=" | ")
print("Medindo...", end=" ")
print("pronto!")
```

Saída:

```text
A | B | C | D
Medindo... pronto!
```

Dentro de um texto, alguns "códigos de barra invertida" têm significado especial: `\n` quebra a linha e `\t` insere uma tabulação.

```python
print("Linha 1\nLinha 2")
print("Amostra\tResultado")
```

Saída:

```text
Linha 1
Linha 2
Amostra	Resultado
```

Textos podem usar aspas simples ou duplas. Use uma para "proteger" a outra:

```python
print('Ela disse: "COF liberado"')
print("Copo d'água")
```

Saída:

```text
Ela disse: "COF liberado"
Copo d'água
```

> ⚠️ **Erro comum:** escrever `Print` com P maiúsculo. Python diferencia maiúsculas de minúsculas: `Print` não existe e você recebe `NameError: name 'Print' is not defined. Did you mean: 'print'?`. Leia a sugestão no fim da mensagem: ela costuma acertar.

> 🔮 **Preveja antes de rodar:** o que este código imprime? Escreva antes de testar.
>
> ```python
> print("Lote", 7, sep="-", end="!")
> print("OK")
> ```

<details><summary>Resposta</summary>

Sai `Lote-7!OK` numa linha só. O `sep="-"` colocou um hífen entre `"Lote"` e `7`, e o `end="!"` trocou a quebra de linha por um `!`. Como o primeiro `print` não quebrou a linha, o `OK` do segundo ficou colado.

</details>

O arquivo `exemplos/01_print.py` tem todos esses casos. Rode:

```text
python 01-fundamentos\exemplos\01_print.py
```

## 3. Comentários: notas para humanos

Tudo depois de `#` numa linha é ignorado pelo Python. Comentários são para quem lê o código, inclusive você daqui a três meses.

```python
# Converte a espessura de micrômetros para milímetros
espessura_mm = 25.4 / 1000  # 1 mm = 1000 µm
print(espessura_mm)
```

Saída:

```text
0.0254
```

Bons comentários explicam o **porquê**, não o óbvio:

```python
# Ruim: repete o que o código já diz
total = total + 1  # soma 1 no total

# Bom: explica uma decisão
tolerancia = 0.08  # 8%: linha C é coextrusão, a espec. do cliente permite mais
```

Um texto entre três aspas logo no começo de um arquivo ou de uma função é uma **docstring**: a documentação oficial daquele trecho. Todos os exercícios do curso começam com uma docstring, que é o enunciado.

> 💡 **Dica:** no VS Code, `Ctrl+;` (ou `Ctrl+/`, conforme o teclado) comenta e descomenta as linhas selecionadas. Ótimo para "desligar" um trecho enquanto testa.

## 4. Variáveis e nomes

Uma variável é um **nome que aponta para um valor**. Pense na etiqueta que você cola numa amostra: a etiqueta "OP12345 - bobina 3" não é a amostra, mas permite encontrá-la depois.

```python
op = "OP12345"
quantidade_bobinas = 8
espessura_um = 25.4
print(op, quantidade_bobinas, espessura_um)
```

Saída:

```text
OP12345 8 25.4
```

O `=` em Python **não** é o "igual" da matemática. Ele é uma ordem: "calcule o que está à direita e cole esta etiqueta no resultado". Por isso, isto é válido:

```python
>>> bobinas = 8
>>> bobinas = bobinas + 2
>>> bobinas
10
```

Na matemática, `x = x + 2` é absurdo. Em Python é rotina: pegue o valor atual (8), some 2 e cole a etiqueta `bobinas` no novo valor (10).

### Regras e convenções de nomes

Regras (se quebrar, dá erro):

- só letras, números e `_`;
- não pode começar com número (`1amostra` é inválido);
- não pode ser uma palavra reservada (`if`, `for`, `def`, `class`, `True`, `None`...);
- maiúsculas e minúsculas são diferentes: `peso` e `Peso` são duas variáveis.

Convenções (o Python aceita quebrar, mas os outros programadores não):

- **snake_case**: palavras minúsculas separadas por `_` → `peso_liquido_kg`;
- **sem acento**: `espessura_media`, não `espessura_média` (funciona, mas dá problema com teclados, ferramentas e colegas);
- **nomes que dizem o que é**: `tolerancia_pct` em vez de `t`; `peso_kg` em vez de `p`;
- **unidade no nome** quando houver risco de confusão: `espessura_um`, `largura_mm`, `peso_kg`;
- **MAIÚSCULAS** para constantes, valores que não devem mudar: `TOLERANCIA_PADRAO_PCT = 10`.

> ⚠️ **Erro comum:** usar uma variável antes de criá-la, ou digitar o nome errado. `print(espesura)` (faltou um "s") dá `NameError: name 'espesura' is not defined. Did you mean: 'espessura'?`.

> 💡 **Dica:** nome bom economiza comentário. Compare `x = a * b / 1000` com `peso_kg = gramatura * area_m2 / 1000`. O segundo dispensa explicação.

**Tente você:** quais destes nomes são inválidos? `peso2`, `2peso`, `peso-liquido`, `peso_liquido`, `class`, `Classe`.

<details><summary>Resposta</summary>

Inválidos: `2peso` (começa com número), `peso-liquido` (o hífen seria lido como subtração) e `class` (palavra reservada). `Classe` é válido, porque maiúsculas contam como letra diferente, mas foge da convenção snake_case.

</details>

## 5. Tipos de dados: int, float, str, bool e None

Todo valor tem um **tipo**. O tipo diz o que dá para fazer com o valor, como a unidade de medida diz o que dá para somar: você soma µm com µm, não µm com kg.

| Tipo | Para quê | Exemplos |
|---|---|---|
| `int` | números inteiros | `8`, `-3`, `12345` |
| `float` | números com casas decimais | `25.4`, `0.1`, `-2.5`, `1e3` |
| `str` | texto (string) | `"OP12345"`, `'linha B'`, `""` |
| `bool` | verdadeiro ou falso | `True`, `False` |
| `None` | "nada", ausência de valor | `None` |

A função `type()` diz o tipo de qualquer valor:

```python
>>> type(8)
<class 'int'>
>>> type(25.4)
<class 'float'>
>>> type("25.4")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type(None)
<class 'NoneType'>
```

Repare em `"25.4"`: entre aspas, é **texto**, mesmo parecendo número. Essa diferença vai aparecer o tempo todo quando você ler planilhas e e-mails.

Detalhes que valem ouro:

- `True` e `False` começam com maiúscula. `true` dá `NameError`.
- `None` é o "campo vazio": a célula da planilha que ainda não foi preenchida, a observação que não existe. Não é zero nem texto vazio; é "não tem valor".
- O Python usa **ponto** como separador decimal: `25.4`, nunca `25,4`. A vírgula separa valores. `1e3` é notação científica: 1 × 10³ = `1000.0`.

```python
>>> 25,4
(25, 4)
```

Viu? Com vírgula, o Python entende **dois números** (25 e 4) agrupados. Isso é uma tupla, que você verá no módulo 03. Por enquanto: decimal é com ponto.

O exemplo `exemplos/02_variaveis_e_tipos.py` cria uma variável de cada tipo e mostra o `type()` de cada uma.

> 🔮 **Preveja antes de rodar:** qual o tipo de cada valor? `10`, `10.0`, `"10"`, `10 / 2`, `"True"`.

<details><summary>Resposta</summary>

`int`, `float`, `str`, `float` e `str`. Duas pegadinhas: `10 / 2` dá `5.0` (a divisão `/` **sempre** devolve float, mesmo quando a conta é exata) e `"True"` entre aspas é texto, não booleano. Confira no REPL com `type(10 / 2)`.

</details>

## 6. Operadores aritméticos e precedência

| Operador | Operação | Exemplo | Resultado |
|---|---|---|---|
| `+` | soma | `7 + 2` | `9` |
| `-` | subtração | `7 - 2` | `5` |
| `*` | multiplicação | `7 * 2` | `14` |
| `/` | divisão | `7 / 2` | `3.5` |
| `//` | divisão inteira | `7 // 2` | `3` |
| `%` | resto da divisão | `7 % 2` | `1` |
| `**` | potência | `7 ** 2` | `49` |

Os dois "estranhos" são `//` e `%`. Pense em embalar: `//` responde "quantas caixas completas?" e `%` responde "quanto sobra fora das caixas?".

### Exemplo resolvido: dividir uma produção em bobinas

**Problema:** a extrusora produziu 12.300 m de filme. Cada bobina leva 1.000 m. Quantas bobinas completas saem, e quanto filme sobra?

**Raciocínio:** "quantas vezes 1.000 cabe inteiro em 12.300" é divisão inteira (`//`). "O que sobra" é o resto (`%`). Vou guardar cada informação numa variável com nome claro e imprimir no fim.

```python
metros_totais = 12300
metros_por_bobina = 1000
bobinas = metros_totais // metros_por_bobina
sobra = metros_totais % metros_por_bobina
print(bobinas, "bobinas completas e sobra de", sobra, "m")
```

Saída:

```text
12 bobinas completas e sobra de 300 m
```

**Conferindo:** 12 × 1.000 + 300 = 12.300. Sempre que usar `//` e `%`, essa prova real vale: `quociente * divisor + resto == dividendo`.

> 🔧 **Modifique:** troque `metros_por_bobina` para `1500`. Antes de rodar, calcule de cabeça. Depois tente `12300 / 1000` (com uma barra só) e veja a diferença.

Outro uso clássico do `%` é saber se um número é par: `n % 2` dá `0` para pares e `1` para ímpares.

### Precedência: quem é calculado primeiro

Como na matemática da escola, o Python não faz as contas simplesmente da esquerda para a direita. Ele segue uma ordem:

```text
1º  ( )              parênteses
2º  **               potência
3º  * / // %         multiplicação, divisões e resto (da esquerda para a direita)
4º  + -              soma e subtração (da esquerda para a direita)
```

```python
>>> 2 + 3 * 4
14
>>> (2 + 3) * 4
20
>>> 2 ** 3 * 2
16
>>> 10 - 4 - 3
3
```

> 🔮 **Preveja antes de rodar:** um aluno tirou 7, 8 e 9. O que este código imprime? É a média dele?
>
> ```python
> print(7 + 8 + 9 / 3)
> ```

<details><summary>Resposta</summary>

Imprime `18.0`, e não é a média. A divisão vem antes da soma, então o Python calculou `9 / 3 = 3.0` e depois `7 + 8 + 3.0 = 18.0`. A média correta é `(7 + 8 + 9) / 3`, que dá `8.0`. Esse erro aparece em código profissional também; o exercício 03 cobra exatamente isso.

</details>

> 💡 **Dica:** na dúvida, use parênteses. Eles nunca atrapalham e deixam a intenção clara para quem lê: `(nominal * tolerancia_pct) / 100`.

> ⚠️ **Erro comum:** dividir por zero. `100 / 0` (ou uma variável que vale 0) dá `ZeroDivisionError: division by zero`. O Python não devolve "infinito": ele para o programa. No módulo 02 você vai aprender a verificar antes de dividir.

Uma curiosidade com números negativos: `//` arredonda **para baixo** (em direção ao menos infinito), não "corta" as casas.

```python
>>> 7 // 2
3
>>> -7 // 2
-4
```

**Tente você:** quantos minutos e segundos são 200 segundos? Use `//` e `%`.

<details><summary>Resposta</summary>

```python
>>> 200 // 60
3
>>> 200 % 60
20
```

3 minutos e 20 segundos. Prova real: 3 × 60 + 20 = 200.

</details>

## 7. Atribuição composta: atualizando valores

Somar algo ao valor atual de uma variável é tão comum que existe um atalho:

```python
total_kg = 0
total_kg += 125.5  # o mesmo que: total_kg = total_kg + 125.5
total_kg += 130.2
total_kg -= 5.7
print("Peso acumulado:", total_kg)
```

Saída:

```text
Peso acumulado: 250.0
```

| Atalho | Equivale a |
|---|---|
| `x += 5` | `x = x + 5` |
| `x -= 5` | `x = x - 5` |
| `x *= 2` | `x = x * 2` |
| `x /= 2` | `x = x / 2` |

Isso vai ser essencial no módulo 02, quando você somar centenas de medições dentro de um laço: `soma += medicao`.

> ⚠️ **Erro comum:** usar `+=` numa variável que ainda não existe. `contador += 1` sem antes ter `contador = 0` dá `NameError`. O Python precisa de um valor inicial para somar.

## 8. Strings básicas: trabalhando com texto

Uma string (`str`) é uma sequência de caracteres. Em sistemas de laboratório, texto está em todo lugar: OP, cliente, observação, nome do ensaio, linha do e-mail.

### Juntar, repetir e medir

```python
>>> "Linha " + "B"
'Linha B'
>>> "-" * 20
'--------------------'
>>> len("filme bopp")
10
```

- `+` entre textos **concatena** (cola um no outro);
- `*` entre texto e inteiro **repete**;
- `len()` conta os caracteres, incluindo espaços.

### Métodos: ferramentas que o texto já traz

Um **método** é uma função que pertence ao valor. Você chama com um ponto: `texto.metodo()`.

```python
>>> "filme bopp".upper()
'FILME BOPP'
>>> "COF LIBERADO".lower()
'cof liberado'
>>> "   Embalagens Sul  ".strip()
'Embalagens Sul'
>>> "25,4".replace(",", ".")
'25.4'
```

| Método | O que faz |
|---|---|
| `upper()` | tudo em maiúsculas (inclusive acentos: `"seleção"` → `"SELEÇÃO"`) |
| `lower()` | tudo em minúsculas |
| `strip()` | remove espaços (e quebras de linha) do começo e do fim |
| `replace(velho, novo)` | troca **todas** as ocorrências de `velho` por `novo` |

### Procurar com `in`

O operador `in` pergunta "este pedaço está dentro daquele texto?" e responde com um `bool`:

```python
>>> "COF" in "COF: liberado"
True
>>> "cof" in "COF: liberado"
False
>>> "cof" in "COF: liberado".lower()
True
```

A busca diferencia maiúsculas. O truque da última linha (passar tudo para minúsculas antes) é o jeito padrão de ignorar essa diferença. É exatamente o exercício 05.

### Strings não mudam

Strings são **imutáveis**: nenhum método altera o texto original. Eles devolvem um texto **novo**.

> 🔮 **Preveja antes de rodar:** o que é impresso?
>
> ```python
> nome = "laudo"
> nome.upper()
> print(nome)
> ```

<details><summary>Resposta</summary>

Imprime `laudo`, em minúsculas. O `nome.upper()` criou o texto `"LAUDO"`, mas ninguém guardou esse resultado, e ele se perdeu. Para "mudar", guarde o resultado: `nome = nome.upper()`. No REPL você veria `'LAUDO'` aparecer ao rodar a segunda linha, mas a variável continuaria igual.

</details>

### Exemplo resolvido: limpar o código de uma OP

**Problema:** a OP chegou digitada como `" op-12345 "`. O sistema precisa de `"OP12345"`.

**Raciocínio:** quebro em etapas pequenas, testando cada uma no REPL.

1. Tirar os espaços das pontas → `strip()`.
2. Deixar tudo maiúsculo → `upper()`.
3. Remover o hífen → `replace("-", "")` (trocar por "nada").

Como cada método devolve uma string nova, posso **encadear**: o resultado de um vira a entrada do próximo.

```python
>>> " op-12345 ".strip()
'op-12345'
>>> " op-12345 ".strip().upper()
'OP-12345'
>>> " op-12345 ".strip().upper().replace("-", "")
'OP12345'
```

Repare no método de trabalho: construí a expressão aos poucos, conferindo cada passo. Isso é muito mais rápido do que escrever tudo de uma vez e caçar o erro depois.

> 🔧 **Modifique:** e se a OP vier como `"OP 12.345"`? Que `replace` você acrescentaria? Teste no REPL. (O exercício 08 generaliza isso.)

> ⚠️ **Erro comum:** somar texto com número. `"Bobinas: " + 8` dá `TypeError: can only concatenate str (not "int") to str`. O Python se recusa a adivinhar se você queria somar números ou juntar textos. Converta com `str(8)` ou, melhor, use uma f-string (seção 11).

**Tente você:** a observação veio como `"  cof: LIBERADO  "`. Escreva uma linha que deixe `"COF: LIBERADO"`.

<details><summary>Resposta</summary>

```python
>>> "  cof: LIBERADO  ".strip().upper()
'COF: LIBERADO'
```

</details>

Rode `exemplos/04_strings.py` para ver tudo isso junto.

## 9. Conversões: int(), float() e str()

Aqui está o motivo número 1 de bugs em scripts de iniciante: **o que vem de fora do programa chega como texto**. O que a pessoa digita, o que vem de um arquivo, de um e-mail, de um formulário. E texto não faz conta.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> print("25" + "5")
> print(25 + 5)
> ```

<details><summary>Resposta</summary>

```text
255
30
```

Com aspas, são textos, e `+` cola um no outro. Sem aspas, são números, e `+` soma. Se um programa lê dois pesos de uma planilha e "soma" `"125"` com `"130"`, o resultado é `"125130"`, e nenhum erro avisa. Por isso, converta na entrada.

</details>

As funções de conversão têm o nome do tipo de destino:

```python
>>> int("42")
42
>>> float("25.4")
25.4
>>> str(12345)
'12345'
>>> int(25.9)
25
>>> float(7)
7.0
>>> int("  42  ")
42
```

Detalhes importantes:

- `int(25.9)` **corta** as casas decimais (não arredonda): dá `25`, não `26`.
- `int()` e `float()` ignoram espaços nas pontas.
- `str()` transforma qualquer valor em texto.

### Quando a conversão falha: ValueError

Se o texto não representa um número válido, o Python levanta `ValueError`:

```python
>>> int("abc")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: 'abc'
>>> int("25.4")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: '25.4'
>>> float("25,4")
Traceback (most recent call last):
  ...
ValueError: could not convert string to float: '25,4'
```

(Nesta aula, as linhas do meio dos tracebacks foram resumidas com `...`. A seção "Lendo mensagens de erro" mostra um completo.)

Leia a última linha de cada erro: ela diz o tipo do erro e mostra, entre aspas, **o texto exato** que causou o problema. Dois casos que pegam muita gente:

- `int("25.4")` falha: `int()` não aceita texto com casas decimais. Use `float("25.4")` (e, se precisar de inteiro, `int(float("25.4"))`).
- `float("25,4")` falha: o padrão brasileiro usa vírgula, e o Python só aceita ponto. Troque antes: `float("25,4".replace(",", "."))`.

> ⚠️ **Erro comum:** achar que o programa "travou" num `ValueError`. Ele fez a coisa certa: preferiu parar a inventar um número. Inventar seria muito pior num certificado de qualidade. No módulo 06 você vai aprender a tratar esses erros com elegância.

### Exemplo resolvido: somar dois pesos vindos de uma planilha

**Problema:** duas células trazem `"125,5"` e `"130,2"`. Quero o total.

**Raciocínio:** são textos com vírgula. Para cada um: trocar vírgula por ponto, converter com `float()`. Só então somar.

```python
peso_1 = float("125,5".replace(",", "."))
peso_2 = float("130,2".replace(",", "."))
total = peso_1 + peso_2
print("Total:", total, "kg")
```

Saída:

```text
Total: 255.7 kg
```

> 🔧 **Modifique:** tire o `.replace(",", ".")` de um dos pesos e rode. Leia a mensagem de erro com calma: ela diz qual texto o Python não conseguiu converter.

## 10. input(): perguntando ao usuário

`input()` mostra uma mensagem, espera a pessoa digitar e apertar Enter, e devolve o que foi digitado. **Sempre como texto**, mesmo que a pessoa digite um número.

```python
nome = input("Seu nome: ")
idade_texto = input("Sua idade: ")
idade = int(idade_texto)
print("Olá,", nome, "- daqui a 10 anos você terá", idade + 10, "anos.")
```

Uma execução no terminal (o que a pessoa digitou está depois dos dois-pontos):

```text
Seu nome: Ana
Sua idade: 28
Olá, Ana - daqui a 10 anos você terá 38 anos.
```

Sem o `int(...)`, a linha `idade + 10` daria `TypeError`, porque `idade_texto` é `"28"`, um texto.

Duas observações práticas:

- Os **exercícios do curso não usam `input()`**. Eles recebem os valores como parâmetros de função (seção 14). Assim, os testes automáticos conseguem conferir seu código sem ninguém digitar nada.
- O exemplo `exemplos/05_conversoes_e_input.py` **simula** o que seria digitado, para rodar sem parar. Abra o arquivo, troque a linha marcada por `input(...)` e teste a versão interativa.

> 💡 **Dica:** um programa que espera `input()` parece "travado" no terminal. Não está: está esperando você digitar. Se quiser interromper qualquer programa, use `Ctrl+C`.

## 11. f-strings e formatação de números

Montar textos com `+` e `str()` funciona, mas é trabalhoso e cheio de armadilhas:

```python
op = "OP12345"
media = 25.0666
print("A OP " + op + " teve média " + str(media) + " µm")
```

Saída:

```text
A OP OP12345 teve média 25.0666 µm
```

A **f-string** é o jeito moderno. Coloque um `f` antes das aspas e escreva as variáveis entre chaves `{}`:

```python
op = "OP12345"
media = 25.0666
print(f"A OP {op} teve média {media} µm")
```

Saída:

```text
A OP OP12345 teve média 25.0666 µm
```

Dentro das chaves vale qualquer expressão: `{peso / 8}`, `{op.lower()}`, `{len(op)}`. E a conversão para texto é automática.

### Formatando números

Depois do valor, um `:` abre a "especificação de formato". As que você mais vai usar:

```python
>>> media = 25.0666
>>> f"{media:.2f}"
'25.07'
>>> f"{1250.5:,.2f}"
'1,250.50'
>>> f"{0.956:.1%}"
'95.6%'
>>> f"{7:03d}"
'007'
>>> f"{-0.35:+.2f} e {0.35:+.2f}"
'-0.35 e +0.35'
```

| Formato | Significado | Exemplo |
|---|---|---|
| `:.2f` | 2 casas decimais (arredonda na exibição) | `25.0666` → `25.07` |
| `:,.2f` | separador de milhar + 2 casas | `1250.5` → `1,250.50` |
| `:.1%` | multiplica por 100 e põe `%` | `0.956` → `95.6%` |
| `:03d` | inteiro com zeros à esquerda até 3 dígitos | `7` → `007` |
| `:+.2f` | sempre mostra o sinal | `0.35` → `+0.35` |

Repare que `:,.2f` usa o **padrão americano** (vírgula no milhar, ponto no decimal). Para o padrão brasileiro (`1.250,50`) existe um truque com `replace`, que você vai montar no exercício 12. No módulo 05 você verá o assunto a fundo.

### Alinhando colunas

Um número antes do formato define a **largura**; `<`, `>` e `^` alinham à esquerda, à direita e ao centro:

```python
print(f"[{'COF':<10}]")
print(f"[{'COF':>10}]")
print(f"[{'COF':^10}]")
print(f"{'Ensaio':<12}{'Resultado':>10}")
print(f"{'Espessura':<12}{25.07:>10.2f}")
print(f"{'Gramatura':<12}{52.3:>10.2f}")
```

Saída:

```text
[COF       ]
[       COF]
[   COF    ]
Ensaio       Resultado
Espessura        25.07
Gramatura        52.30
```

Com isso você já monta relatórios de terminal bem apresentáveis. Note a combinação `>10.2f`: largura 10, alinhado à direita, 2 casas.

### Exemplo resolvido: uma linha de laudo

**Problema:** imprimir `Peso líquido: 1,217.70 kg (8 bobinas, lote 007)` a partir de `peso = 1217.7`, `bobinas = 8` e `lote = 7`.

**Raciocínio:** separo o texto em partes fixas e partes variáveis. As variáveis vão entre chaves, cada uma com o formato que pede: o peso com milhar e 2 casas (`:,.2f`), o lote com 3 dígitos (`:03d`), as bobinas sem formato.

```python
peso = 1217.7
bobinas = 8
lote = 7
print(f"Peso líquido: {peso:,.2f} kg ({bobinas} bobinas, lote {lote:03d})")
```

Saída:

```text
Peso líquido: 1,217.70 kg (8 bobinas, lote 007)
```

> 🔧 **Modifique:** mude `lote` para `123` e para `1234`. O que acontece com o `:03d` quando o número já tem 3 dígitos ou mais?

> 💡 **Dica:** para depurar, coloque `=` depois do nome: `print(f"{media=}")` mostra `media=25.0666`. Você vê o nome e o valor de uma vez.

> ⚠️ **Erro comum:** esquecer o `f`. `print("Média: {media}")` imprime literalmente `Média: {media}`, com as chaves. Sem erro, sem aviso, só o texto errado no relatório.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> valor = 2.5
> print(f"{valor:.0f} | {3.5:.0f} | {0.5:.0%}")
> ```

<details><summary>Resposta</summary>

Sai `2 | 4 | 50%`. O `:.0f` arredonda para zero casas, e o empate `.5` vai para o número **par** mais próximo (2.5 → 2, 3.5 → 4). Isso não é bug; é o arredondamento "do banqueiro", explicado na próxima seção. E `0.5` em porcentagem é `50%`.

</details>

## 12. O problema do float e o round()

Rode isto no REPL:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 1.1 * 3
3.3000000000000003
```

Não é defeito do Python. Acontece em JavaScript, Java, C e em praticamente toda linguagem que usa float. Até no Excel: ele só esconde boa parte disso porque arredonda o que mostra na célula. O motivo: o computador guarda números em **binário** (base 2), e alguns decimais simples não têm representação exata em binário.

Analogia: tente escrever 1/3 em decimal. Dá `0.3333...` e nunca termina; em algum momento você corta, e o valor fica um pouquinho errado. Com `0.1` em binário acontece o mesmo. O erro é minúsculo (na 17ª casa), mas aparece quando você imprime ou compara.

### round(): arredondar na hora certa

```python
>>> round(0.1 + 0.2, 2)
0.3
>>> round(25.67, 1)
25.7
>>> round(25.67)
26
```

- `round(x, n)` arredonda para `n` casas e devolve `float`.
- `round(x)` sem casas devolve `int`.

Duas surpresas que você **precisa** conhecer:

```python
>>> round(2.5)
2
>>> round(3.5)
4
>>> round(2.675, 2)
2.67
```

1. **Empate vai para o par** ("arredondamento do banqueiro"): `2.5` → `2`, `3.5` → `4`. Isso evita que, somando muitos arredondamentos, o total "puxe" sempre para cima. É o padrão IEEE 754, o mesmo de muitos sistemas financeiros.
2. `round(2.675, 2)` dá `2.67`, não `2.68`, porque `2.675` está guardado como `2.67499999...`. De novo o binário.

Regras práticas:

- **Calcule com todas as casas e arredonde só no fim**, para exibir ou gravar. Arredondar no meio da conta acumula erro.
- Para **exibir**, prefira formatar (`f"{x:.2f}"`) a arredondar o valor.
- Para **comparar** floats, nunca confie na igualdade exata. Use `math.isclose` (próxima seção) ou compare com uma tolerância.
- Para **dinheiro** de verdade (sistemas financeiros), existe o tipo `Decimal`, do módulo `decimal`. Fica para depois; no laboratório, float com arredondamento no fim resolve.

> ⚠️ **Erro comum:** concluir que "o Python calcula errado" e sair arredondando tudo em todo lugar. O cálculo está certo dentro da precisão do float. O que você controla é **quando** arredonda e **como** exibe.

## 13. O módulo math

O Python vem com uma "biblioteca padrão" enorme, organizada em módulos. Para usar um módulo, você o **importa** uma vez, no topo do arquivo:

```python
>>> import math
>>> math.pi
3.141592653589793
>>> math.sqrt(144)
12.0
>>> math.ceil(83.1)
84
>>> math.floor(83.9)
83
>>> math.isclose(0.1 + 0.2, 0.3)
True
```

| Função | O que faz |
|---|---|
| `math.sqrt(x)` | raiz quadrada (devolve float) |
| `math.pi` | o número π (não é função: sem parênteses) |
| `math.ceil(x)` | arredonda **para cima** até o inteiro (teto) |
| `math.floor(x)` | arredonda **para baixo** até o inteiro (piso) |
| `math.isclose(a, b)` | `True` se `a` e `b` são "praticamente iguais" |

Potência não precisa de `math`: use `**`. E raiz também pode ser potência: `144 ** 0.5` dá `12.0`.

### Exemplo resolvido: quantas caixas?

**Problema:** 47 bobinas, 6 por caixa. Quantas caixas a expedição precisa?

**Raciocínio:** `47 / 6 = 7.83`. Não existe 0,83 de caixa, e as bobinas que sobram também precisam de caixa. Logo, arredondo **para cima**, sempre, mesmo que fosse 7,01. Isso é `math.ceil`. Se eu usasse `round`, daria 8 aqui, mas para 7,2 daria 7, e uma bobina ficaria sem caixa.

```python
import math

bobinas = 47
por_caixa = 6
print("Caixas:", math.ceil(bobinas / por_caixa))
```

Saída:

```text
Caixas: 8
```

> 🔧 **Modifique:** troque para 48 bobinas e depois para 49. Compare com `round(bobinas / por_caixa)` e `bobinas // por_caixa`. Qual dos três sempre dá a resposta certa para "quantas caixas"?

> 💡 **Dica:** como descobrir o que existe em `math`? No REPL: `import math` e depois `help(math)` (aperte `q` para sair) ou `dir(math)`. A documentação oficial em português também é ótima: procure "math" em docs.python.org/pt-br/3/. Aprender a consultar a documentação é uma habilidade profissional, não um sinal de que você "não sabe".

## 14. O molde dos exercícios: def e return

Todos os exercícios do curso pedem para você completar **funções**. O assunto é aprofundado no módulo 04; aqui está só o necessário para trabalhar.

Uma função é uma **máquina com entrada e saída**, como um equipamento do laboratório: você coloca o corpo de prova (a entrada), a máquina faz o ensaio e devolve um resultado (a saída). Quem usa a máquina não precisa saber como ela funciona por dentro.

```python
def area_retangulo(largura: float, comprimento: float) -> float:
    """Devolve a área de um retângulo."""
    return largura * comprimento


area = area_retangulo(0.1, 0.1)
print("Área:", round(area, 4), "m²")
print("Outra:", area_retangulo(2, 3))
```

Saída:

```text
Área: 0.01 m²
Outra: 6
```

Peça por peça:

```text
def area_retangulo(largura: float, comprimento: float) -> float:
│   │              │                                    │
│   │              │                                    └─ tipo do resultado (dica)
│   │              └─ parâmetros: os valores de entrada
│   └─ nome da função (snake_case, como variável)
└─ "vou definir uma função"

    """Devolve a área de um retângulo."""   ← docstring: o que ela faz
    return largura * comprimento           ← devolve o resultado e encerra
```

- `def` cria a função, mas **não executa nada**. O código de dentro só roda quando alguém **chama** a função: `area_retangulo(0.1, 0.1)`.
- Na chamada, os valores entre parênteses (os **argumentos**) ocupam os parâmetros na ordem: `largura` recebe `0.1`, `comprimento` recebe `0.1`.
- `return` devolve o resultado para quem chamou. Quem chamou pode guardar numa variável, imprimir ou usar em outra conta.
- O corpo da função é tudo que está **indentado** (recuado 4 espaços) abaixo do `def`. A indentação não é enfeite: é ela que diz ao Python onde a função começa e termina.

Sobre `largura: float` e `-> float`: são **dicas de tipo** (type hints). Elas dizem o que a função espera receber e o que devolve; o Python não obriga, mas o editor usa para avisar erros, e elas documentam o código. Detalhes no módulo 04.

### print não é return

Esta é a confusão número 1 com funções. `print` **mostra** um valor na tela. `return` **devolve** o valor para o programa continuar usando.

> 🔮 **Preveja antes de rodar:** o que aparece na tela?
>
> ```python
> def dobro(numero):
>     return numero * 2
>
>
> def mostrar_dobro(numero):
>     print(numero * 2)
>
>
> a = dobro(21)
> b = mostrar_dobro(21)
> print(a, b)
> ```

<details><summary>Resposta</summary>

```text
42
42 None
```

A primeira linha (`42`) vem do `print` **dentro** de `mostrar_dobro`. A segunda mostra `a` e `b`: `a` recebeu `42` porque `dobro` usa `return`; `b` recebeu `None`, porque `mostrar_dobro` não tem `return`, e toda função sem `return` devolve `None`. Moral: se o resultado vai ser usado depois (e nos exercícios sempre vai, pelos testes), use `return`.

</details>

### Exemplo resolvido: do enunciado à função

**Enunciado:** "Escreva `calcular_gramatura(massa_g, area_m2)` que devolve a gramatura em g/m², arredondada em 1 casa."

**Raciocínio:**

1. O que entra? `massa_g` e `area_m2` (já estão nos parâmetros).
2. O que sai? Um número: gramatura = massa ÷ área, arredondada em 1 casa.
3. Testo a conta no REPL com um caso que eu sei a resposta: 0,523 g em 0,01 m² devem dar 52,3 g/m².

```python
>>> 0.523 / 0.01
52.300000000000004
>>> round(0.523 / 0.01, 1)
52.3
```

4. Agora escrevo a função, trocando os números pelos parâmetros:

```python
def calcular_gramatura(massa_g: float, area_m2: float) -> float:
    """Devolve a gramatura em g/m², com 1 casa decimal."""
    gramatura = massa_g / area_m2
    return round(gramatura, 1)


print(calcular_gramatura(0.523, 0.01))
```

Saída:

```text
52.3
```

### Como é um exercício do curso

Abra `exercicios/ex01_apresentacao.py`. Você verá:

```python
def apresentar(nome: str, idade: int, cidade: str) -> str:
    """Devolve a frase de apresentação com nome, idade e cidade."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
```

A linha `raise NotImplementedError(...)` é um "aviso de obra": ela faz a função dar erro de propósito, para os testes mostrarem que o exercício ainda não foi feito. Seu trabalho:

1. ler o enunciado (a docstring no topo do arquivo);
2. **apagar** a linha do `raise` e escrever seu código no lugar, terminando com `return`;
3. rodar, na pasta `curso-python`: `python curso.py testar 01 ex01`;
4. ler a mensagem dos testes, corrigir e repetir até passar.

> ⚠️ **Erro comum:** esquecer de recuar o código dentro do `def`. Sem os 4 espaços, aparece `IndentationError: expected an indented block after function definition on line 1`. No VS Code, a tecla Tab já insere 4 espaços.

## 15. Pensando como programador

Saber a sintaxe é metade do caminho. A outra metade é saber **o que fazer quando você não sabe o que fazer**. Quatro hábitos que separam quem trava de quem avança:

**1. Decomponha.** Problema grande é a soma de problemas pequenos. "Gerar a ficha de uma amostra" vira: (a) limpar a OP; (b) converter as medições; (c) calcular a média; (d) calcular a faixa; (e) imprimir. Cada item é uma ou duas linhas que você já sabe escrever.

**2. Teste hipóteses no REPL.** Não sabe se `strip()` tira espaços do meio? Não discuta com a dúvida, pergunte ao Python:

```python
>>> "  OP 123  ".strip()
'OP 123'
```

Resposta em 5 segundos: não tira. Para tirar todos, `replace(" ", "")`.

**3. Leia a documentação.** `help(str.replace)` no REPL mostra como usar um método. A documentação oficial em português (docs.python.org/pt-br/3/) tem tutorial e referência completos. Comece pelo tutorial.

**4. Depure com print.** Resultado estranho? Imprima os valores intermediários e veja onde a conta saiu do trilho:

```python
massa_g = 0.523
largura_cm = 10
comprimento_cm = 10
area = largura_cm * comprimento_cm  # esqueci de converter para m²!
print(f"{area=}")
print(f"{massa_g / area=}")
```

Saída:

```text
area=100
massa_g / area=0.00523
```

Gramatura de 0,005 g/m² é absurda (filmes têm dezenas de g/m²). O `print` mostra que a área está em cm², não em m². Achou o erro sem adivinhar.

> 💡 **Dica:** ao usar IA para estudar, peça "me explique por que este código dá TypeError" ou "me dê uma dica sem a resposta", e não "resolva o exercício". O objetivo é você conseguir resolver sozinho na entrevista e no trabalho.

## Lendo mensagens de erro deste módulo

Mensagem de erro (traceback) não é bronca: é um **laudo** do problema. Leia **de baixo para cima**:

1. **última linha**: tipo do erro e descrição;
2. linhas de cima: **arquivo e número da linha** onde aconteceu, com o trecho de código e marcas (`^` ou `~`) apontando o lugar exato.

Um traceback completo, de um script `teste.py`:

```text
Traceback (most recent call last):
  File "C:\curso-python\teste.py", line 2, in <module>
    print("Bobinas: " + quantidade)
          ~~~~~~~~~~~~^~~~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

Tradução: "na linha 2 de teste.py, você tentou juntar (`+`) um texto com um inteiro; só sei concatenar texto com texto". As marcas `~~~^~~~` apontam o `+` problemático. Correção: `"Bobinas: " + str(quantidade)` ou `f"Bobinas: {quantidade}"`.

Os erros mais comuns deste módulo:

| Erro | Exemplo que causa | O que significa | Como corrigir |
|---|---|---|---|
| `NameError: name 'espesura' is not defined. Did you mean: 'espessura'?` | `print(espesura)` | nome não existe (erro de digitação ou variável não criada) | confira a grafia; crie a variável antes de usar |
| `NameError: name 'Print' is not defined. Did you mean: 'print'?` | `Print("Olá")` | maiúscula/minúscula errada | `print` é minúsculo |
| `TypeError: can only concatenate str (not "int") to str` | `"Lote " + 7` | juntou texto com número | `str(7)` ou f-string |
| `ValueError: invalid literal for int() with base 10: 'abc'` | `int("abc")` | o texto não é um inteiro válido | confira o dado; para decimais use `float` |
| `ValueError: could not convert string to float: '12,5'` | `float("12,5")` | vírgula decimal | `.replace(",", ".")` antes |
| `ZeroDivisionError: division by zero` | `100 / pessoas` com `pessoas = 0` | divisão por zero | confira o divisor (módulo 02 ensina a testar antes) |
| `AttributeError: 'int' object has no attribute 'upper'` | `lote = 7` e `lote.upper()` | método de texto num número | converta, ou reveja o tipo da variável |

Erros de **sintaxe** são diferentes: o Python nem começa a rodar, porque não entendeu o texto do programa. Não aparece a linha `Traceback`, só o local:

```text
  File "C:\curso-python\teste.py", line 1
    print("Olá)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

"String não terminada": abriu aspas e não fechou. Outro clássico:

```text
  File "C:\curso-python\teste.py", line 1
    print("Média:", (7 + 8 + 9 / 3)
         ^
SyntaxError: '(' was never closed
```

Parêntese aberto e nunca fechado. Conte os parênteses: cada `(` precisa do seu `)`.

E os de **indentação**:

```text
  File "C:\curso-python\teste.py", line 2
    media = total / 2
IndentationError: unexpected indent
```

"Recuo inesperado": a linha 2 começa com espaços sem motivo (não está dentro de nenhuma função). Tire os espaços.

```text
  File "C:\curso-python\teste.py", line 2
    return n * 2
    ^^^^^^
IndentationError: expected an indented block after function definition on line 1
```

"Esperava um bloco recuado depois da definição da função": o corpo do `def` precisa estar 4 espaços para dentro.

> 💡 **Dica:** às vezes o erro de sintaxe aponta para a linha **seguinte** à que tem o problema (um parêntese não fechado na linha 5 pode estourar na linha 6). Se a linha apontada parece perfeita, olhe a anterior.

## Boas práticas

- **Nomes que explicam**: `peso_liquido_kg`, não `p` ou `x1`. Inclua a unidade quando houver dúvida.
- **snake_case sem acento** para variáveis e funções; MAIÚSCULAS para constantes.
- **Converta na entrada**: transforme texto em número assim que o dado chega, não no meio das contas.
- **Arredonde só no fim**, e prefira formatar na exibição (`:.2f`) a arredondar o valor.
- **f-strings** em vez de `+` com `str()`.
- **Uma ideia por linha**: quebrar uma fórmula em variáveis intermediárias (`area_m2`, `peso_g`) facilita conferir e depurar.
- **Comentários explicam o porquê**, não repetem o código.
- **Teste no REPL** antes de escrever no arquivo.
- **Formate o código** com `ruff format` (o curso já vem configurado). Código bem formatado é mais fácil de ler e é o que as empresas esperam.

## No mundo real

A ficha abaixo junta tudo do módulo num caso de laboratório: os dados chegam como texto (como viriam de um formulário ou planilha), são limpos e convertidos, os cálculos são feitos com nomes claros e o resultado sai numa ficha alinhada. É o arquivo `exemplos/10_ficha_amostra.py`.

```python
import math

# --- Dados de entrada (do jeito que chegam) ---
op_digitada = " op-48213 "
linha = "c"
espessura_1 = "24,8"
espessura_2 = "25,3"
espessura_3 = "25,1"
massa_corpo_prova_g = "0,4710"  # disco de 100 cm²
comprimento_bobina_m = 6000
largura_bobina_mm = 640
espessura_nominal_um = 25.0
tolerancia_pct = 8.0

# --- Limpeza e conversão ---
op = "OP" + op_digitada.upper().replace("OP", "").replace("-", "").strip()
linha = linha.strip().upper()
e1 = float(espessura_1.replace(",", "."))
e2 = float(espessura_2.replace(",", "."))
e3 = float(espessura_3.replace(",", "."))
massa_g = float(massa_corpo_prova_g.replace(",", "."))

# --- Cálculos ---
media_um = (e1 + e2 + e3) / 3
minimo_um = espessura_nominal_um - espessura_nominal_um * tolerancia_pct / 100
maximo_um = espessura_nominal_um + espessura_nominal_um * tolerancia_pct / 100
desvio = (media_um - espessura_nominal_um) / espessura_nominal_um
gramatura = massa_g / 0.01  # 100 cm² = 0,01 m²
peso_kg = gramatura * (largura_bobina_mm / 1000) * comprimento_bobina_m / 1000
diametro_mm = math.sqrt(76**2 + 4 * comprimento_bobina_m * 1000 * (media_um / 1000) / math.pi)

# --- Saída ---
faixa = f"{minimo_um:.2f} a {maximo_um:.2f}"
print("=" * 40)
print(f"{'FICHA DE AMOSTRA':^40}")
print("=" * 40)
print(f"{'OP':<22}{op:>18}")
print(f"{'Linha':<22}{linha:>18}")
print(f"{'Espessura média (µm)':<22}{media_um:>18.2f}")
print(f"{'Faixa (µm)':<22}{faixa:>18}")
print(f"{'Desvio do nominal':<22}{desvio:>+18.2%}")
print(f"{'Gramatura (g/m²)':<22}{gramatura:>18.1f}")
print(f"{'Peso estimado (kg)':<22}{peso_kg:>18,.2f}")
print(f"{'Diâmetro estimado (mm)':<22}{diametro_mm:>18.0f}")
print("-" * 40)
print("Veredito: aprovado ou reprovado? No módulo 02!")
```

Saída:

```text
========================================
            FICHA DE AMOSTRA
========================================
OP                               OP48213
Linha                                  C
Espessura média (µm)               25.07
Faixa (µm)                 23.00 a 27.00
Desvio do nominal                 +0.27%
Gramatura (g/m²)                    47.1
Peso estimado (kg)                180.86
Diâmetro estimado (mm)               444
----------------------------------------
Veredito: aprovado ou reprovado? No módulo 02!
```

Repare na organização em três blocos (entrada, cálculo, saída). Esse padrão vale para scripts de qualquer tamanho e é a semente do projeto final. O que falta? **Decidir**: a média está dentro da faixa? A ficha deve dizer "APROVADO" ou "REPROVADO"? Isso exige `if`, assunto do módulo 02.

## Resumo

| Assunto | Sintaxe essencial |
|---|---|
| Mostrar | `print("a", 1, sep=" - ", end="\n")` |
| Comentário | `# texto ignorado pelo Python` |
| Variável | `peso_kg = 125.5` |
| Tipos | `int` `8` · `float` `25.4` · `str` `"OP1"` · `bool` `True` · `None` |
| Tipo de um valor | `type(valor)` |
| Contas | `+  -  *  /  //  %  **` (precedência: `()` → `**` → `* / // %` → `+ -`) |
| Atualizar | `total += x` · `total -= x` · `total *= x` · `total /= x` |
| Texto | `+` concatena · `*` repete · `len(t)` · `t.upper()` · `t.lower()` · `t.strip()` · `t.replace(a, b)` · `"x" in t` |
| Conversão | `int("42")` · `float("25.4")` · `str(42)` · vírgula: `float(t.replace(",", "."))` |
| Entrada | `texto = input("Pergunta: ")` (sempre devolve `str`) |
| f-string | `f"{valor}"` · `:.2f` · `:,.2f` · `:.1%` · `:03d` · `:+.2f` · `:<10` `:>10` `:^10` · `{x=}` |
| Arredondar | `round(x, 2)` (float) · `round(x)` (int) · empate vai para o par |
| math | `import math` · `math.sqrt` · `math.pi` · `math.ceil` · `math.floor` · `math.isclose` |
| Função | `def nome(param: tipo) -> tipo:` + corpo recuado + `return resultado` |

## Você domina este módulo se...

- [ ] explico, sem consultar, a diferença entre `/`, `//` e `%`, com um exemplo de bobinas ou caixas;
- [ ] prevejo o resultado de `2 + 3 * 4 ** 2` antes de rodar (e acerto);
- [ ] sei por que `"25" + "5"` dá `"255"` e como converter para somar de verdade;
- [ ] transformo `" 12,5 kg "` no número `12.5` usando só métodos de string e `float()`;
- [ ] formato `1250.5` como `1,250.50` e `0.956` como `95.6%` com f-strings, sem consultar;
- [ ] explico por que `0.1 + 0.2` não dá `0.3` e quando usar `round` ou `:.2f`;
- [ ] explico a diferença entre `print` e `return` numa função e por que os exercícios usam `return`;
- [ ] leio a última linha de um traceback e digo o tipo de erro, a linha e a causa provável.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_apresentacao` | ★☆☆ | f-string, return |
| 02 | `ex02_cabecalho` | ★☆☆ | print, repetição de string, upper |
| 03 | `ex03_media_notas` | ★☆☆ | precedência, parênteses |
| 04 | `ex04_celsius_fahrenheit` | ★☆☆ | fórmulas, ordem das operações |
| 05 | `ex05_contem_termo` | ★☆☆ | `in`, lower, strip, bool |
| 06 | `ex06_peso_liquido` | ★★☆ | contas encadeadas, round |
| 07 | `ex07_dividir_conta` | ★★☆ | porcentagem, round, f-string com `:.2f`, ZeroDivisionError |
| 08 | `ex08_normalizar_op` | ★★☆ | upper, replace encadeado |
| 09 | `ex09_gramatura` | ★★☆ | conversão de unidades, round |
| 10 | `ex10_faixa_tolerancia` | ★★☆ | tolerância ± %, função chamando função, `:.2f` |
| 11 | `ex11_texto_para_numero` | ★★☆ | limpeza de texto, float(), ValueError, problema do float |
| 12 | `ex12_formatar_reais` | ★★★ | `:,.2f` + troca de separadores |
| 13 | `ex13_diametro_bobina` | ★★★ | `math.sqrt`, `math.pi`, unidades, fórmula inversa |
| 14 | `ex14_tempo_de_producao` | ★★★ | `math.ceil`, `//`, `%`, `:02d` |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de `raise NotImplementedError`, e rode na pasta `curso-python`:

```text
python curso.py testar 01 ex01
```

Para testar o módulo inteiro: `python curso.py testar 01`. Faça na ordem: os primeiros preparam os seguintes. Depois de passar, compare com `solucoes/`: muitas vezes há uma alternativa comentada.

## Desafio do módulo

**Ficha de medição da bobina:** um script que recebe os dados brutos de uma amostra (OP mal digitada, medições com vírgula, massa do corpo de prova, dimensões da bobina) e imprime uma ficha completa e alinhada, com média, faixa de tolerância, desvio, gramatura, peso e diâmetro estimados e os valores no formato brasileiro. Enunciado, requisitos e critérios de aceite em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md) (15 perguntas, gabarito comentado no final).

## Para ir além

- Tutorial oficial em português, capítulo 3, "Uma introdução informal ao Python": <https://docs.python.org/pt-br/3/tutorial/introduction.html>
- Formatação de strings (f-strings e a "mini-linguagem" de formato): <https://docs.python.org/pt-br/3/tutorial/inputoutput.html> e <https://docs.python.org/pt-br/3/library/string.html#formatspec>
- Aritmética de ponto flutuante, problemas e limitações: <https://docs.python.org/pt-br/3/tutorial/floatingpoint.html>
- Módulo `math`: <https://docs.python.org/pt-br/3/library/math.html>
- Métodos de string: <https://docs.python.org/pt-br/3/library/stdtypes.html#string-methods>
- Leitura extra: PEP 8, o guia de estilo do Python (seções "Naming Conventions" e "Comments"): <https://peps.python.org/pep-0008/>
