# Módulo 03 — Coleções: listas, tuplas, dicionários e conjuntos

> **Tempo estimado:** 8 a 12 horas · **Pré-requisitos:** módulos 00, 01 e 02 · **Nível:** iniciante

## O que você vai aprender

- Criar listas, acessar itens por índice (inclusive negativo) e recortar trechos com fatiamento.
- Modificar listas com `append`, `insert`, `remove`, `pop` e `sort`, sabendo quais métodos devolvem `None`.
- Explicar com um desenho a diferença entre **cópia e referência**, e copiar uma lista (ou um dicionário de listas) sem efeitos surpresa.
- Usar tuplas para registros fixos e desempacotar valores (`op, peso = pedido`).
- Criar e consultar dicionários com `[]` e `get`, percorrer com `items()` e montar contagens e agrupamentos.
- Navegar num dicionário aninhado, como a tabela de tolerâncias por linha.
- Usar conjuntos para tirar repetições e cruzar listas (o que está nas duas, o que falta em uma).
- Percorrer com `enumerate` e `zip`, e usar `sum`, `min`, `max`, `any`, `all` e `sorted` com `key`.
- Escrever compreensões de lista, dicionário e conjunto, e saber quando um `for` comum é melhor.
- Tratar uma **lista de dicionários como tabela**: filtrar, escolher colunas, ordenar, agrupar e juntar. É a mesma lógica do pandas e do SQL.

## Por que isso importa

Até agora, cada variável guardava um valor. Uma espessura. Uma nota. Um peso.

Seu trabalho nunca é um valor só. É a série de medições de uma bobina. É a planilha com as amostras do dia. É a tabela de tolerâncias de cada linha. É a lista de OPs que a expedição pediu por e-mail.

**Coleções** são o jeito de o Python guardar muitos valores organizados. Sem elas não existe análise de dados, automação nem API:

- um DataFrame do pandas (módulo 10) é uma tabela, e você vai montá-la a partir de listas e dicionários;
- uma consulta SQL (módulo 11) devolve uma lista de linhas;
- o JSON de uma API (módulos 12 e 13) é feito de dicionários e listas.

No projeto final, as tolerâncias por linha viram um dicionário aninhado, os valores da planilha viram uma lista de dicionários e o cruzamento "OPs do e-mail × OPs com resultado" é uma operação de conjuntos. Você vai escrever versões pequenas de tudo isso neste módulo.

## 1. Listas: vários valores numa variável só

Pense numa coluna do Excel com as espessuras das bobinas da linha A. Cada valor ocupa uma posição. Em Python, isso é uma **lista**: valores entre colchetes, separados por vírgula. (Abra o REPL com `python` no PowerShell e digite junto: ver a saída na sua tela fixa muito mais do que ler.)

```python
>>> espessuras = [50.2, 49.8, 51.0, 50.5, 48.9]
>>> espessuras
[50.2, 49.8, 51.0, 50.5, 48.9]
>>> len(espessuras)
5
```

Cada item tem um **índice**: a posição dele. A diferença do Excel é que o Python começa a contar do **zero**.

```text
 índice:       0      1      2      3      4
             +------+------+------+------+------+
 espessuras  | 50.2 | 49.8 | 51.0 | 50.5 | 48.9 |
             +------+------+------+------+------+
 negativo:    -5     -4     -3     -2     -1
```

```python
>>> espessuras[0]
50.2
>>> espessuras[2]
51.0
>>> espessuras[-1]
48.9
>>> espessuras[-2]
50.5
```

O índice negativo conta do fim para o começo. `espessuras[-1]` é sempre o último, não importa o tamanho da lista. Isso é muito mais seguro do que `espessuras[len(espessuras) - 1]`.

Você também troca um item pelo índice:

```python
>>> espessuras[1] = 49.9
>>> espessuras
[50.2, 49.9, 51.0, 50.5, 48.9]
```

Lista vazia é `[]`, e `list(range(5))` vira `[0, 1, 2, 3, 4]`. Uma lista pode misturar tipos (`["OP-4512", "A", 1250.5]`), mas na prática prefira listas de **uma coisa só**: só espessuras, só OPs. Para um registro com campos diferentes, você vai ver ferramentas melhores (tuplas e dicionários) daqui a pouco.

> ⚠️ **Erro comum:** pedir um índice que não existe. A lista acima tem 5 itens, então `espessuras[5]` dá `IndexError: list index out of range`. Com `n` itens, os índices vão de `0` a `n - 1`.

O exemplo completo está em `exemplos/01_listas.py`. No PowerShell, dentro da pasta `03-colecoes`:

```text
python exemplos\01_listas.py
```

(No Linux/macOS, use `python3 exemplos/01_listas.py`.)

**Tente você:** dada `notas = [7.0, 8.5, 6.0, 9.5]`, pegue o `9.5` de dois jeitos diferentes.

<details><summary>Resposta</summary>

`notas[3]` e `notas[-1]`. Qual usar? Se a pergunta é "qual a última nota?", use `notas[-1]`: continua certo mesmo se a lista crescer. `notas[3]` só faz sentido quando a posição 3 tem um significado fixo (por exemplo, "a 4ª prova").

</details>

## 2. Fatiamento: recortando pedaços

Às vezes você não quer um item, quer um **trecho**: as 3 primeiras medições, as 2 últimas. Para isso existe o **fatiamento** (*slicing*): `lista[inicio:fim]`.

A melhor forma de entender é imaginar **cortes entre os itens**, numerados assim:

```text
 cortes:   0      1      2      3      4      5
           |      |      |      |      |      |
           +------+------+------+------+------+
           | 50.2 | 49.8 | 51.0 | 50.5 | 48.9 |
           +------+------+------+------+------+

 medicoes[1:4]  ->  do corte 1 ao corte 4  ->  [49.8, 51.0, 50.5]
```

O item do `fim` **não entra**. `[1:4]` pega os índices 1, 2 e 3. Quantos itens? `4 - 1 = 3`.

```python
>>> medicoes = [50.2, 49.8, 51.0, 50.5, 48.9, 50.1]
>>> medicoes[1:4]
[49.8, 51.0, 50.5]
>>> medicoes[:3]
[50.2, 49.8, 51.0]
>>> medicoes[3:]
[50.5, 48.9, 50.1]
>>> medicoes[-2:]
[48.9, 50.1]
```

- Sem `inicio`: começa do começo. Sem `fim`: vai até o fim.
- `[:3]` = "os 3 primeiros". `[-2:]` = "os 2 últimos".

Existe um terceiro número, o **passo**: `lista[inicio:fim:passo]`.

```python
>>> medicoes[::2]
[50.2, 51.0, 48.9]
>>> medicoes[::-1]
[50.1, 48.9, 50.5, 51.0, 49.8, 50.2]
```

Duas propriedades importantes:

1. **Fatiar nunca dá `IndexError`.** Se o fim passa do tamanho, ele simplesmente para no fim: `medicoes[:100]` devolve a lista toda.
2. **Fatiar sempre cria uma lista nova.** `medicoes[:]` é uma cópia da lista inteira (isso vai ser importante na seção 4).

Strings também fatiam, do mesmo jeito: `"OP-4512-A"[3:7]` é `'4512'` e `"OP-4512-A"[-1]` é `'A'`.

> 🔮 **Preveja antes de rodar:** você quer as `n` últimas medições e escreve `medicoes[-n:]`. O que acontece quando `n = 0`?
>
> ```python
> n = 0
> print(medicoes[-n:])
> ```

<details><summary>Resposta</summary>

Imprime a lista **inteira**: `[50.2, 49.8, 51.0, 50.5, 48.9, 50.1]`.

Por quê? `-0` é igual a `0`. Então `medicoes[-0:]` vira `medicoes[0:]`, que é "do começo até o fim". Quando `n` pode ser zero, trate esse caso antes com um `if n <= 0`. O exercício 01 cobra exatamente isso.

</details>

> 🔧 **Modifique:** em `exemplos/02_fatiamento.py`, troque `medicoes[1:4]` por `medicoes[4:1]` e por `medicoes[4:1:-1]`. Explique por que um devolve `[]` e o outro não.

## 3. Modificando listas: os métodos

Listas têm **métodos**: funções que você chama com um ponto depois do nome (`lista.append(x)`). Os mais usados:

| Método | O que faz | Devolve |
|---|---|---|
| `lista.append(x)` | acrescenta `x` no fim | `None` |
| `lista.extend(outra)` | acrescenta todos os itens de `outra` no fim | `None` |
| `lista.insert(i, x)` | insere `x` na posição `i` | `None` |
| `lista.remove(x)` | remove a **primeira** ocorrência de `x` | `None` |
| `lista.pop()` / `lista.pop(i)` | remove o último (ou o da posição `i`) | o item removido |
| `lista.index(x)` | posição da primeira ocorrência de `x` | um `int` |
| `lista.count(x)` | quantas vezes `x` aparece | um `int` |
| `lista.sort()` | ordena a própria lista | `None` |
| `lista.copy()` | cria uma cópia rasa | uma lista nova |

Veja alguns em ação:

```python
>>> ops = ["OP-4512", "OP-4513"]
>>> ops.append("OP-4514")
>>> ops.insert(0, "OP-4500")
>>> ops
['OP-4500', 'OP-4512', 'OP-4513', 'OP-4514']
>>> ops.extend(["OP-4515", "OP-4516"])
>>> ops.remove("OP-4513")
>>> ultima = ops.pop()
>>> ultima
'OP-4516'
>>> ops
['OP-4500', 'OP-4512', 'OP-4514', 'OP-4515']
```

Operadores também funcionam: `[1, 2] + [3]` dá `[1, 2, 3]`, `[0] * 4` dá `[0, 0, 0, 0]` e `"OP-4512" in ops` dá `True`.

### `sort()` ou `sorted()`?

- `lista.sort()` **ordena a própria lista** e devolve `None`.
- `sorted(lista)` **devolve uma lista nova** ordenada e não mexe na original.

```python
>>> notas = [7.5, 9.0, 6.0]
>>> sorted(notas)
[6.0, 7.5, 9.0]
>>> notas
[7.5, 9.0, 6.0]
>>> notas.sort(reverse=True)
>>> notas
[9.0, 7.5, 6.0]
```

> 🔮 **Preveja antes de rodar:** o que este código imprime?
>
> ```python
> medicoes = [50.2, 49.8, 51.0]
> medicoes = medicoes.sort()
> print(medicoes)
> ```

<details><summary>Resposta</summary>

Imprime `None`. O `sort()` ordenou a lista e devolveu `None`, e a linha `medicoes = ...` guardou esse `None` na variável. A lista ordenada se perdeu.

Regra prática: **métodos que modificam a lista no lugar devolvem `None`**. Use `medicoes.sort()` sozinho na linha, ou `medicoes = sorted(medicoes)`.

</details>

### Como descobrir sozinho o que um método faz

Você não precisa decorar a tabela. No REPL, `help(list.remove)` mostra a documentação do método (aperte `q` para sair). Ou teste uma hipótese. "Será que `remove` apaga **todas** as ocorrências?" Não adivinhe, pergunte ao Python:

```python
>>> teste = [1, 2, 1, 3]
>>> teste.remove(1)
>>> teste
[2, 1, 3]
```

Só a primeira. Esse hábito (criar um exemplo mínimo no REPL para tirar a dúvida) vai economizar horas da sua vida de programador. A documentação oficial das listas está em [docs.python.org/pt-br/3/tutorial/datastructures.html](https://docs.python.org/pt-br/3/tutorial/datastructures.html).

## 4. Mutabilidade: cópia ou referência?

Esta é a seção mais importante do módulo. Os bugs mais estranhos de iniciante (e de muito profissional) vêm daqui.

### 4.1 Variáveis são etiquetas, não caixas

No módulo 01, dissemos que uma variável "guarda" um valor. Agora vamos ser mais precisos: **uma variável é uma etiqueta presa num objeto**. O objeto (a lista) mora na memória; o nome só aponta para ele.

```python
>>> a = [50.2, 49.8]
>>> b = a
>>> b.append(51.0)
>>> a
[50.2, 49.8, 51.0]
```

Mexemos em `b` e `a` mudou. Por quê? Porque `b = a` **não copiou a lista**. Só colou uma segunda etiqueta no mesmo objeto:

```text
 b = a            (NÃO copia: só cola mais uma etiqueta)

     a ---------> +------+------+
                  | 50.2 | 49.8 |
     b ---------> +------+------+

 b.append(51.0)   (muda o objeto; os dois nomes "veem")

     a ---------> +------+------+------+
                  | 50.2 | 49.8 | 51.0 |
     b ---------> +------+------+------+
```

Uma analogia do seu dia a dia: `b = a` é como mandar o **link** de uma planilha do OneDrive. Quem edita pelo link muda a planilha de todo mundo. Copiar de verdade é mandar a planilha **em anexo**: cada um fica com a sua.

Como provar que são o mesmo objeto? Com o operador `is`:

```python
>>> a is b
True
```

- `==` pergunta: "têm o **mesmo conteúdo**?"
- `is` pergunta: "são o **mesmo objeto**?" (o mesmo que comparar `id(a) == id(b)`; `id()` é o "número de série" do objeto na memória).

### 4.2 Como copiar de verdade

Três formas equivalentes de copiar uma lista: `original.copy()`, `original[:]` e `list(original)`.

```python
>>> original = [50.2, 49.8]
>>> copia = original.copy()
>>> original == copia, original is copia
(True, False)
>>> copia.append(51.0)
>>> original
[50.2, 49.8]
```

Agora são dois objetos, cada um com sua etiqueta. Dicionários e conjuntos também têm `.copy()`.

### 4.3 Mutáveis e imutáveis

Alguns tipos **podem mudar** depois de criados; outros **não**.

| Imutáveis (não mudam) | Mutáveis (mudam no lugar) |
|---|---|
| `int`, `float`, `bool`, `None` | `list` |
| `str` | `dict` |
| `tuple` | `set` |

Com imutáveis, "mudar" sempre cria um objeto novo e move a etiqueta. Por isso este código é tranquilo:

```python
>>> x = 10
>>> y = x
>>> x += 1
>>> x, y
(11, 10)
```

O `x += 1` criou o objeto `11` e moveu só a etiqueta `x`; `y` continua no `10`. Com strings é igual: `texto.upper()` não muda `texto`, devolve uma string nova. Você já viu isso no módulo 01.

> 🔮 **Preveja antes de rodar:** o que aparece nas duas últimas linhas?
>
> ```python
> a = [1, 2]
> b = a
> a += [3]
> print(b)
> a = a + [4]
> print(a, b)
> ```

<details><summary>Resposta</summary>

```text
[1, 2, 3]
[1, 2, 3, 4] [1, 2, 3]
```

Com listas, `a += [3]` **modifica a lista no lugar** (como um `extend`), então `b` vê o 3. Já `a = a + [4]` **cria uma lista nova** e move só a etiqueta `a`. Daí em diante, `a` e `b` apontam para objetos diferentes.

</details>

### 4.4 Cópia rasa × cópia profunda

`.copy()` copia só **a caixa de fora**. Se dentro dela houver outras listas, as de dentro continuam compartilhadas. Isso se chama **cópia rasa** (*shallow copy*).

```python
>>> por_linha = {"A": [50.2, 49.8], "B": [20.1]}
>>> rasa = por_linha.copy()
>>> rasa["C"] = [35.0]
>>> "C" in por_linha
False
>>> rasa["A"].append(99.9)
>>> por_linha["A"]
[50.2, 49.8, 99.9]
```

Acrescentar a chave `"C"` em `rasa` não afetou o original (o dicionário é novo). Mas o `append` em `rasa["A"]` afetou! Veja por quê:

```text
 rasa = por_linha.copy()

  por_linha --> { "A": * , "B": * }   dicionário original
                       |        |
                       v        v
                 [50.2, 49.8] [20.1]  as listas existem UMA vez só
                       ^        ^
                       |        |
  rasa -------> { "A": * , "B": * }   dicionário NOVO, mesmas listas
```

É como copiar uma pasta cheia de **atalhos**: a pasta é nova, mas os atalhos abrem os mesmos arquivos.

Para copiar "até o fundo", use `copy.deepcopy` (o módulo `copy` vem com o Python; você importa como importou o `math` no módulo 01):

```python
>>> import copy
>>> por_linha = {"A": [50.2, 49.8], "B": [20.1]}
>>> profunda = copy.deepcopy(por_linha)
>>> profunda["A"].append(99.9)
>>> por_linha["A"]
[50.2, 49.8]
```

> ⚠️ **Erro comum:** criar uma "grade" com `[[0] * 3] * 3`. O `* 3` de fora repete **a mesma lista interna** três vezes:
>
> ```python
> >>> grade = [[0] * 3] * 3
> >>> grade[0][0] = 1
> >>> grade
> [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
> ```
>
> A forma certa usa uma compreensão (seção 10), que cria uma lista nova a cada volta: `[[0] * 3 for _ in range(3)]`. O `_` é o nome convencional para "variável que eu não vou usar".

### 4.5 Funções recebem o mesmo objeto

Quando você passa uma lista para uma função, a função recebe **uma etiqueta para a mesma lista**, não uma cópia. Se a função modificar a lista, quem chamou vê a mudança.

**Exemplo resolvido: a função que estragava os dados brutos.** Um analista escreveu esta função para descontar o *offset* do micrômetro:

```python
>>> def corrigir_offset(medicoes, offset):
...     for i in range(len(medicoes)):
...         medicoes[i] = round(medicoes[i] - offset, 2)
...     return medicoes
...
>>> brutas = [50.4, 49.9, 51.2]
>>> corrigidas = corrigir_offset(brutas, 0.2)
>>> corrigidas
[50.2, 49.7, 51.0]
>>> brutas
[50.2, 49.7, 51.0]
```

O resultado está certo, mas os dados **brutos sumiram**. Se o laudo precisar mostrar o valor medido, ele não existe mais.

Como eu penso para consertar:

1. **Quem é dono da lista?** Quem chamou a função. A função só deveria **ler**.
2. **O que a função precisa entregar?** Uma lista com os valores corrigidos.
3. **Então:** monto uma lista **nova** e devolvo ela. A recebida fica intacta.

```python
>>> def corrigir_offset(medicoes, offset):
...     corrigidas = []
...     for valor in medicoes:
...         corrigidas.append(round(valor - offset, 2))
...     return corrigidas
...
>>> brutas = [50.4, 49.9, 51.2]
>>> corrigir_offset(brutas, 0.2)
[50.2, 49.7, 51.0]
>>> brutas
[50.4, 49.9, 51.2]
```

Regra que vale para o curso inteiro: **uma função não deve modificar a coleção que recebeu**, a menos que esse seja o objetivo declarado dela (como o `sort()`). No módulo 04 você vai ver que isso tem nome: função **pura**.

> 🔮 **Preveja antes de rodar:** você quer tirar os valores acima de 50 de uma lista. O que sobra?
>
> ```python
> valores = [10, 55, 60, 20]
> for v in valores:
>     if v > 50:
>         valores.remove(v)
> print(valores)
> ```

<details><summary>Resposta</summary>

`[10, 60, 20]`. O 60 escapou!

O `for` anda por **posições**. Na posição 1 está o 55: ele é removido e todo mundo anda uma casa para a esquerda (o 60 vai para a posição 1). O `for` segue para a posição 2, que agora é o 20. O 60 nunca foi olhado.

Nunca remova itens da lista que você está percorrendo. Monte uma lista nova com o que fica: `[v for v in valores if v <= 50]`.

</details>

> 🔧 **Modifique:** rode `exemplos/03_mutabilidade.py`, depois cole o código em [pythontutor.com](https://pythontutor.com) (escolha Python 3) e avance passo a passo. Você vai **ver** as setas dos diagramas acima.

## 5. Tuplas e desempacotamento

Uma **tupla** é como uma lista que não pode mudar. Usa parênteses:

```python
>>> bobina = ("OP-4512", "A", 1250.5)
>>> bobina[0]
'OP-4512'
>>> len(bobina)
3
>>> bobina[2] = 1300.0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

Para que serve uma "lista que não muda"?

- **Registros fixos:** (OP, linha, peso); (mínimo, máximo); (latitude, longitude). A posição tem significado e não deve mudar.
- **Devolver vários valores** de uma função (módulo 04).
- **Chaves de dicionário:** tuplas podem ser chaves, listas não (seção 7).
- **Segurança:** quem recebe sua tupla não consegue alterá-la sem querer.

### Desempacotamento

O poder real das tuplas está no **desempacotamento**: cada posição vai para uma variável. Funciona com qualquer sequência (listas também) e deixa o código muito mais legível. Compare `peso` com `bobina[2]`: qual dos dois explica melhor o que é?

```python
>>> op, linha, peso = bobina
>>> peso
1250.5
>>> minimo, maximo = 55.0, 45.0
>>> minimo, maximo = maximo, minimo
>>> minimo, maximo
(45.0, 55.0)
>>> medicoes = [50.2, 49.8, 51.0, 50.5]
>>> primeira, *meio, ultima = medicoes
>>> meio
[49.8, 51.0]
>>> pedidos = [("OP-4512", 500.0), ("OP-4513", 320.5)]
>>> for op, peso in pedidos:
...     print(f"{op}: {peso} kg")
...
OP-4512: 500.0 kg
OP-4513: 320.5 kg
```

- `minimo, maximo = maximo, minimo` troca dois valores sem variável auxiliar.
- `*meio` recolhe "o resto" (sempre vira lista).
- `for op, peso in pedidos` desempacota cada tupla da lista, a cada volta.

> ⚠️ **Erro comum:** tupla de um item só. `(50.2)` é só um número entre parênteses. A vírgula é que faz a tupla: `(50.2,)`.

> ⚠️ **Erro comum:** número de variáveis diferente do número de itens. `op, peso = ("OP-4512", "A", 1250.5)` dá `ValueError: too many values to unpack (expected 2)`: são 3 itens para 2 variáveis.

Exemplo completo: `exemplos/04_tuplas.py`.

## 6. Percorrendo melhor: `enumerate` e `zip`

### `enumerate`: posição e valor juntos

No módulo 02, para saber a posição você faria `for i in range(len(medicoes))`. Funciona, mas é feio e fácil de errar. O `enumerate` entrega a dupla (posição, valor):

```python
>>> medicoes = [50.2, 44.1, 51.0]
>>> for ponto, valor in enumerate(medicoes, start=1):
...     print(f"Ponto {ponto}: {valor} µm")
...
Ponto 1: 50.2 µm
Ponto 2: 44.1 µm
Ponto 3: 51.0 µm
```

`start=1` faz a contagem começar em 1, como o analista conta os pontos. Sem ele, começa em 0.

### `zip`: andar por várias listas ao mesmo tempo

Duas colunas de uma planilha (OPs e pesos) viram duas listas. O `zip` junta o 1º com o 1º, o 2º com o 2º...

```python
>>> ops = ["OP-4512", "OP-4513", "OP-4514"]
>>> pesos = [500.0, 320.5, 210.0]
>>> for op, peso in zip(ops, pesos, strict=True):
...     print(op, peso)
...
OP-4512 500.0
OP-4513 320.5
OP-4514 210.0
>>> dict(zip(ops, pesos, strict=True))
{'OP-4512': 500.0, 'OP-4513': 320.5, 'OP-4514': 210.0}
```

> ⚠️ **Erro comum:** listas de tamanhos diferentes. Sem `strict=True`, o `zip` **para na mais curta sem avisar**, e você perde dados em silêncio:
>
> ```python
> >>> list(zip(["OP-1", "OP-2"], [500.0, 320.5, 210.0]))
> [('OP-1', 500.0), ('OP-2', 320.5)]
> ```
>
> Com `strict=True` (Python 3.10+), o Python reclama com `ValueError`. Prefira sempre ele; o ruff, que você vai usar no curso, até avisa quando falta. Se você não quer que o programa pare, confira `len()` das listas antes.

Exemplo completo: `exemplos/05_enumerate_zip.py`.

## 7. Dicionários: buscar pelo nome, não pela posição

Numa lista, você acha as coisas pela **posição**. Mas qual é o peso da OP-4513? Você teria que procurar item por item.

Um **dicionário** guarda pares **chave → valor**. Você acha o valor pela chave, na hora. É o **PROCV** do Python: você dá a chave, ele devolve o valor.

```python
>>> peso_da_op = {"OP-4512": 500.0, "OP-4513": 320.5}
>>> peso_da_op["OP-4513"]
320.5
>>> len(peso_da_op)
2
```

### Acrescentar, alterar e remover

A mesma sintaxe acrescenta (se a chave é nova) ou altera (se já existe):

```python
>>> peso_da_op["OP-4514"] = 210.0
>>> peso_da_op["OP-4512"] = 510.0
>>> peso_da_op
{'OP-4512': 510.0, 'OP-4513': 320.5, 'OP-4514': 210.0}
>>> peso_da_op.pop("OP-4513")
320.5
>>> del peso_da_op["OP-4514"]
>>> peso_da_op
{'OP-4512': 510.0}
```

Desde o Python 3.7, o dicionário **lembra a ordem em que as chaves entraram**.

### `[]` ou `get`?

Chave que não existe com `[]` dá erro. Com `get`, devolve `None` (ou um padrão que você escolher):

```python
>>> peso_da_op["OP-9999"]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'OP-9999'
>>> print(peso_da_op.get("OP-9999"))
None
>>> peso_da_op.get("OP-9999", 0.0)
0.0
>>> "OP-4512" in peso_da_op
True
```

Quando usar cada um:

- `dic[chave]` quando a chave **tem que existir**. Se não existir, é bug, e é bom o programa parar e avisar.
- `dic.get(chave)` quando faltar é **normal** (uma OP que ainda não tem resultado).
- `chave in dic` para perguntar se existe. O `in` olha as **chaves**, não os valores.

### Percorrendo

```python
>>> peso_da_op = {"OP-4512": 500.0, "OP-4513": 320.5}
>>> for op, peso in peso_da_op.items():
...     print(f"{op} -> {peso} kg")
...
OP-4512 -> 500.0 kg
OP-4513 -> 320.5 kg
>>> sum(peso_da_op.values())
820.5
```

`items()` entrega pares (chave, valor); desempacote direto no `for`. `keys()` e `values()` entregam só um dos lados. Um `for` direto no dicionário (`for op in peso_da_op`) passa pelas chaves.

### O que pode ser chave?

Chaves precisam ser **imutáveis**: `str`, `int`, `float`, `tuple`. Uma tupla como `("A", 1)` (linha, ponto) é uma ótima chave. Uma lista não serve: `{["A", 1]: 50.2}` dá `TypeError: unhashable type: 'list'`, o jeito do Python dizer "isso pode mudar, então não serve de chave".

### Os dois padrões que você vai usar a vida toda

**Exemplo resolvido: contar defeitos por tipo.** O inspetor anotou os defeitos de um lote, um por linha:

```python
>>> defeitos = ["bolha", "risco", "bolha", "gel", "bolha", "risco"]
```

Quero saber quantos de cada. Como eu penso:

1. A resposta tem cara de "para cada defeito, um número". **"Para cada X, um Y" = dicionário.**
2. Começo com um dicionário vazio e passo por cada defeito.
3. Para cada um: se já existe no dicionário, somo 1; se não, começa em 1. O `get(defeito, 0)` faz as duas coisas: devolve o valor atual, ou 0 se ainda não existe.

```python
>>> contagem = {}
>>> for defeito in defeitos:
...     contagem[defeito] = contagem.get(defeito, 0) + 1
...
>>> contagem
{'bolha': 3, 'risco': 2, 'gel': 1}
```

**Padrão de agrupamento:** em vez de contar, junto os valores de cada grupo numa lista.

```python
>>> bobinas = [("A", 50.2), ("B", 20.1), ("A", 49.8), ("B", 19.9), ("A", 51.0)]
>>> por_linha = {}
>>> for linha, espessura in bobinas:
...     if linha not in por_linha:
...         por_linha[linha] = []
...     por_linha[linha].append(espessura)
...
>>> por_linha
{'A': [50.2, 49.8, 51.0], 'B': [20.1, 19.9]}
```

O `if ... not in` cria a lista vazia na primeira vez. Existe um atalho que faz o mesmo numa linha: `por_linha.setdefault(linha, []).append(espessura)`. O `setdefault` devolve a lista que já está lá, ou cria uma vazia e devolve.

> 🔧 **Modifique:** troque o padrão de agrupamento para **somar** as espessuras de cada linha em vez de guardá-las numa lista. (Dica: é parecido com a contagem.)

### Juntando dicionários

No seu projeto, a OP pode ter uma especificação própria que **substitui** parte do padrão da linha. O operador `|` (Python 3.9+) junta dois dicionários; nas chaves repetidas, **vence o da direita**:

```python
>>> padrao_da_linha = {"nominal": 50.0, "tol_pct": 10.0, "cof_max": 0.30}
>>> especificacao_da_op = {"tol_pct": 5.0}
>>> padrao_da_linha | especificacao_da_op
{'nominal': 50.0, 'tol_pct': 5.0, 'cof_max': 0.3}
```

Essa linha é, literalmente, a regra "use a especificação da OP; o que ela não define, vem do padrão da linha". Outra forma que você vai ver por aí: `{**padrao_da_linha, **especificacao_da_op}`.

> 🔮 **Preveja antes de rodar:** quantas chaves tem `estoque` no final, e qual o valor de `"L-101"`?
>
> ```python
> estoque = {"L-101": 3}
> estoque["L-102"] = 5
> estoque["L-101"] = estoque.get("L-101", 0) + 2
> estoque["l-101"] = 1
> print(len(estoque), estoque["L-101"])
> ```

<details><summary>Resposta</summary>

Imprime `3 5`. São 3 chaves: `"L-101"`, `"L-102"` e `"l-101"`. Para o Python, `"l-101"` (minúsculo) é outra chave. Por isso, ao usar textos digitados como chave, normalize antes (`.strip().upper()`). E `"L-101"` vale `3 + 2 = 5`.

</details>

Exemplo completo: `exemplos/06_dicionarios.py`.

## 8. Dicionários aninhados: a tabela de tolerâncias

O valor de um dicionário pode ser **qualquer coisa**, inclusive outro dicionário. É assim que você representa a tabela de tolerâncias: para cada linha, para cada propriedade, a regra.

```python
>>> TOLERANCIAS = {
...     "A": {
...         "espessura": {"nominal": 50.0, "tol_pct": 10.0},
...         "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
...         "cof": {"min": 0.15, "max": 0.30},
...     },
...     "B": {
...         "espessura": {"nominal": 20.0, "tol_pct": 8.0},
...         "cof": {"min": 0.20, "max": 0.40},
...     },
... }
```

Desenhando como árvore:

```text
 TOLERANCIAS
 |
 +-- "A"
 |    +-- "espessura" --> {"nominal": 50.0, "tol_pct": 10.0}
 |    +-- "gramatura" --> {"nominal": 46.0, "tol_pct": 5.0}
 |    +-- "cof"       --> {"min": 0.15, "max": 0.30}
 |
 +-- "B"  (mesma ideia: espessura e cof)
```

Cada `[]` desce um nível:

```python
>>> TOLERANCIAS["A"]["espessura"]["nominal"]
50.0
>>> regra = TOLERANCIAS["A"]["espessura"]
>>> minimo = round(regra["nominal"] * (1 - regra["tol_pct"] / 100), 2)
>>> maximo = round(regra["nominal"] * (1 + regra["tol_pct"] / 100), 2)
>>> minimo, maximo
(45.0, 55.0)
```

Guardar um nível numa variável (`regra`) evita linhas enormes como `TOLERANCIAS["A"]["espessura"]["tol_pct"]` repetidas.

Para acessar com segurança um caminho que pode não existir, encadeie `get` usando `{}` como padrão:

```python
>>> print(TOLERANCIAS.get("E", {}).get("espessura"))
None
>>> print(TOLERANCIAS.get("B", {}).get("gramatura"))
None
```

Se a linha `"E"` não existe, o primeiro `get` devolve `{}`, e o segundo `get` num dicionário vazio devolve `None`. Sem erro.

Para percorrer dois níveis, use um `for` dentro de outro: `for linha, propriedades in TOLERANCIAS.items():` e, dentro dele, `for nome, regra in propriedades.items():`. O exemplo `07` mostra isso rodando.

> 💡 **Dica:** isso que você acabou de escrever é praticamente um arquivo **JSON**. Quando, no módulo 06, você salvar as regras num arquivo `regras.json`, e no módulo 12 receber dados de uma API, a estrutura vai ser exatamente esta: dicionários e listas aninhados.

Exemplo completo: `exemplos/07_dicionarios_aninhados.py`.

## 9. Conjuntos: sem repetição, com matemática

Um **conjunto** (`set`) é uma coleção **sem itens repetidos** e **sem ordem**. Ele responde muito rápido à pergunta "isto está aqui?".

```python
>>> lidos = ["L-101", "L-102", "L-101", "L-103", "L-102"]
>>> unicos = set(lidos)
>>> len(unicos)
3
>>> sorted(unicos)
['L-101', 'L-102', 'L-103']
>>> "L-102" in unicos
True
```

> ⚠️ **Erro comum:** `{}` cria um **dicionário** vazio, não um conjunto. Conjunto vazio é `set()`.

A grande vantagem são as operações entre conjuntos. Imagine as OPs que a expedição pediu e as OPs que já têm resultado no laboratório:

```python
>>> pedidas = {"OP-4512", "OP-4513", "OP-4514", "OP-4520"}
>>> com_resultado = {"OP-4512", "OP-4514", "OP-4515"}
>>> sorted(pedidas & com_resultado)
['OP-4512', 'OP-4514']
>>> sorted(pedidas - com_resultado)
['OP-4513', 'OP-4520']
>>> sorted(com_resultado - pedidas)
['OP-4515']
>>> sorted(pedidas | com_resultado)
['OP-4512', 'OP-4513', 'OP-4514', 'OP-4515', 'OP-4520']
```

```text
        pedidas                 com_resultado
     +-------------------+-------------------+
     |  OP-4513          |                   |
     |  OP-4520  +-------+-------+           |
     |           |  OP-4512      |  OP-4515  |
     |           |  OP-4514      |           |
     +-----------+-------+-------+-----------+
       pedidas - com_res    &      com_res - pedidas
```

| Operador | Nome | Pergunta que responde |
|---|---|---|
| `a & b` | interseção | o que está nos dois? |
| `a \| b` | união | o que está em pelo menos um? |
| `a - b` | diferença | o que está em `a` e não em `b`? |
| `a ^ b` | diferença simétrica | o que está em só um dos dois? |

Para modificar: `conjunto.add(x)`, `conjunto.remove(x)` (dá `KeyError` se não existir) e `conjunto.discard(x)` (não reclama).

> 💡 **Dica:** um conjunto não tem ordem garantida. A ordem em que ele aparece no `print` pode mudar de uma execução para outra. Sempre que for **mostrar** um conjunto, use `sorted(...)`.

> 🔮 **Preveja antes de rodar:** o que cada linha imprime?
>
> ```python
> print(len(set("bobina")))
> print(sorted({"A", "b", "a", "B "}))
> ```

<details><summary>Resposta</summary>

```text
5
['A', 'B ', 'a', 'b']
```

- `set("bobina")` guarda as letras sem repetir: `b`, `o`, `i`, `n`, `a`. O segundo `b` não entra. São 5.
- Para o conjunto, `"A"` e `"a"` são diferentes, e `"B "` (com espaço) também é diferente de `"B"`. Nada foi eliminado. E o `sorted` põe maiúsculas antes de minúsculas. Se você queria as linhas A e B, normalize antes: `{x.strip().upper() for x in ...}`.

</details>

Exemplo completo: `exemplos/08_conjuntos.py`.

## 10. Compreensões: montar coleções numa linha

Você vai escrever muito este padrão: "crie uma lista nova a partir de outra, transformando e/ou filtrando".

```python
>>> espessuras_um = [50.2, 44.1, 51.0, 56.3, 49.8]
>>> em_mm = []
>>> for valor in espessuras_um:
...     em_mm.append(round(valor / 1000, 4))
...
>>> em_mm
[0.0502, 0.0441, 0.051, 0.0563, 0.0498]
```

A **compreensão de lista** faz o mesmo numa linha:

```python
>>> [round(valor / 1000, 4) for valor in espessuras_um]
[0.0502, 0.0441, 0.051, 0.0563, 0.0498]
```

Leia assim: "**o que guardar**, para cada item, de onde vem, (se passar no filtro)".

```text
 [ round(v / 1000, 4)   for v in espessuras_um   if v > 45 ]
   \_______________/    \____________________/   \_______/
     o que guardar         de onde vem           filtro
                                                 (opcional)
```

Com filtro:

```python
>>> [valor for valor in espessuras_um if valor < 45 or valor > 55]
[44.1, 56.3]
```

Com expressão condicional (módulo 02) na parte do "o que guardar". Aqui **todos** entram, transformados:

```python
>>> ["ok" if 45 <= valor <= 55 else "fora" for valor in espessuras_um]
['ok', 'fora', 'ok', 'fora', 'ok']
```

> ⚠️ **Erro comum:** confundir os dois `if`. O `if` no **fim** filtra (alguns itens não entram). O `if ... else` no **começo** transforma (todos entram). O `if` do fim não aceita `else`.

### De dicionário e de conjunto

Trocando os colchetes por chaves, você monta dicionários e conjuntos:

```python
>>> ops = ["OP-4512", "OP-4513", "OP-4514"]
>>> pesos = [500.0, 320.5, 210.0]
>>> peso_da_op = {op: peso for op, peso in zip(ops, pesos, strict=True)}
>>> {op: peso for op, peso in peso_da_op.items() if peso > 300}
{'OP-4512': 500.0, 'OP-4513': 320.5}
>>> linhas = {linha.strip().upper() for linha in ["a", "A ", " b", "B", "c"]}
>>> sorted(linhas)
['A', 'B', 'C']
```

### Quando NÃO usar compreensão

- Quando a lógica tem **vários passos** ou mais de uma condição complicada. Um `for` com nomes claros é melhor.
- Quando o objetivo é um **efeito** (como `print`), não montar uma lista. `[print(x) for x in lista]` funciona, mas cria uma lista inútil de `None`. Use `for`.
- Quando ela não cabe numa linha legível. Compreensão é para deixar o código **mais claro**, não mais curto.

> 🔧 **Modifique:** em `exemplos/09_compreensoes.py`, crie a lista `fora_com_posicao` com tuplas (posição, valor) das espessuras fora de 45–55, usando `enumerate(..., start=1)` dentro da compreensão. (É o exercício 06 quase pronto.)

## 11. Funções embutidas que economizam laços

Muitos laços do módulo 02 viram uma chamada de função:

```python
>>> medicoes = [50.2, 49.8, 51.0, 50.5, 48.9]
>>> round(sum(medicoes) / len(medicoes), 2)
50.08
>>> min(medicoes), max(medicoes)
(48.9, 51.0)
>>> any(valor < 49 for valor in medicoes)
True
>>> all(45 <= valor <= 55 for valor in medicoes)
True
```

- `any(...)`: **algum** item satisfaz? (para no primeiro `True`)
- `all(...)`: **todos** satisfazem? (para no primeiro `False`)

O que vai dentro do `any` e do `all` é uma **expressão geradora**: parece uma compreensão sem os colchetes. Ela produz os valores um por um, sem montar uma lista inteira na memória. Também funciona com `sum`: `sum(peso for peso in pesos if peso > 300)`.

> ⚠️ **Erro comum:** `max([])` e `min([])` dão `ValueError`, porque não existe maior item numa lista vazia. Use `max(lista, default=None)` ou confira antes com `if lista:`.

### `sorted`, `min` e `max` com `key`

E se você quer ordenar bobinas pelo **peso**, e não pela OP? O parâmetro `key` recebe uma função que diz **o que comparar** em cada item.

A forma mais curta de escrever essa função é uma **lambda**: `lambda bobina: bobina["peso_kg"]` é uma função de uma linha, sem nome, que recebe `bobina` e devolve `bobina["peso_kg"]`. O módulo 04 explica lambdas a fundo.

```python
>>> bobinas = [
...     {"op": "OP-4513", "peso_kg": 320.5},
...     {"op": "OP-4512", "peso_kg": 500.0},
...     {"op": "OP-4514", "peso_kg": 210.0},
... ]
>>> por_peso = sorted(bobinas, key=lambda bobina: bobina["peso_kg"])
>>> [b["op"] for b in por_peso]
['OP-4514', 'OP-4513', 'OP-4512']
>>> max(bobinas, key=lambda bobina: bobina["peso_kg"])["op"]
'OP-4512'
>>> min([50.2, 49.8, 51.0, 48.9], key=lambda valor: abs(valor - 49.0))
48.9
```

O último exemplo pergunta: "qual medição está **mais perto** de 49.0?". A key transforma cada valor na distância até 49.0; o `min` escolhe a menor distância, mas devolve o **valor original**.

**Exemplo resolvido: ranking com desempate.** Quero as bobinas da maior espessura para a menor; se empatar, pela OP em ordem crescente.

```python
>>> amostras = [("OP-4513", 50.4), ("OP-4512", 51.0), ("OP-4511", 50.4)]
```

Como eu penso:

1. `reverse=True` inverte **tudo**, inclusive o desempate (as OPs sairiam de trás para frente). Não serve.
2. A key pode devolver uma **tupla**. Tuplas comparam o 1º item; se empatar, o 2º.
3. Para a espessura ficar decrescente e a OP crescente, uso o **negativo** da espessura: o maior valor vira o menor número.

```python
>>> sorted(amostras, key=lambda par: (-par[1], par[0]))
[('OP-4512', 51.0), ('OP-4511', 50.4), ('OP-4513', 50.4)]
```

O exercício 09 usa exatamente esse raciocínio com as notas de uma turma.

### Juntando textos de uma lista

Um último método, de string, que você vai querer para montar relatórios: `separador.join(lista_de_textos)` junta os textos colocando o separador entre eles. O módulo 05 aprofunda.

```python
>>> ", ".join(["espessura", "cof"])
'espessura, cof'
```

Exemplo completo: `exemplos/10_funcoes_embutidas.py`.

## 12. Lista de dicionários: sua primeira tabela

Agora vem a ideia que liga este módulo ao resto da sua carreira com dados.

Uma planilha é um monte de **linhas**, e cada linha tem as mesmas **colunas**. Em Python, a forma mais natural de representar isso é uma **lista de dicionários**: cada dicionário é uma linha; as chaves são os nomes das colunas.

```python
>>> amostras = [
...     {"op": "OP-4512", "linha": "A", "espessura": 50.4, "cof": 0.22},
...     {"op": "OP-4513", "linha": "B", "espessura": 20.9, "cof": 0.31},
...     {"op": "OP-4514", "linha": "A", "espessura": 56.1, "cof": 0.25},
...     {"op": "OP-4515", "linha": "C", "espessura": 35.2, "cof": 0.18},
...     {"op": "OP-4516", "linha": "A", "espessura": 49.7, "cof": 0.27},
... ]
```

```text
                 colunas (as chaves) -->
                 "op"       "linha"  "espessura"  "cof"
 amostras[0] --> OP-4512    A        50.4         0.22
 amostras[1] --> OP-4513    B        20.9         0.31
 amostras[2] --> OP-4514    A        56.1         0.25
 amostras[3] --> OP-4515    C        35.2         0.18
 amostras[4] --> OP-4516    A        49.7         0.27
```

Pegar um valor é "linha, depois coluna": `amostras[2]["espessura"]` é `56.1`.

Com o que você já sabe, dá para fazer **tudo** que um analista faz numa tabela. E repare na coluna da direita: é o mesmo raciocínio, com outra sintaxe, que você vai usar no SQL (módulo 11) e no pandas (módulo 10).

| Operação | Python puro (este módulo) | SQL | pandas |
|---|---|---|---|
| Filtrar linhas | `[a for a in amostras if a["linha"] == "A"]` | `WHERE linha = 'A'` | `df[df["linha"] == "A"]` |
| Pegar uma coluna | `[a["espessura"] for a in amostras]` | `SELECT espessura` | `df["espessura"]` |
| Ordenar | `sorted(amostras, key=lambda a: a["espessura"])` | `ORDER BY espessura` | `df.sort_values("espessura")` |
| Agregar | `sum(...) / len(...)` | `AVG(espessura)` | `df["espessura"].mean()` |
| Agrupar | dicionário de listas (seção 7) | `GROUP BY linha` | `df.groupby("linha")` |
| Nova coluna | `{**a, "status": ...}` | `SELECT *, ... AS status` | `df["status"] = ...` |
| Juntar tabelas | índice com dicionário | `JOIN` | `pd.merge(...)` |

### Filtrar e escolher colunas

```python
>>> linha_a = [a for a in amostras if a["linha"] == "A"]
>>> [a["op"] for a in linha_a]
['OP-4512', 'OP-4514', 'OP-4516']
>>> [a["espessura"] for a in amostras]
[50.4, 20.9, 56.1, 35.2, 49.7]
>>> [(a["op"], a["cof"]) for a in amostras if a["cof"] > 0.30]
[('OP-4513', 0.31)]
```

### Ordenar e mostrar como tabela

```python
>>> ordenadas = sorted(amostras, key=lambda a: a["espessura"], reverse=True)
>>> for a in ordenadas[:3]:
...     print(f"{a['op']:<9}{a['linha']:<3}{a['espessura']:>6.1f}")
...
OP-4514  A    56.1
OP-4512  A    50.4
OP-4516  A    49.7
```

Na f-string, `:<9` alinha à esquerda ocupando 9 caracteres e `:>6.1f` alinha à direita em 6 caracteres com 1 casa decimal. É o que deixa as colunas retinhas.

### Exemplo resolvido: média de espessura por linha (GROUP BY)

Problema: "qual a espessura média de cada linha de produção?"

Como eu penso, passo a passo:

1. **Que forma tem a resposta?** "Para cada linha, um número" → um dicionário `{"A": ..., "B": ...}`.
2. **Dá para fazer em um passo só?** Não fácil. Divido em dois: primeiro **agrupo** as espessuras de cada linha; depois **calculo** a média de cada grupo.
3. **Passo 1, agrupar:** é o padrão de agrupamento da seção 7.
4. **Passo 2, resumir:** uma compreensão de dicionário que transforma cada lista em média.
5. **Testo** com os dados que tenho e confiro uma conta de cabeça: linha A tem 50.4, 56.1 e 49.7; média ≈ 52.07.

```python
>>> grupos = {}
>>> for a in amostras:
...     grupos.setdefault(a["linha"], []).append(a["espessura"])
...
>>> grupos
{'A': [50.4, 56.1, 49.7], 'B': [20.9], 'C': [35.2]}
>>> {linha: round(sum(v) / len(v), 2) for linha, v in grupos.items()}
{'A': 52.07, 'B': 20.9, 'C': 35.2}
```

Confere com a conta de cabeça. Esse "agrupar, depois resumir" é exatamente o que o `GROUP BY` do SQL e o `groupby` do pandas fazem por baixo. O exercício 11 pede a versão completa (quantidade, média, mínimo e máximo, ignorando células vazias).

> 🔧 **Modifique:** mude o código para calcular a média do **COF** por linha. Depois, para contar **quantas amostras** cada linha tem.

### Nova coluna sem estragar a tabela original

Para acrescentar uma coluna `status`, crie dicionários **novos**. `{**a, "status": ...}` copia todas as chaves de `a` e acrescenta (ou substitui) `status`:

```python
>>> com_status = [
...     {**a, "status": "ok" if a["cof"] <= 0.30 else "COF alto"} for a in amostras
... ]
>>> [(a["op"], a["status"]) for a in com_status][:2]
[('OP-4512', 'ok'), ('OP-4513', 'COF alto')]
>>> "status" in amostras[0]
False
```

Se você fizesse `a["status"] = ...` dentro de um `for`, estaria alterando a tabela original (seção 4). Às vezes é isso que você quer; na dúvida, crie uma nova.

### Exemplo resolvido: juntar duas tabelas (JOIN)

A expedição mandou os pedidos; o laboratório tem os resultados. Quero, para cada pedido, a linha e o COF da amostra.

```python
>>> pedidos = [
...     {"op": "OP-4514", "nf": "000123", "peso_kg": 500.0},
...     {"op": "OP-4599", "nf": "000124", "peso_kg": 80.5},
... ]
```

Como eu penso:

1. Primeira ideia: para cada pedido, percorrer **todas** as amostras procurando a OP. Funciona, mas é um laço dentro de outro. Com 1.000 pedidos e 1.000 amostras, são 1.000.000 comparações.
2. Ideia melhor: montar **uma vez** um dicionário `OP → amostra` (um "PROCV pronto") e depois só consultar com `get`. Cada consulta é instantânea.
3. Pedido sem amostra? `get` devolve `None`, e eu trato esse caso.

```python
>>> indice = {a["op"]: a for a in amostras}
>>> for pedido in pedidos:
...     amostra = indice.get(pedido["op"])
...     if amostra is None:
...         print(pedido["op"], "-> sem resultado no laboratório")
...     else:
...         print(pedido["op"], "-> linha", amostra["linha"], "| COF", amostra["cof"])
...
OP-4514 -> linha A | COF 0.25
OP-4599 -> sem resultado no laboratório
```

Isso é um **LEFT JOIN**: todos os pedidos aparecem, com ou sem resultado. O exercício 13 pede a versão completa, com OPs digitadas de jeitos diferentes.

### Linhas ou colunas?

Existe outro formato para a mesma tabela: um **dicionário de listas**, uma lista por coluna, como `colunas = {"op": ["OP-4512", "OP-4513"], "espessura": [50.4, 20.9]}`. O pandas aceita os dois formatos: `pd.DataFrame(amostras)` e `pd.DataFrame(colunas)` geram a mesma tabela. Lista de dicionários é mais natural para **ler e processar linha a linha** (é o que o `csv.DictReader` do módulo 06 entrega). Dicionário de listas é mais natural para **cálculos por coluna**.

Exemplo completo: `exemplos/11_tabela_lista_de_dicts.py`.

## 13. Qual coleção usar?

| | Lista `[]` | Tupla `()` | Dicionário `{k: v}` | Conjunto `{}` / `set()` |
|---|---|---|---|---|
| Tem ordem? | sim | sim | sim (de inserção) | não |
| Pode mudar? | sim | não | sim | sim |
| Aceita repetidos? | sim | sim | chaves não | não |
| Você acessa por... | posição | posição | chave | só pergunta "está aqui?" |
| Use para... | sequência de itens do mesmo tipo | registro fixo, vários retornos | buscar por nome, contar, agrupar | tirar repetidos, cruzar grupos |
| Exemplo | medições de uma bobina | `(mínimo, máximo)` | peso de cada OP | OPs pedidas |

Na dúvida, faça a pergunta que você vai fazer aos dados:

- "Qual é o 3º?" → lista.
- "Qual é o valor de X?" → dicionário.
- "X está aqui? O que tem em A e não tem em B?" → conjunto.
- "Estes valores andam sempre juntos e não mudam?" → tupla.

## Lendo mensagens de erro deste módulo

Um traceback se lê **de baixo para cima**: a última linha diz **o que** deu errado; as de cima dizem **onde**. Desde o Python 3.11, os `~~~^^^` apontam o pedaço exato da linha.

**1. `KeyError`: chave que não existe.**

```text
Traceback (most recent call last):
  File "C:\curso-python\conferencia.py", line 5, in <module>
    minimo, maximo = tolerancias[amostra["linha"]]
                     ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
KeyError: 'E'
```

Leitura: na linha 5, o dicionário `tolerancias` não tem a chave `'E'`. Pergunte-se: a chave deveria existir (então o dado está errado ou o dicionário está incompleto) ou faltar é normal (então use `get` e trate o `None`)? Repare também se não é diferença de maiúscula ou espaço (`"e"`, `"E "`).

**2. `TypeError: 'NoneType' object is not subscriptable`.**

```text
Traceback (most recent call last):
  File "C:\curso-python\medias.py", line 3, in <module>
    print(medicoes[0])
          ~~~~~~~~^^^
TypeError: 'NoneType' object is not subscriptable
```

Leitura: `medicoes` vale `None`, e `None` não tem índice. Quase sempre é um `medicoes = medicoes.sort()` (ou `.append`, `.reverse`) mais acima. Procure a linha que **atribuiu** a variável, não a linha do erro.

**Outros que você vai encontrar:**

| Mensagem | Causa provável | Correção |
|---|---|---|
| `IndexError: list index out of range` | índice passou do último (`len(lista) - 1`), comum em `for i in range(...)` | percorra os itens direto, ou use `enumerate` |
| `AttributeError: 'NoneType' object has no attribute 'append'` | a variável recebeu o `None` de um método como `sort()` | não atribua o resultado de métodos que modificam no lugar |
| `TypeError: unhashable type: 'list'` | lista usada como chave de dicionário ou item de conjunto | use uma tupla |
| `TypeError: 'tuple' object does not support item assignment` | tentou mudar uma tupla | crie uma tupla nova, ou use lista |
| `ValueError: list.remove(x): x not in list` | `remove` de valor que não está na lista | confira com `in` antes |
| `ValueError: too many values to unpack (expected 2)` | mais itens do que variáveis no desempacotamento | confira o formato do dado (ou use `*resto`) |
| `ValueError: max() iterable argument is empty` | `max`/`min` de lista vazia | `max(lista, default=None)` |
| `RuntimeError: dictionary changed size during iteration` | acrescentou/removeu chaves dentro de um `for` sobre o dicionário | percorra `list(dic)` ou monte um dicionário novo |
| `TypeError: '<' not supported between instances of 'str' and 'float'` | `sort`/`sorted`/`max` numa lista com textos e números misturados | converta tudo para o mesmo tipo antes |
| `TypeError: 'list' object is not callable` | você criou uma variável chamada `list` (ou `dict`, `sum`...) e depois tentou usar a função | renomeie a variável |

> 💡 **Dica:** as mensagens podem mudar um pouco entre versões do Python. O tipo do erro (a palavra antes dos dois-pontos) não muda, e é por ele que você começa.

## Boas práticas

- **Nomes no plural para coleções, singular para o item:** `for medicao in medicoes`, `for amostra in amostras`. O código se lê como português.
- **Nunca remova itens da lista que você está percorrendo.** Monte uma lista nova com o que fica.
- **Não altere a coleção que você recebeu**, a não ser que esse seja o objetivo declarado. Devolva uma nova.
- **`dic[chave]` quando faltar é bug; `dic.get(chave)` quando faltar é normal.**
- **Normalize textos antes de usar como chave** (`.strip().upper()`): `"a "` e `"A"` são chaves diferentes.
- **Use `zip(..., strict=True)`** para não perder dados em silêncio.
- **Compreensões curtas.** Se não cabe numa linha legível, vire um `for`.
- **Mantenha as "linhas" da tabela com as mesmas chaves.** Se uma coluna pode faltar, decida o padrão (`None`) e use `get`.
- **Não use nomes de funções embutidas como variável:** `list`, `dict`, `set`, `sum`, `max`, `min`, `id`, `type`. O Python deixa, e depois a função "some".

## No mundo real

Fim de turno. A planilha do dia tem as amostras das linhas A a D. A expedição mandou por e-mail as OPs que saem amanhã. Você precisa: conferir cada amostra contra as tolerâncias da linha, respeitar a observação "COF: liberado" e montar a lista de certificados a emitir.

O script `exemplos/12_mundo_real_conferencia.py` faz isso só com o que você aprendeu neste módulo. No começo do arquivo ficam os dados:

- `TOLERANCIAS`: dicionário aninhado. Para cada linha (A a D), cada propriedade tem uma tupla: `(nominal, %)` para espessura e gramatura, `(mín, máx)` para COF. Exemplo: `"A": {"espessura": (50.0, 10.0), "gramatura": (46.0, 5.0), "cof": (0.15, 0.30)}`.
- `PERCENTUAIS = {"espessura", "gramatura"}`: o conjunto das propriedades que usam nominal ± %.
- `AMOSTRAS`: a planilha do dia como lista de dicionários, montada com `dict(zip(COLUNAS, linha, strict=True))` a partir de tuplas, como se viesse de um CSV. Cada amostra tem `op`, `linha`, `espessura`, `gramatura`, `cof` e `obs` (a observação, que às vezes diz "COF: liberado").
- `OPS_PEDIDAS`: as OPs do e-mail da expedição, com uma repetida.

O miolo do programa:

```python
def faixa(propriedade, regra):
    """Converte a regra em (mínimo, máximo)."""
    if propriedade in PERCENTUAIS:
        nominal, pct = regra
        return round(nominal * (1 - pct / 100), 2), round(nominal * (1 + pct / 100), 2)
    return regra  # já é (mínimo, máximo)


def conferir(amostra):
    """Devolve uma cópia da amostra com as colunas 'falhas' e 'status'."""
    regras = TOLERANCIAS[amostra["linha"]]
    falhas = []
    for propriedade, regra in regras.items():
        minimo, maximo = faixa(propriedade, regra)
        if not minimo <= amostra[propriedade] <= maximo:
            falhas.append(propriedade)

    if not falhas:
        status = "APROVADA"
    elif falhas == ["cof"] and "cof: liberado" in amostra["obs"].lower():
        status = "LIBERADA"  # COF fora, mas liberado pela qualidade
    else:
        status = "REPROVADA"
    return {**amostra, "falhas": falhas, "status": status}


conferidas = [conferir(amostra) for amostra in AMOSTRAS]

print("== Conferência do dia ==")
for c in conferidas:
    detalhe = ", ".join(c["falhas"]) if c["falhas"] else "-"
    print(f"{c['op']}  linha {c['linha']}  {c['status']:<9}  fora: {detalhe}")

print("\n== Resumo por linha ==")
for linha in sorted(TOLERANCIAS):
    da_linha = [c for c in conferidas if c["linha"] == linha]
    ok = sum(c["status"] != "REPROVADA" for c in da_linha)
    print(f"Linha {linha}: {ok}/{len(da_linha)} amostras liberadas")

liberadas = {c["op"] for c in conferidas if c["status"] != "REPROVADA"}
reprovadas = {c["op"] for c in conferidas if c["status"] == "REPROVADA"}
pedidas = set(OPS_PEDIDAS)
com_resultado = liberadas | reprovadas

print("\n== Expedição ==")
print("Emitir certificado:", sorted(pedidas & liberadas))
print("Bloqueadas:        ", sorted(pedidas & reprovadas))
print("Sem resultado:     ", sorted(pedidas - com_resultado))
```

Saída:

```text
== Conferência do dia ==
OP-4512  linha A  APROVADA   fora: -
OP-4513  linha B  REPROVADA  fora: espessura
OP-4514  linha A  LIBERADA   fora: cof
OP-4515  linha C  APROVADA   fora: -
OP-4516  linha D  REPROVADA  fora: espessura, gramatura
OP-4517  linha D  APROVADA   fora: -

== Resumo por linha ==
Linha A: 2/2 amostras liberadas
Linha B: 0/1 amostras liberadas
Linha C: 1/1 amostras liberadas
Linha D: 1/2 amostras liberadas

== Expedição ==
Emitir certificado: ['OP-4512', 'OP-4514']
Bloqueadas:         ['OP-4516']
Sem resultado:      ['OP-4520']
```

Repare no que cada coleção está fazendo:

- **dicionário aninhado** para as regras (busca pela linha, depois pela propriedade);
- **tuplas** para registros fixos (`(nominal, %)`, `(mín, máx)`, as linhas da planilha);
- **lista de dicionários** para a tabela de amostras, e uma **nova** tabela com as colunas `falhas` e `status`;
- **conjuntos** para cruzar o que a expedição pediu com o que o laboratório liberou.

Nos próximos módulos, isso cresce: as funções ficam melhores (04), a observação vira texto analisado com regex (05), os dados vêm de arquivos de verdade (06 e 10) e as regras vão para um banco (11). A lógica, você já tem.

## Resumo

| Quero... | Sintaxe |
|---|---|
| criar uma lista | `medicoes = [50.2, 49.8]` |
| primeiro / último item | `lista[0]` / `lista[-1]` |
| trecho | `lista[ini:fim]` (fim não entra), `lista[-3:]`, `lista[::-1]` |
| acrescentar / inserir | `lista.append(x)` / `lista.insert(i, x)` |
| remover por valor / por posição | `lista.remove(x)` / `lista.pop(i)` |
| ordenar no lugar / ordenada nova | `lista.sort()` / `sorted(lista)` |
| copiar (rasa / profunda) | `lista.copy()` ou `lista[:]` / `copy.deepcopy(obj)` |
| mesmo objeto? mesmo conteúdo? | `a is b` / `a == b` |
| tupla e desempacotamento | `t = ("OP-1", 500.0)`; `op, peso = t`; `a, *resto = lista` |
| posição + valor | `for i, v in enumerate(lista, start=1)` |
| andar em várias listas | `for a, b in zip(lista1, lista2, strict=True)` |
| criar dicionário | `d = {"OP-1": 500.0}`; `dict(zip(chaves, valores, strict=True))` |
| ler com segurança | `d.get(chave)`, `d.get(chave, padrao)` |
| percorrer dicionário | `for chave, valor in d.items()` |
| contar | `d[k] = d.get(k, 0) + 1` |
| agrupar | `d.setdefault(k, []).append(v)` |
| juntar dicionários | `padrao \| especifico` |
| conjunto | `set(lista)`; `a & b`, `a \| b`, `a - b`; vazio: `set()` |
| compreensões | `[x for x in xs if ...]`, `{k: v for ...}`, `{x for ...}` |
| agregar | `sum`, `min`, `max`, `len`, `any`, `all` |
| ordenar por critério | `sorted(xs, key=lambda x: x["peso"], reverse=True)` |
| filtrar tabela | `[r for r in tabela if r["linha"] == "A"]` |
| juntar tabelas | `indice = {r["op"]: r for r in tabela}`; `indice.get(op)` |

## Você domina este módulo se...

- [ ] Consigo explicar, desenhando etiquetas e caixas, por que `b = a` seguido de `b.append(1)` muda `a`, e como evitar isso.
- [ ] Sei a diferença entre cópia rasa e profunda e consigo dar um exemplo em que a rasa não basta.
- [ ] Prevejo sem rodar o resultado de `lista[-3:]`, `lista[::-1]` e `lista[-0:]`.
- [ ] Escolho entre lista, tupla, dicionário e conjunto justificando pela pergunta que vou fazer aos dados.
- [ ] Escrevo de memória os padrões de contagem e de agrupamento com dicionário.
- [ ] Transformo um `for` com `append` numa compreensão (e sei quando não vale a pena).
- [ ] Filtro, ordeno, agrupo e junto uma lista de dicionários, e sei o nome dessas operações em SQL.
- [ ] Leio um `KeyError` ou um `'NoneType' object is not subscriptable` e sei onde procurar a causa.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_ultimas_medicoes` | ★☆☆ | fatiamento, índice negativo, caso `n = 0` |
| 02 | `ex02_resumo_espessura` | ★☆☆ | `sum`, `min`, `max`, `len`, montar dicionário |
| 03 | `ex03_dentro_da_tolerancia` | ★☆☆ | `dict.get`, desempacotar tupla, normalizar chave |
| 04 | `ex04_contar_votos` | ★☆☆ | padrão de contagem, `max` com `key` |
| 05 | `ex05_remover_duplicadas` | ★☆☆ | conjunto como "já vi", manter a ordem |
| 06 | `ex06_fora_da_faixa` | ★★☆ | `enumerate`, compreensão com filtro, percentual |
| 07 | `ex07_pesos_por_op` | ★★☆ | `zip`, acumular em dicionário, validar tamanhos |
| 08 | `ex08_leitura_copia_referencia` | ★★☆ | **leitura de código:** prever saídas e consertar um bug de referência |
| 09 | `ex09_ranking_alunos` | ★★☆ | `sorted` com `key` de tupla, desempate |
| 10 | `ex10_conferir_ops` | ★★☆ | operações de conjunto |
| 11 | `ex11_resumo_por_linha` | ★★★ | lista de dicionários, agrupar e resumir (GROUP BY) |
| 12 | `ex12_revisao_tolerancias` | ★★★ | **revisão** 01+02+03: dicionário aninhado, f-strings, laços |
| 13 | `ex13_revisao_juntar_tabelas` | ★★★ | **revisão** 01+02+03: JOIN com índice, normalizar textos |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de `raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 03 ex01
```

Para testar o módulo todo: `python curso.py testar 03`. Para ver seu progresso: `python curso.py progresso`.

> 💡 **Dica:** antes de olhar a solução (`solucoes/`), rode os exemplos do enunciado no REPL e leia a mensagem do teste que falhou. Ela diz o que era esperado e o que seu código devolveu.

## Desafio do módulo

**Painel de conferência do lote.** Você recebe a "planilha" do dia (lista de dicionários), as tolerâncias por linha (dicionário aninhado) e as OPs pedidas pela expedição. Seu programa imprime a tabela conferida, o resumo por linha, as maiores não conformidades e a fila de certificados.

Enunciado completo, requisitos e critérios de aceite: [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md) (15 perguntas, gabarito no final).

## Para ir além

- Tutorial oficial, estruturas de dados: [docs.python.org/pt-br/3/tutorial/datastructures.html](https://docs.python.org/pt-br/3/tutorial/datastructures.html)
- Tipos embutidos (listas, tuplas, dicionários, conjuntos): [docs.python.org/pt-br/3/library/stdtypes.html](https://docs.python.org/pt-br/3/library/stdtypes.html)
- Ordenação, com `key` e desempates: [docs.python.org/pt-br/3/howto/sorting.html](https://docs.python.org/pt-br/3/howto/sorting.html)
- Módulo `copy` (cópia rasa e profunda): [docs.python.org/pt-br/3/library/copy.html](https://docs.python.org/pt-br/3/library/copy.html)
- Leitura extra: *Facts and myths about Python names and values*, de Ned Batchelder (em inglês, a melhor explicação de "etiquetas"): [nedbatchelder.com/text/names.html](https://nedbatchelder.com/text/names.html)
- Ferramenta: [pythontutor.com](https://pythontutor.com) desenha as setas de referência enquanto o código roda. Use sempre que a seção 4 parecer mágica.
