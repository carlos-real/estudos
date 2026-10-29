# Módulo 04 — Funções: organize, reutilize e decomponha problemas

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 03 · **Nível:** iniciante

## O que você vai aprender

- Escrever funções com `def`, parâmetros e `return`, e explicar a diferença entre **devolver** e **mostrar** um valor.
- Chamar funções com argumentos posicionais e nomeados, e definir valores padrão.
- Reconhecer e corrigir a armadilha do **valor padrão mutável**.
- Devolver vários valores de uma vez e usar **retorno antecipado** para acabar com `if` dentro de `if`.
- Prever o valor de uma variável sabendo onde ela vive (escopo local e global).
- Documentar funções com docstring e type hints.
- Receber quantos argumentos vierem com `*args` e `**kwargs`.
- Passar funções como argumento, guardá-las em dicionários e criar funções dentro de funções.
- Usar `lambda` com `key=`.
- Separar **funções puras** de **efeitos colaterais**.
- **Decompor** um problema grande em funções pequenas, testáveis e fáceis de ler.
- Escrever uma função recursiva simples, com caso base, e saber quando preferir um laço.

## Por que isso importa

Até agora seus programas eram uma lista de comandos de cima para baixo. Funciona para 30 linhas. Com 300 linhas, vira um labirinto: a mesma conta de tolerância aparece em cinco lugares, uma correção num lugar esquece os outros, e ninguém (nem você, daqui a um mês) entende o que o código faz.

Funções resolvem isso. Elas deixam você:

- **dar nome a uma ideia** (`calcular_limites`, `conferir_amostra`) e usar o nome no lugar dos detalhes;
- **escrever uma vez e usar em vários lugares**;
- **testar cada pedaço sozinho**, que é exatamente o que o `python curso.py testar` faz com os seus exercícios.

No mercado, "saber programar" é em grande parte saber **quebrar um problema em funções bem nomeadas**. É o que um entrevistador observa num teste técnico, e é o que separa um script que só o autor entende de um sistema que uma equipe mantém. O seu projeto final (ler a planilha, conferir tolerâncias, ler e-mails, gerar certificados) só fica de pé se cada parte for uma função pequena que você consegue testar.

## 1. Funções: dar nome a uma ideia

Você já escreveu funções no "molde" dos exercícios. Agora vamos entender cada peça.

Imagine a conta de limites de tolerância repetida em três lugares do seu script:

```python
minimo_a = round(50.0 * (1 - 10.0 / 100), 2)
maximo_a = round(50.0 * (1 + 10.0 / 100), 2)
minimo_b = round(20.0 * (1 - 8.0 / 100), 2)
maximo_b = round(20.0 * (1 + 8.0 / 100), 2)
# ... e de novo para a gramatura, para a linha C ...
```

Se a regra mudar (arredondar em 1 casa, por exemplo), você precisa caçar todas as cópias. Com uma função, a regra mora num lugar só:

```python
>>> def calcular_limites(nominal, tol_pct):
...     """Devolve (mínimo, máximo) para nominal ± tol_pct %."""
...     fator = tol_pct / 100
...     return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)
...
>>> calcular_limites(50.0, 10.0)
(45.0, 55.0)
>>> calcular_limites(20.0, 8.0)
(18.4, 21.6)
```

### Anatomia

```text
 def calcular_limites(nominal, tol_pct):          <- cabeçalho
 |   |                \______ ______/
 |   |                       v
 |   nome (verbo, snake_case) parâmetros: as "entradas"
 palavra-chave

     """Devolve (mínimo, máximo) ..."""           <- docstring (o manual)
     fator = tol_pct / 100                        <- corpo (indentado)
     return round(...), round(...)                <- return: a "saída"
```

E o que acontece quando você **chama** a função:

```text
 limites = calcular_limites(50.0, 10.0)
                 |
                 |  1. o Python pula para dentro da função
                 v     com nominal = 50.0 e tol_pct = 10.0
         fator = 0.1
         return (45.0, 55.0)
                 |
                 |  2. volta para onde foi chamada,
                 v     trazendo o valor do return
 limites = (45.0, 55.0)
```

O `def` só **cria** a função; nada roda nessa hora. O corpo só executa quando alguém **chama**: `calcular_limites(50.0, 10.0)`.

### Devolver não é mostrar

Esta é a confusão número 1 de quem começa.

- `print` **mostra** um valor na tela. Quem chamou a função não recebe nada.
- `return` **devolve** o valor para quem chamou, que pode guardar, somar, comparar, passar adiante.

> 🔮 **Preveja antes de rodar:** o que aparece na tela?
>
> ```python
> def media_mostrando(valores):
>     print(sum(valores) / len(valores))
>
> resultado = media_mostrando([50.0, 52.0])
> print(resultado)
> ```

<details><summary>Resposta</summary>

```text
51.0
None
```

A primeira linha vem do `print` **dentro** da função. A segunda mostra o que a função **devolveu**: como não há `return`, ela devolve `None`. Toda função sem `return` (ou com `return` sozinho) devolve `None`.

Se você tentasse `resultado * 2`, teria `TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'`. Regra prática: **funções de cálculo devolvem; só a parte do programa que conversa com o usuário imprime** (seção 10).

</details>

O exemplo completo está em `exemplos/01_def_e_return.py`. No PowerShell, na pasta `04-funcoes`:

```text
python exemplos\01_def_e_return.py
```

(No Linux/macOS: `python3 exemplos/01_def_e_return.py`.)

**Tente você:** escreva `peso_liquido(peso_bruto, tara)` que devolve o peso bruto menos a tara, arredondado em 1 casa.

<details><summary>Resposta</summary>

```python
>>> def peso_liquido(peso_bruto, tara):
...     return round(peso_bruto - tara, 1)
...
>>> peso_liquido(1265.3, 14.8)
1250.5
```

</details>

## 2. Parâmetros e argumentos

Dois nomes que você vai ver na documentação:

- **parâmetro** é o nome na definição (`nominal`, `tol_pct`);
- **argumento** é o valor que você passa na chamada (`50.0`, `10.0`).

Você pode passar argumentos de dois jeitos:

```python
>>> calcular_limites(46.0, 5.0)
(43.7, 48.3)
>>> calcular_limites(nominal=46.0, tol_pct=5.0)
(43.7, 48.3)
>>> calcular_limites(tol_pct=5.0, nominal=46.0)
(43.7, 48.3)
>>> calcular_limites(46.0, tol_pct=5.0)
(43.7, 48.3)
```

- **Posicionais:** casam pela ordem. Curtos, mas você precisa lembrar a ordem.
- **Nomeados:** casam pelo nome, em qualquer ordem. Mais legíveis, principalmente com números soltos: `calcular_limites(46.0, 5.0)` obriga o leitor a abrir a função; `calcular_limites(46.0, tol_pct=5.0)` não.
- Pode misturar, mas **posicionais primeiro**.

Os erros de chamada mais comuns, com a mensagem que o Python mostra:

```python
>>> calcular_limites(46.0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: calcular_limites() missing 1 required positional argument: 'tol_pct'
>>> calcular_limites(46.0, 5.0, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: calcular_limites() takes 2 positional arguments but 3 were given
>>> calcular_limites(46.0, tolerancia=5.0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: calcular_limites() got an unexpected keyword argument 'tolerancia'
```

Leia a mensagem: ela diz **qual função**, **qual parâmetro** e **o que estava errado** (faltou, sobrou, nome desconhecido).

## 3. Valores padrão (e a armadilha do padrão mutável)

Um parâmetro pode ter um **valor padrão**, usado quando o argumento não é passado:

```python
>>> def formatar_medida(valor, unidade="µm", casas=1):
...     return f"{valor:.{casas}f} {unidade}"
...
>>> formatar_medida(50.24)
'50.2 µm'
>>> formatar_medida(46, "g/m²")
'46.0 g/m²'
>>> formatar_medida(0.2234, unidade="(COF)", casas=3)
'0.223 (COF)'
```

Repare no `{valor:.{casas}f}`: dá para colocar uma variável **dentro** da especificação de formato. O Python troca `{casas}` pelo número (3) e depois aplica `.3f`. O exercício 02 usa isso.

Regras:

- Parâmetros **com** padrão vêm **depois** dos sem padrão. `def f(a=1, b)` dá `SyntaxError: parameter without a default follows parameter with a default`.
- Use padrão para o **caso comum**. Quem precisa do caso especial passa o argumento, de preferência nomeado.

### Argumentos só por nome

Um `*` sozinho na lista de parâmetros diz: "daqui para frente, só por nome".

```python
>>> def formatar(valor, *, casas=1, unidade="µm"):
...     return f"{valor:.{casas}f} {unidade}"
...
>>> formatar(0.2234, casas=3, unidade="")
'0.223 '
>>> formatar(0.2234, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: formatar() takes 1 positional argument but 2 were given
```

Isso evita chamadas misteriosas como `formatar(0.2234, 3, "")`. Bibliotecas profissionais (pandas, por exemplo) usam muito.

### A armadilha do padrão mutável

> 🔮 **Preveja antes de rodar:** o que as duas chamadas devolvem?
>
> ```python
> def registrar(defeito, defeitos=[]):
>     defeitos.append(defeito)
>     return defeitos
>
> print(registrar("bolha"))
> print(registrar("risco"))
> ```

<details><summary>Resposta</summary>

```text
['bolha']
['bolha', 'risco']
```

A segunda chamada "lembrou" da primeira. Ninguém passou a lista, então as duas usaram o padrão. E o padrão é **a mesma lista**, criada uma vez só.

</details>

Por quê? O valor padrão é criado **quando o `def` roda**, uma única vez, e fica guardado dentro da função. Toda chamada sem o argumento usa **esse mesmo objeto**. Com números e strings (imutáveis) não há problema. Com uma lista (mutável), o `append` modifica o objeto guardado, e a próxima chamada já o encontra modificado.

```text
 Quando o def roda (UMA vez):
     registrar  ---- padrão de "defeitos" ---->  [ ]

 registrar("bolha"):   defeitos --+
                                  +-->  ["bolha"]           (a mesma lista)
 registrar("risco"):   defeitos --+
                                  +-->  ["bolha", "risco"]  (ainda a mesma!)
```

Não precisa acreditar em mim. Teste a hipótese no REPL: a função guarda os padrões em `__defaults__`.

```python
>>> def registrar(defeito, defeitos=[]):
...     defeitos.append(defeito)
...     return defeitos
...
>>> registrar.__defaults__
([],)
>>> registrar("bolha")
['bolha']
>>> registrar.__defaults__
(['bolha'],)
```

Ali está: a lista padrão mudou dentro da própria função.

**A correção** é um idioma que você vai ver em todo código Python profissional: use `None` como padrão e crie a lista **dentro** da função.

```python
>>> def registrar(defeito, defeitos=None):
...     if defeitos is None:
...         defeitos = []
...     defeitos.append(defeito)
...     return defeitos
...
>>> registrar("bolha")
['bolha']
>>> registrar("risco")
['risco']
```

Vale para qualquer padrão mutável: lista (`[]`), dicionário (`{}`), conjunto (`set()`). O ruff, que você vai usar no módulo 09, aponta esse erro sozinho (regra B006).

> ⚠️ **Erro comum:** escrever `if not defeitos:` em vez de `if defeitos is None:`. Uma lista vazia que o chamador passou **de propósito** também é falsy, e seria trocada por outra. Use `is None`.

Exemplos completos: `exemplos/02_parametros.py` e `exemplos/03_padrao_mutavel.py`.

## 4. Vários retornos e retorno antecipado

### Devolvendo mais de um valor

Uma função devolve **um** objeto. Mas esse objeto pode ser uma tupla, e o desempacotamento do módulo 03 faz o resto:

```python
>>> def dividir_em_bobinas(peso_total_kg, peso_bobina_kg):
...     bobinas = int(peso_total_kg // peso_bobina_kg)
...     sobra = round(peso_total_kg % peso_bobina_kg, 2)
...     return bobinas, sobra
...
>>> dividir_em_bobinas(1250.5, 300)
(4, 50.5)
>>> bobinas, sobra = dividir_em_bobinas(1250.5, 300)
>>> sobra
50.5
```

Prefira tupla quando são **2 ou 3 valores** com ordem óbvia. Mais do que isso, devolva um dicionário (`{"bobinas": 4, "sobra": 50.5}`): ninguém precisa lembrar qual posição é o quê.

### Retorno antecipado (guard clauses)

`return` encerra a função **na hora**. Isso permite tratar os casos especiais logo no começo e sair, deixando o caminho principal limpo.

**Exemplo resolvido: a "flecha" de ifs.** Um colega escreveu:

```python
def status_amostra(amostra, tolerancias):
    if amostra is not None:
        if amostra["linha"] in tolerancias:
            if amostra["espessura"] is not None:
                minimo, maximo = tolerancias[amostra["linha"]]
                if minimo <= amostra["espessura"] <= maximo:
                    return "aprovada"
                else:
                    return "reprovada"
            else:
                return "sem medição"
        else:
            return "linha sem tolerância"
    else:
        return "sem amostra"
```

O código anda para a direita como uma flecha, e o `else` de cada caso fica longe do `if` dele. Como eu penso para arrumar:

1. **Quais são os casos que impedem o trabalho?** Sem amostra, linha sem tolerância, sem medição.
2. **Trato cada um logo no começo, com `return`.** Se passou por eles, os dados são válidos.
3. **O caminho feliz fica por último**, sem indentação extra.

```python
>>> def status_amostra(amostra, tolerancias):
...     if amostra is None:
...         return "sem amostra"
...     if amostra["linha"] not in tolerancias:
...         return "linha sem tolerância"
...     if amostra["espessura"] is None:
...         return "sem medição"
...     minimo, maximo = tolerancias[amostra["linha"]]
...     if minimo <= amostra["espessura"] <= maximo:
...         return "aprovada"
...     return "reprovada"
...
>>> TOL = {"A": (45.0, 55.0)}
>>> status_amostra({"linha": "A", "espessura": 50.2}, TOL)
'aprovada'
>>> status_amostra({"linha": "E", "espessura": 50.2}, TOL)
'linha sem tolerância'
>>> status_amostra(None, TOL)
'sem amostra'
```

Mesmo comportamento, metade da indentação, e cada regra numa linha. Repare que **a ordem dos `if` é a regra de negócio**: o exercício 03 cobra exatamente isso ("falta vence tudo").

> 🔧 **Modifique:** acrescente a regra "espessura negativa → `'medição inválida'`" na versão nova. Onde ela entra? Agora tente acrescentar a mesma regra na versão "flecha" e compare o esforço.

## 5. Escopo: onde cada nome vive

Cada chamada de função ganha um "rascunho" próprio. Os nomes criados lá dentro (parâmetros e variáveis) são **locais**: nascem na chamada e somem quando ela termina.

```python
>>> def conferir(valor):
...     resultado_local = 45 <= valor <= 55
...     return resultado_local
...
>>> conferir(50)
True
>>> resultado_local
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'resultado_local' is not defined
```

Para achar um nome, o Python procura de dentro para fora:

```text
 +-- embutidos (built-in): print, len, sum, ... ------------------+
 |  +-- global: nomes criados no arquivo, fora de funções ------+ |
 |  |  +-- função de fora (se houver uma função dentro de outra)| |
 |  |  |  +-- local: parâmetros e variáveis desta chamada --+   | |
 |  |  |  |  o Python procura AQUI primeiro, depois sobe     |   | |
 |  |  |  +--------------------------------------------------+   | |
 |  |  +--------------------------------------------------------+ |
 |  +-------------------------------------------------------------+ |
 +------------------------------------------------------------------+
```

Uma função pode **ler** uma variável global. Mas **atribuir** a um nome dentro da função cria uma variável **local** com esse nome.

> 🔮 **Preveja antes de rodar:** o que o último `print` mostra?
>
> ```python
> total = 0
>
> def somar(valor):
>     total = valor + 1
>     return total
>
> somar(10)
> print(total)
> ```

<details><summary>Resposta</summary>

`0`. O `total = valor + 1` criou um `total` **local**, que sumiu no fim da chamada. O global nunca foi tocado. (E o 11 que a função devolveu foi jogado fora, porque ninguém guardou.)

</details>

E se você tentar **alterar** a global com `+=`?

```python
>>> reprovadas = 0
>>> def registrar_reprovacao():
...     reprovadas += 1
...
>>> registrar_reprovacao()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in registrar_reprovacao
UnboundLocalError: cannot access local variable 'reprovadas' where it is not associated with a value
```

Como existe uma atribuição (`+=`) a `reprovadas` dentro da função, o Python decide que ela é local **na função inteira**. Aí, para somar 1, ele tenta ler a local, que ainda não tem valor. (No Python 3.10, a mensagem é `local variable 'reprovadas' referenced before assignment`.)

Existe a palavra `global reprovadas` para forçar o uso da global, mas **evite**. Uma função que mexe em variáveis de fora é difícil de testar e de entender. O jeito limpo é receber por parâmetro e devolver com `return`:

```python
>>> def registrar_reprovacao(reprovadas):
...     return reprovadas + 1
...
>>> reprovadas = 0
>>> reprovadas = registrar_reprovacao(reprovadas)
>>> reprovadas
1
```

> 💡 **Dica:** variáveis globais que **nunca mudam** são bem-vindas, como configurações: `TOLERANCIA_PADRAO = 10.0`. Pela convenção, escreva o nome em MAIÚSCULAS para avisar "isto é uma constante".

### Parâmetros e objetos mutáveis

No módulo 03 você viu que variáveis são etiquetas. Um parâmetro é só **mais uma etiqueta para o objeto que veio na chamada**. Daí duas situações bem diferentes:

> 🔮 **Preveja antes de rodar:** o que aparece no `print`?
>
> ```python
> def reatribuir(valores):
>     valores = [0, 0]
>
> def modificar(valores):
>     valores.append(0)
>
> a = [1, 2]
> b = [1, 2]
> reatribuir(a)
> modificar(b)
> print(a, b)
> ```

<details><summary>Resposta</summary>

`[1, 2] [1, 2, 0]`.

```text
 reatribuir(a):                       modificar(b):

  a ---------> [1, 2]                  b ---------> [1, 2, 0]
  valores --X                          valores ---^  (mesmo objeto)
  valores ---> [0, 0]  (nova; some
                        no fim)
```

- `valores = [0, 0]` só **move a etiqueta local** para uma lista nova. A lista de `a` não é tocada.
- `valores.append(0)` **mexe no objeto**, que é o mesmo de `b`.

</details>

Por isso a regra do módulo 03 continua valendo: **não modifique a coleção que você recebeu**, a não ser que esse seja o objetivo declarado da função. Exemplo completo: `exemplos/04_escopo.py`.

## 6. Docstrings e type hints

### Docstring: o manual da função

A string logo abaixo do `def` é a **docstring**. Ela vira a ajuda da função:

```python
def calcular_limites(nominal: float, tol_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± tol_pct %.

    Os limites são arredondados em 2 casas, para evitar o ruído do float
    (46 * 0.95 daria 43.699999999999996).
    """
```

```text
>>> help(calcular_limites)
Help on function calcular_limites in module __main__:

calcular_limites(nominal: float, tol_pct: float) -> tuple[float, float]
    Devolve (mínimo, máximo) para nominal ± tol_pct %.
    ...
```

No VS Code, passar o mouse sobre o nome da função mostra a mesma coisa. Boas docstrings:

- primeira linha curta dizendo **o que a função devolve ou faz** ("Devolve...", "Conta...");
- depois, se precisar, regras e casos especiais ("lista vazia devolve None");
- não repita o código; explique o que o código não diz.

### Type hints: os tipos esperados

As anotações depois dos parâmetros (`nominal: float`) e depois da seta (`-> tuple[float, float]`) são **type hints**: dizem que tipo cada coisa deveria ter.

| Anotação | Significa |
|---|---|
| `x: int`, `x: float`, `x: str`, `x: bool` | tipos simples |
| `medicoes: list[float]` | lista de floats |
| `tolerancias: dict[str, float]` | dicionário de str para float |
| `-> tuple[int, float]` | devolve uma tupla (int, float) |
| `-> float \| None` | devolve um float ou None |
| `-> None` | não devolve nada útil (só faz efeito) |

O Python **não confere** os hints na hora de rodar. Eles servem para você, para o leitor e para as ferramentas (o VS Code avisa quando você passa o tipo errado; o mypy, visto no módulo 09, confere o projeto inteiro).

```python
>>> def dobro(x: int) -> int:
...     return x * 2
...
>>> dobro("ab")
'abab'
```

O hint dizia `int`, mas o Python rodou com string mesmo. Hint é documentação verificável por ferramenta, não trava.

> 💡 **Dica:** nos exercícios, os stubs já vêm com hints. Leia-os como parte do enunciado: `-> list[str] | None` já diz "devolva uma lista de textos, ou None".

## 7. `*args` e `**kwargs`: quantos argumentos vierem

Às vezes você não sabe quantos argumentos virão. Quer escrever `media(50.2, 49.8, 51.0)` sem montar lista.

- `*nome` recolhe os argumentos **posicionais** que sobraram numa **tupla**.
- `**nome` recolhe os argumentos **nomeados** que sobraram num **dicionário**.

(Os nomes `args` e `kwargs` são só convenção; o que importa são os asteriscos.)

```python
>>> def media(*valores):
...     if not valores:
...         return None
...     return sum(valores) / len(valores)
...
>>> media(50.0, 52.0, 51.0)
51.0
>>> print(media())
None
>>> def criar_amostra(op, linha, **medidas):
...     return {"op": op, "linha": linha, **medidas}
...
>>> criar_amostra("OP-4512", "A", espessura=50.2, cof=0.22)
{'op': 'OP-4512', 'linha': 'A', 'espessura': 50.2, 'cof': 0.22}
```

Os asteriscos também funcionam **na chamada**, no sentido contrário: espalham uma lista em argumentos posicionais, ou um dicionário em argumentos nomeados.

```python
>>> medicoes = [49.2, 51.5, 50.1]
>>> media(*medicoes)
50.26666666666667
>>> dados = {"op": "OP-4513", "linha": "B", "gramatura": 18.4}
>>> criar_amostra(**dados)
{'op': 'OP-4513', 'linha': 'B', 'gramatura': 18.4}
```

Ordem dos parâmetros numa definição, quando aparecem juntos:

```text
 def f(normais, com_padrao=1, *args, so_por_nome=2, **kwargs):
```

Um uso que você vai adorar: um filtro do tipo `WHERE` em que qualquer coluna vira critério.

```python
>>> def filtrar(registros, **criterios):
...     return [r for r in registros
...             if all(r.get(coluna) == valor for coluna, valor in criterios.items())]
...
>>> tabela = [{"op": "OP-1", "linha": "A"}, {"op": "OP-2", "linha": "B"}]
>>> filtrar(tabela, linha="B")
[{'op': 'OP-2', 'linha': 'B'}]
```

> ⚠️ **Erro comum:** abusar de `**kwargs`. Se a função sempre recebe `op`, `nf` e `peso_kg`, declare os três parâmetros. Eles aparecem na ajuda, no autocompletar, e o Python reclama se faltar um. Use `*args`/`**kwargs` quando a quantidade ou os nomes **realmente** variam.

Exemplo completo: `exemplos/05_args_kwargs.py`.

## 8. Funções são valores

Em Python, uma função é um objeto como um número ou uma lista. Você pode guardá-la numa variável, passá-la como argumento e devolvê-la de outra função. Isso parece estranho no começo e é muito poderoso depois.

```python
>>> conferir_limites = calcular_limites
>>> conferir_limites(50.0, 10.0)
(45.0, 55.0)
```

Sem parênteses, `calcular_limites` é **a função**. Com parênteses, é **a chamada** (o resultado).

### Passando função como argumento

Pense no `CONT.SE` do Excel: você passa um intervalo e um **critério**. Em Python, o critério pode ser uma função:

```python
>>> def cont_se(valores, condicao):
...     return sum(1 for valor in valores if condicao(valor))
...
>>> def acima_de_50(valor):
...     return valor > 50
...
>>> cont_se([50.2, 44.1, 56.3], acima_de_50)
2
```

`cont_se` não sabe qual é o critério. Só sabe que pode chamá-lo. Você troca o critério sem mexer em `cont_se`. Você já usou essa ideia no módulo 03: o `key=` do `sorted` recebe uma função.

Nos type hints, uma função é anotada como `Callable`. Para usar, importe no topo do arquivo: `from collections.abc import Callable`. `Callable[[float], bool]` quer dizer "função que recebe um float e devolve um bool". Os exercícios 06 e 13 usam.

### Exemplo resolvido: uma regra de conferência para cada tipo

No projeto, algumas propriedades usam **nominal ± %** (espessura, gramatura) e outras **faixa fixa** (COF). Como eu penso:

1. Escrevo **uma função para cada tipo de regra**, com a mesma "cara": recebem `(valor, regra)` e devolvem `True`/`False`.
2. Guardo as funções num **dicionário**: tipo → função.
3. Na hora de conferir, pego a função pelo tipo e chamo. Sem `if tipo == ... elif ...`.

```python
>>> def faixa_fixa(valor, regra):
...     return regra["min"] <= valor <= regra["max"]
...
>>> def nominal_percentual(valor, regra):
...     margem = regra["nominal"] * regra["tol_pct"] / 100
...     return regra["nominal"] - margem <= valor <= regra["nominal"] + margem
...
>>> VERIFICADORES = {"faixa": faixa_fixa, "nominal": nominal_percentual}
>>> regra_cof = {"tipo": "faixa", "min": 0.15, "max": 0.30}
>>> verificar = VERIFICADORES[regra_cof["tipo"]]
>>> verificar(0.33, regra_cof)
False
```

Amanhã surge um tipo novo ("só mínimo", para tração)? Escreva a função e acrescente uma linha no dicionário. Nada mais muda. Esse padrão (tabela de despacho) aparece no projeto final.

### Funções que fabricam funções

Uma função pode criar outra lá dentro e devolvê-la. A função de dentro **lembra** as variáveis de onde nasceu, mesmo depois que a de fora terminou. Isso se chama **closure** (fechamento).

```python
>>> def criar_verificador(minimo, maximo):
...     def verificar(valor):
...         return minimo <= valor <= maximo
...     return verificar
...
>>> linha_a = criar_verificador(45.0, 55.0)
>>> linha_b = criar_verificador(18.0, 22.0)
>>> linha_a(50.0), linha_b(50.0)
(True, False)
>>> cont_se([50.2, 44.1, 56.3], linha_a)
1
```

`linha_a` e `linha_b` são funções "pré-configuradas", cada uma com sua faixa.

Por fim, **métodos também são funções**: `str.upper` é a função por trás de `"op".upper()`. Então `str.upper("op-4512")` devolve `'OP-4512'`, e você pode passar `str.strip` ou `str.upper` como argumento para outra função, como no exercício 13.

> 🔧 **Modifique:** em `exemplos/06_funcoes_como_valores.py`, acrescente um tipo de regra `"minimo"` (só valor mínimo, como a tração) com sua função, e uma propriedade `"tracao"` que o use.

## 9. `lambda` e o parâmetro `key=`

Muitas vezes a função que você passa é minúscula e usada uma vez só. Para isso existe a **lambda**: uma função de uma expressão, sem nome.

```text
 lambda bobina: bobina["peso_kg"]
        \____/  \______________/
     parâmetros  o que devolve (uma expressão, sem "return")
```

É equivalente a:

```python
def peso(bobina):
    return bobina["peso_kg"]
```

O lugar natural da lambda é o `key=` de `sorted`, `min` e `max`:

```python
>>> bobinas = [
...     {"op": "OP-4513", "peso_kg": 320.5},
...     {"op": "OP-4512", "peso_kg": 500.0},
...     {"op": "OP-4514", "peso_kg": 210.0},
... ]
>>> [b["op"] for b in sorted(bobinas, key=lambda b: b["peso_kg"])]
['OP-4514', 'OP-4513', 'OP-4512']
>>> min([50.6, 49.8, 51.0], key=lambda v: abs(v - 50.0))
49.8
>>> sorted(["Selagem", "cof", "Gel"], key=lambda p: (len(p), p.lower()))
['cof', 'Gel', 'Selagem']
```

Quando **não** usar lambda:

- Se a lógica tem mais de uma expressão, ou precisa de um nome para ser entendida: use `def`.
- **Não guarde lambda em variável** (`peso = lambda b: b["peso_kg"]`). Se precisa de nome, use `def`: a mensagem de erro fica melhor e o ruff deixa de reclamar (regra E731).

Exemplo completo: `exemplos/07_lambda_key.py`.

## 10. Funções puras e efeitos colaterais

Uma função é **pura** quando:

1. o resultado depende **só dos argumentos** (mesma entrada → mesma saída, sempre);
2. ela **não muda nada fora dela**.

Qualquer coisa que a função faz "no mundo", além de devolver um valor, é um **efeito colateral**:

- imprimir na tela (`print`);
- alterar uma lista ou dicionário recebido;
- alterar uma variável global;
- ler ou gravar arquivo, banco de dados, planilha;
- mandar e-mail, clicar no TOTVS com um robô.

Efeitos colaterais não são "errados". Sem eles, o programa não serve para nada: alguém tem que ler a planilha e alguém tem que gerar o certificado. O problema é **misturar** efeitos com cálculo. Compare:

```python
reprovadas_do_dia = 0


def conferir_e_mostrar(medicoes, minimo, maximo):
    global reprovadas_do_dia
    medicoes.sort()  # altera a lista de quem chamou
    fora = [v for v in medicoes if not minimo <= v <= maximo]
    if fora:
        reprovadas_do_dia += 1  # altera o mundo lá fora
    print(f"{len(fora)} fora da faixa: {fora}")  # mostra em vez de devolver


def valores_fora(medicoes, minimo, maximo):
    """Pura: só recebe, calcula e devolve."""
    return [v for v in medicoes if not minimo <= v <= maximo]
```

Como você testaria `conferir_e_mostrar`? Teria que capturar a tela, conferir a global, conferir se a lista foi reordenada... E se chamar duas vezes, a global já mudou. Já a pura se testa com uma linha:

```python
>>> def valores_fora(medicoes, minimo, maximo):
...     return [v for v in medicoes if not minimo <= v <= maximo]
...
>>> valores_fora([50.2, 56.3, 44.1], 45.0, 55.0) == [56.3, 44.1]
True
```

### Núcleo puro, casca com efeitos

A arquitetura que você vai usar no projeto final (e que times profissionais usam) é esta:

```text
 +------------------------- casca: efeitos --------------------------+
 |                                                                   |
 |  ler planilha  -->  +------------ núcleo puro ------------+  -->  |
 |  ler e-mail         |  calcular limites                   |       |
 |                     |  conferir amostras                  |  imprimir
 |                     |  decidir status                     |  salvar
 |                     |  montar o texto do certificado      |  robô no TOTVS
 |                     +-------------------------------------+       |
 +-------------------------------------------------------------------+
```

- O **núcleo** recebe dados prontos (listas, dicionários) e devolve resultados. É onde mora a lógica que pode dar errado, e é 100% testável.
- A **casca** é fina: lê, chama o núcleo, mostra ou grava. Quase não tem `if`.

Quando a planilha mudar de formato, só a casca muda. Quando a regra de tolerância mudar, só o núcleo muda, e os testes avisam se algo quebrou.

> 🔮 **Preveja antes de rodar:** esta função é pura? Por quê?
>
> ```python
> def proxima_op(ops_emitidas):
>     ops_emitidas.sort()
>     return ops_emitidas[-1]
> ```

<details><summary>Resposta</summary>

**Não.** O resultado depende só do argumento, mas o `sort()` **altera a lista de quem chamou**: depois da chamada, `ops_emitidas` está ordenada. Versão pura: `return max(ops_emitidas)`, ou `return sorted(ops_emitidas)[-1]` (o `sorted` cria uma lista nova).

</details>

Exemplo completo, com a versão "faz tudo" e a versão pura lado a lado: `exemplos/08_puras_vs_efeitos.py`.

## 11. Decomposição de problemas

Esta é a habilidade mais importante do módulo. Linguagem você aprende em semanas; **quebrar um problema** é o que leva tempo, e é o que faz você ser contratado.

### O método em 6 passos

1. **Escreva o problema em uma frase.** Se não cabe numa frase, ainda não está claro.
2. **Liste os passos em português**, sem pensar em código. "Para cada amostra: achar os limites da linha, contar quantas medições estão fora, ..."
3. **Cada passo vira uma função** com nome de verbo. Se um passo ainda é grande, quebre de novo.
4. **Escreva as assinaturas antes do corpo:** nome, parâmetros, o que devolve, docstring. Escreva a função de cima **como se as de baixo já existissem**. (Isso tem nome: *programação por desejo*. Você "deseja" a função e depois a escreve.)
5. **Implemente de baixo para cima, testando cada uma** no REPL ou com `assert` antes de ir para a próxima.
6. **Componha:** a função de cima vira uma "receita" que só chama as outras.

### Exemplo resolvido: o relatório do turno

**Passo 1. O problema em uma frase:** "Para cada amostra do turno, dizer a média da espessura, quantas medições ficaram fora da tolerância da linha e se a OP foi aprovada; no fim, o total de aprovadas."

Os dados:

```python
>>> NOMINAIS = {"A": (50.0, 10.0), "B": (20.0, 8.0)}
>>> AMOSTRAS = [
...     {"op": "OP-4512", "linha": "A", "medicoes": [50.2, 49.8, 51.0]},
...     {"op": "OP-4513", "linha": "B", "medicoes": [20.1, 22.3, 19.0]},
...     {"op": "OP-4514", "linha": "A", "medicoes": [44.0, 50.3]},
... ]
```

A saída desejada:

```text
OP-4512 (A): média 50.33 µm, 0 fora -> APROVADA
OP-4513 (B): média 20.47 µm, 1 fora -> REPROVADA
OP-4514 (A): média 47.15 µm, 1 fora -> REPROVADA
Turno: 1/3 OPs aprovadas
```

O primeiro impulso é escrever tudo num `for` só, com ifs e contas misturados. Funciona (está em `exemplos/09_decomposicao.py`, na função `relatorio_monolitico`), mas tem 25 linhas, quatro níveis de indentação, e nenhum pedaço pode ser testado sozinho.

**Passo 2. Os passos em português:**

- para cada amostra:
  - achar os limites da linha (nominal ± %);
  - contar as medições fora dos limites;
  - calcular a média;
  - decidir o status;
  - escrever a linha do relatório;
- no fim, escrever a linha do total.

**Passo 3. A árvore de funções:**

```text
 gerar_relatorio(amostras, nominais)  -> list[str]
 +-- conferir_amostra(amostra, nominais)  -> dict
 |   +-- calcular_limites(nominal, tol_pct)  -> (mín, máx)
 |   +-- contar_fora(medicoes, limites)      -> int
 |   +-- media(valores)                      -> float
 +-- formatar_linha(conferencia)          -> str
 +-- formatar_rodape(conferencias)        -> str
```

Repare: o **cálculo** (`conferir_amostra`) está separado da **apresentação** (`formatar_...`). Se amanhã o relatório virar uma planilha Excel, só as funções de formatar mudam.

**Passo 4. As assinaturas primeiro.** Começo pela função de cima, "desejando" as outras:

```python
def gerar_relatorio(amostras, nominais):
    """A receita: só junta as funções de baixo."""
    conferencias = [conferir_amostra(a, nominais) for a in amostras]
    return [formatar_linha(c) for c in conferencias] + [formatar_rodape(conferencias)]
```

Ela ainda não roda (as outras não existem), mas já mostra se o desenho faz sentido. Fez? Desço um nível.

**Passo 5. De baixo para cima, testando cada uma.** Primeiro as folhas da árvore, que não dependem de ninguém:

```python
>>> def calcular_limites(nominal, tol_pct):
...     fator = tol_pct / 100
...     return round(nominal * (1 - fator), 2), round(nominal * (1 + fator), 2)
...
>>> def contar_fora(medicoes, limites):
...     minimo, maximo = limites
...     return sum(1 for valor in medicoes if not minimo <= valor <= maximo)
...
>>> def media(valores):
...     return sum(valores) / len(valores)
...
>>> calcular_limites(50.0, 10.0)
(45.0, 55.0)
>>> contar_fora([44.0, 50.3], (45.0, 55.0))
1
```

Testei cada uma **antes** de usar. Se `contar_fora` tivesse um erro, eu descobriria agora, numa função de 3 linhas, e não depois, no meio do relatório. Agora o nível do meio:

```python
>>> def conferir_amostra(amostra, nominais):
...     limites = calcular_limites(*nominais[amostra["linha"]])
...     fora = contar_fora(amostra["medicoes"], limites)
...     return {
...         "op": amostra["op"],
...         "linha": amostra["linha"],
...         "media": media(amostra["medicoes"]),
...         "fora": fora,
...         "status": "APROVADA" if fora == 0 else "REPROVADA",
...     }
...
>>> conferir_amostra(AMOSTRAS[2], NOMINAIS)["status"]
'REPROVADA'
```

O `*nominais[...]` espalha a tupla `(50.0, 10.0)` nos dois parâmetros de `calcular_limites` (seção 7). E as funções de apresentação:

```python
>>> def formatar_linha(c):
...     return (f"{c['op']} ({c['linha']}): média {c['media']:.2f} µm, "
...             f"{c['fora']} fora -> {c['status']}")
...
>>> def formatar_rodape(conferencias):
...     aprovadas = sum(1 for c in conferencias if c["status"] == "APROVADA")
...     return f"Turno: {aprovadas}/{len(conferencias)} OPs aprovadas"
...
```

**Passo 6. Compor:**

```python
>>> def gerar_relatorio(amostras, nominais):
...     conferencias = [conferir_amostra(a, nominais) for a in amostras]
...     return [formatar_linha(c) for c in conferencias] + [formatar_rodape(conferencias)]
...
>>> for linha in gerar_relatorio(AMOSTRAS, NOMINAIS):
...     print(linha)
...
OP-4512 (A): média 50.33 µm, 0 fora -> APROVADA
OP-4513 (B): média 20.47 µm, 1 fora -> REPROVADA
OP-4514 (A): média 47.15 µm, 1 fora -> REPROVADA
Turno: 1/3 OPs aprovadas
```

Mais linhas no total do que a versão monolítica? Um pouco. Mas cada função cabe na tela, tem um nome que explica o que faz e pode ser testada sozinha. E o arquivo de exemplo termina com um `assert` provando que as duas versões dão **exatamente** o mesmo resultado: é assim que se refatora com segurança.

> 🔧 **Modifique:** o supervisor quer ver também o **maior desvio** de cada OP em relação ao nominal. Em `exemplos/09_decomposicao.py`, quais funções você muda? (Resposta: uma função nova `maior_desvio`, uma chave a mais em `conferir_amostra` e um trecho em `formatar_linha`. Nenhuma outra função precisa mudar.)

### Sinais de que uma função precisa ser quebrada

- O nome precisa de um "**e**": `conferir_e_imprimir`, `ler_e_validar`. São duas funções.
- Ela tem mais de ~20 linhas, ou mais de 2 níveis de indentação.
- Você escreveu um comentário do tipo `# agora calcula a média` no meio dela: esse trecho quer ser uma função chamada `media`.
- Ela mistura **calcular** com **mostrar** ou **gravar**.
- Para testá-la, você precisa preparar o mundo inteiro.

### Mais um exemplo resolvido: regras de senha

Decomposição não é só para laboratório. Um sistema exige senha com 8+ caracteres, pelo menos um dígito e pelo menos uma maiúscula, e quer dizer **todos** os problemas de uma vez.

Três métodos de string ajudam aqui (o módulo 05 aprofunda): `c.isdigit()` diz se o caractere `c` é um dígito; `c.isupper()`, se é letra maiúscula; e `texto.startswith("OP-")` diz se o texto começa com `"OP-"`. Os dois primeiros funcionam também com um texto inteiro: `"4512".isdigit()` é `True`.

Como eu penso: cada regra é uma pergunta de sim/não → uma função pequena. A lista de problemas é "as regras que falharam" → um dicionário descrição → função, e uma compreensão.

```python
>>> def tem_tamanho_minimo(senha):
...     return len(senha) >= 8
...
>>> def tem_digito(senha):
...     return any(c.isdigit() for c in senha)
...
>>> def tem_maiuscula(senha):
...     return any(c.isupper() for c in senha)
...
>>> REGRAS = {
...     "pelo menos 8 caracteres": tem_tamanho_minimo,
...     "pelo menos um dígito": tem_digito,
...     "pelo menos uma maiúscula": tem_maiuscula,
... }
>>> def problemas_da_senha(senha):
...     return [descricao for descricao, regra in REGRAS.items() if not regra(senha)]
...
>>> problemas_da_senha("bobina")
['pelo menos 8 caracteres', 'pelo menos um dígito', 'pelo menos uma maiúscula']
>>> problemas_da_senha("Bobina2026")
[]
```

Uma regra nova é uma função nova e uma linha no dicionário. O exercício 12 usa a mesma ideia para validar os pedidos da expedição (OP, NF e peso).

## 12. Recursão (introdução)

Uma função **recursiva** chama a si mesma para resolver um pedaço **menor** do mesmo problema. Toda recursão tem duas partes:

- **caso base:** o problema é tão pequeno que a resposta é direta. Aqui a função **para** de se chamar;
- **caso recursivo:** a função resolve um pedaço e chama a si mesma com o resto, que é menor.

O exemplo clássico é o fatorial: `n! = n × (n−1)!`, e `0! = 1`.

```python
>>> def fatorial(n):
...     if n == 0:
...         return 1
...     return n * fatorial(n - 1)
...
>>> fatorial(5)
120
```

O `exemplos/10_recursao.py` imprime o "rastro" das chamadas. Cada chamada fica esperando a de baixo responder:

```text
fatorial(3) chamado
  fatorial(2) chamado
    fatorial(1) chamado
      fatorial(0) chamado
      fatorial(0) devolve 1
    fatorial(1) devolve 1
  fatorial(2) devolve 2
fatorial(3) devolve 6
```

> 🔮 **Preveja antes de rodar:** em que ordem os números aparecem?
>
> ```python
> def contagem(n):
>     if n == 0:
>         return
>     print("ida", n)
>     contagem(n - 1)
>     print("volta", n)
>
> contagem(2)
> ```

<details><summary>Resposta</summary>

```text
ida 2
ida 1
volta 1
volta 2
```

O `print("volta", n)` de cada chamada só roda **depois** que a chamada de baixo termina. Por isso as "voltas" saem em ordem inversa: a última chamada a começar é a primeira a terminar (como uma pilha de pratos).

</details>

### Onde a recursão brilha: estruturas aninhadas

Para somar uma lista "reta", um `for` é mais simples. A recursão vale a pena quando a estrutura tem **níveis que você não conhece de antemão**: listas dentro de listas, pastas dentro de pastas, categorias dentro de categorias.

Para saber se um item é lista, use `isinstance(item, list)`: devolve `True` se `item` for uma lista. É parecido com `type(item) == list`, que você viu no módulo 01, mas é a forma recomendada.

**Exemplo resolvido: o peso de uma carga.** Um carregamento tem paletes; paletes têm bobinas ou caixas; caixas têm bobinas... Quero o peso total.

```python
>>> carga = [[100.0, 120.5], [80.0, [40.0, 40.0]], 10.0]
```

Como eu penso:

1. Uma carga é "uma lista de coisas, e cada coisa é um **número** ou **outra carga**". A definição já é recursiva!
2. Caso base: o item é um número → o peso é ele mesmo.
3. Caso recursivo: o item é uma lista → o peso é a soma dessa lista, que é **o mesmo problema, menor**.
4. Por que termina? Cada chamada recebe uma lista que está **dentro** da anterior. Uma hora só sobram números.

```python
>>> def soma_aninhada(itens):
...     total = 0
...     for item in itens:
...         if isinstance(item, list):
...             total += soma_aninhada(item)
...         else:
...             total += item
...     return total
...
>>> soma_aninhada(carga)
390.5
```

### Quando a recursão dá errado

Sem caso base (ou com um caso recursivo que não diminui o problema), a função se chama para sempre. O Python corta depois de cerca de 1000 chamadas:

```text
Traceback (most recent call last):
  File "C:\curso-python\rec.py", line 6, in <module>
    contagem(3)
  File "C:\curso-python\rec.py", line 3, in contagem
    return contagem(n - 1)
  File "C:\curso-python\rec.py", line 3, in contagem
    return contagem(n - 1)
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
```

Use recursão **com moderação**: para dados aninhados de profundidade desconhecida, ela é a ferramenta certa. Para "repetir N vezes" ou percorrer uma lista, use laço.

## Lendo mensagens de erro deste módulo

Com funções, o traceback ganha **várias camadas**: uma para cada chamada em andamento. Leia de baixo para cima: a última linha diz **o que**; a última camada diz **onde** estourou; as camadas de cima dizem **quem chamou quem**.

**1. Argumento faltando, duas camadas abaixo.**

```text
Traceback (most recent call last):
  File "C:\curso-python\laudo.py", line 11, in <module>
    print(conferir(50.2, 50.0))
          ~~~~~~~~^^^^^^^^^^^^
  File "C:\curso-python\laudo.py", line 7, in conferir
    minimo, maximo = calcular_limites(nominal)
                     ~~~~~~~~~~~~~~~~^^^^^^^^^
TypeError: calcular_limites() missing 1 required positional argument: 'tol_pct'
```

Leitura: o programa chamou `conferir` (linha 11), que chamou `calcular_limites` (linha 7) sem o `tol_pct`. O defeito está na **linha 7**, na chamada, não dentro de `calcular_limites`.

**2. `UnboundLocalError`.**

```text
Traceback (most recent call last):
  File "C:\curso-python\contador.py", line 8, in <module>
    registrar_reprovacao()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "C:\curso-python\contador.py", line 5, in registrar_reprovacao
    reprovadas += 1
    ^^^^^^^^^^
UnboundLocalError: cannot access local variable 'reprovadas' where it is not associated with a value
```

Leitura: a função tenta alterar uma variável global. Correção: receba o valor por parâmetro e devolva o novo valor (seção 5).

**3. Função sem `return` usada num cálculo.**

```text
Traceback (most recent call last):
  File "C:\curso-python\media.py", line 6, in <module>
    print(round(m, 1))
          ~~~~~^^^^^^
TypeError: type NoneType doesn't define __round__ method
```

Leitura: `m` é `None`. Ele veio de `m = media([...])`, e a função `media` calcula mas **esqueceu o `return`**. Toda mensagem com `NoneType` pede a mesma pergunta: "de qual função veio esse valor, e ela tem `return` em todos os caminhos?"

**Outros que você vai encontrar:**

| Mensagem | Causa provável | Correção |
|---|---|---|
| `TypeError: f() takes 2 positional arguments but 3 were given` | argumento a mais (ou parâmetro esquecido no `def`) | confira a assinatura |
| `TypeError: f() got an unexpected keyword argument 'x'` | nome de argumento errado (erro de digitação?) | use o nome exato do parâmetro |
| `TypeError: f() got multiple values for argument 'x'` | o mesmo parâmetro passado por posição e por nome | passe uma vez só |
| `SyntaxError: parameter without a default follows parameter with a default` | parâmetro sem padrão depois de um com padrão | parâmetros sem padrão primeiro |
| `NameError: name 'x' is not defined` | usou fora da função uma variável local dela | devolva o valor com `return` |
| `TypeError: 'NoneType' object is not subscriptable` | função sem `return` (ou com `return` só em alguns caminhos) | garanta `return` em todos os caminhos |
| `TypeError: 'float' object is not callable` | você criou uma variável com o nome de uma função (`media = media(...)`) e depois chamou a "função" | use nomes diferentes para a função e para o resultado |
| `RecursionError: maximum recursion depth exceeded` | recursão sem caso base, ou que não diminui o problema | confira o caso base |

> 💡 **Dica:** quando o traceback é longo, procure a **última camada que é código seu**. As camadas de bibliotecas (pandas, openpyxl) raramente são onde está o defeito.

## Boas práticas

- **Nome de função é verbo** (`calcular_limites`, `conferir_amostra`, `formatar_linha`). Função que devolve bool pode ser pergunta: `esta_na_faixa`, `tem_digito`.
- **Uma função, uma tarefa.** Se o nome precisa de "e", quebre.
- **Funções pequenas:** cabem na tela, idealmente com menos de 20 linhas.
- **Calcule em funções puras; imprima e grave nas bordas** (núcleo puro, casca fina).
- **Devolva, não imprima,** em funções de cálculo.
- **Não modifique argumentos mutáveis** a menos que esse seja o objetivo declarado.
- **Nunca use lista, dicionário ou conjunto como valor padrão.** Use `None`.
- **Retorno antecipado** para casos inválidos; caminho feliz no fim, sem indentação extra.
- **Argumentos nomeados** para números soltos: `calcular_limites(46.0, tol_pct=5.0)`.
- **Docstring em toda função** que outra pessoa (ou você daqui a um mês) vai usar.
- **Evite `global`.** Constantes em MAIÚSCULAS no topo do arquivo são a exceção bem-vinda.
- **Teste cada função assim que escrevê-la**, com um `assert` ou no REPL.

## No mundo real

O coração do seu projeto final é: dado um pedido da expedição e o resultado do laboratório, montar o certificado. A regra: **se a OP tem especificação própria, ela vale; o que ela não define vem do padrão da linha**. E COF fora da faixa pode ser liberado pela qualidade com a observação "COF: liberado".

O `exemplos/11_mundo_real_certificado.py` resolve isso com funções puras e uma casca mínima. Os dados (`PADROES_DA_LINHA`, `ESPECIFICACOES` e `UNIDADES`) ficam no topo do arquivo; o núcleo é este:

```python
def regras_da_op(op, linha):
    """Devolve (título, regras): especificação da OP sobre o padrão da linha."""
    padrao = PADROES_DA_LINHA[linha]
    especificacao = ESPECIFICACOES.get(op)
    if especificacao is None:
        return f"Padrão da linha {linha}", padrao
    return especificacao["titulo"], padrao | especificacao["regras"]


def faixa(regra):
    """Converte {nominal, tol_pct} ou {min, max} em (mínimo, máximo)."""
    if "nominal" in regra:
        fator = regra["tol_pct"] / 100
        return round(regra["nominal"] * (1 - fator), 2), round(regra["nominal"] * (1 + fator), 2)
    return regra["min"], regra["max"]


def conforme(valor, regra):
    minimo, maximo = faixa(regra)
    return minimo <= valor <= maximo


def parecer(falhas, observacao):
    """APROVADO, APROVADO COM RESSALVA (só COF fora e liberado) ou REPROVADO."""
    if not falhas:
        return "APROVADO"
    if falhas == ["cof"] and "cof: liberado" in observacao.lower():
        return "APROVADO COM RESSALVA (COF: liberado)"
    return "REPROVADO"


def montar_certificado(pedido, resultado):
    """Texto completo do certificado. Não imprime nada: devolve uma string."""
    titulo, regras = regras_da_op(pedido["op"], resultado["linha"])
    medidas = resultado["medidas"]
    falhas = [p for p, regra in regras.items() if not conforme(medidas[p], regra)]
    cabecalho = [
        "CERTIFICADO DE QUALIDADE",
        f"OP: {pedido['op']}   NF: {pedido['nf']}   Peso: {pedido['peso_kg']} kg",
        f"Especificação: {titulo}",
        "-" * 50,
    ]
    tabela = [linha_da_tabela(p, medidas[p], regra) for p, regra in regras.items()]
    rodape = ["-" * 50, f"Parecer: {parecer(falhas, resultado['obs'])}"]
    return "\n".join(cabecalho + tabela + rodape)  # "\n" = quebra de linha
```

(`linha_da_tabela` formata uma linha da tabela com as casas decimais de cada propriedade; veja no arquivo.) A casca (`main`) só monta os dados de exemplo e imprime:

```text
CERTIFICADO DE QUALIDADE
OP: OP-4512   NF: 000123456   Peso: 1250.5 kg
Especificação: Filme PE 50 µm alta selagem
--------------------------------------------------
espessura  51.2 µm     47.5 a 52.5    conforme
gramatura  46.3 g/m²   43.7 a 48.3    conforme
cof        0.22        0.15 a 0.30    conforme
--------------------------------------------------
Parecer: APROVADO

CERTIFICADO DE QUALIDADE
OP: OP-4514   NF: 000123457   Peso: 830.0 kg
Especificação: Padrão da linha A
--------------------------------------------------
espessura  49.1 µm     45.0 a 55.0    conforme
gramatura  45.8 g/m²   43.7 a 48.3    conforme
cof        0.33        0.15 a 0.30    NÃO conforme
--------------------------------------------------
Parecer: APROVADO COM RESSALVA (COF: liberado)
```

Repare em três decisões de projeto:

- **`padrao | especificacao["regras"]`**: a regra de negócio "especificação da OP sobre o padrão" é uma linha, e mora numa função só (`regras_da_op`).
- **`montar_certificado` devolve texto**: amanhã o mesmo texto pode ir para o `print`, para um arquivo, para o corpo de um e-mail ou para o robô que preenche o TOTVS. O núcleo não muda.
- **Cada função se testa com um `assert`**: `assert parecer([], "") == "APROVADO"`, `assert faixa({"min": 0.15, "max": 0.30}) == (0.15, 0.30)`. No módulo 09, esses asserts viram uma suíte de testes com pytest.

## Resumo

| Quero... | Sintaxe |
|---|---|
| definir e devolver | `def nome(a, b):` ... `return resultado` |
| devolver vários valores | `return minimo, maximo` → `mi, ma = f(...)` |
| valor padrão | `def f(valor, casas=1):` |
| padrão mutável (certo) | `def f(x, itens=None):` + `if itens is None: itens = []` |
| argumento nomeado | `f(46.0, tol_pct=5.0)` |
| só por nome | `def f(valor, *, casas=1):` |
| quantos posicionais vierem | `def f(*valores):` (tupla) |
| quantos nomeados vierem | `def f(**campos):` (dicionário) |
| espalhar na chamada | `f(*lista)`, `f(**dicionario)` |
| retorno antecipado | `if invalido: return None` no começo |
| docstring | `"""Devolve ..."""` logo abaixo do `def` |
| type hints | `def f(x: float, ys: list[str]) -> dict[str, int] \| None:` |
| função como argumento | `cont_se(valores, acima_de_50)` |
| fábrica de funções (closure) | `def criar(m): def f(x): ... return f` |
| lambda | `sorted(itens, key=lambda i: i["peso"])` |
| recursão | caso base com `return` + chamada com problema menor |
| ver ajuda | `help(funcao)` |

## Você domina este módulo se...

- [ ] Explico, sem consultar, a diferença entre `print` e `return`, e por que uma função sem `return` devolve `None`.
- [ ] Prevejo o que acontece com uma lista usada como valor padrão, e escrevo a correção com `None` de memória.
- [ ] Sei dizer se uma variável é local ou global olhando o código, e explico um `UnboundLocalError`.
- [ ] Reescrevo uma "flecha" de `if` aninhados com retorno antecipado.
- [ ] Passo uma função como argumento, guardo funções num dicionário e escrevo uma função que devolve outra.
- [ ] Classifico uma função como pura ou não, e aponto os efeitos colaterais dela.
- [ ] Dado um problema de uma frase, desenho a árvore de funções, escrevo as assinaturas e implemento de baixo para cima, testando cada uma.
- [ ] Escrevo uma função recursiva com caso base e explico por que ela termina.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_dividir_lote` | ★☆☆ | vários retornos (tupla), retorno antecipado, uma função usando outra |
| 02 | `ex02_formatar_medida` | ★☆☆ | valores padrão, argumentos nomeados, formato com variável |
| 03 | `ex03_conceito_nota` | ★☆☆ | retorno antecipado, ordem das regras |
| 04 | `ex04_media_args` | ★☆☆ | `*args`, espalhar lista na chamada |
| 05 | `ex05_padrao_mutavel` | ★☆☆ | a armadilha do padrão mutável e o idioma `None` |
| 06 | `ex06_funcoes_como_valores` | ★★☆ | função como argumento (CONT.SE/SOMASE), fábrica de funções |
| 07 | `ex07_ordenar_com_key` | ★★☆ | `lambda`, `key=` em `min` e `sorted`, critério com tupla |
| 08 | `ex08_filtrar_kwargs` | ★★☆ | `**kwargs`, filtro tipo WHERE |
| 09 | `ex09_leitura_escopo` | ★★☆ | **leitura de código:** prever escopo, padrão mutável, print × return; consertar uma função |
| 10 | `ex10_soma_recursiva` | ★★☆ | recursão em listas aninhadas |
| 11 | `ex11_laudo_decomposto` | ★★★ | **decomposição:** compor cinco funções pequenas num resumo de lote |
| 12 | `ex12_revisao_validar_pedido` | ★★★ | **revisão** 01+02+03: validadores pequenos, strings, `enumerate`, dicionários |
| 13 | `ex13_revisao_pipeline_limpeza` | ★★★ | **revisão** 01+02+03: `compor(*funcoes)`, métodos de string, conjunto para repetidos |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de `raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 04 ex01
```

Para testar o módulo todo: `python curso.py testar 04`. Para ver seu progresso: `python curso.py progresso`.

> 💡 **Dica:** no exercício 11, siga os 6 passos da seção 11. Faça uma função por vez, rode o teste, e só depois passe para a próxima. Os testes de cada função são separados justamente para isso.

## Desafio do módulo

**Fila de emissão de certificados.** Você recebe os pedidos do dia (alguns com erro de digitação), os resultados do laboratório, as especificações próprias de algumas OPs e os padrões de cada linha. Seu programa valida os pedidos, decide quais certificados podem ser emitidos (respeitando "especificação da OP sobre o padrão da linha" e "COF: liberado"), gera o texto de cada certificado e lista as pendências. Tudo com núcleo puro e casca fina.

Enunciado completo, requisitos e critérios de aceite: [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md) (14 perguntas, gabarito no final).

## Para ir além

- Tutorial oficial, definindo funções: [docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions](https://docs.python.org/pt-br/3/tutorial/controlflow.html#defining-functions)
- Mais sobre funções (padrões, nomeados, `*args`, `**kwargs`, lambda, docstrings): [docs.python.org/pt-br/3/tutorial/controlflow.html#more-on-defining-functions](https://docs.python.org/pt-br/3/tutorial/controlflow.html#more-on-defining-functions)
- FAQ oficial: por que valores padrão são compartilhados entre chamadas: [docs.python.org/pt-br/3/faq/programming.html](https://docs.python.org/pt-br/3/faq/programming.html#why-are-default-values-shared-between-objects)
- Type hints, guia rápido do mypy (em inglês): [mypy.readthedocs.io/en/stable/cheat_sheet_py3.html](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Leitura extra: capítulo "Funções" de *Código Limpo*, de Robert C. Martin. Use com bom senso: a ideia de funções pequenas e com um único propósito vale ouro; as regras radicais, nem tanto.
- Leitura extra: *Composing Programs*, capítulo 1 (em inglês, gratuito, baseado no clássico SICP): [composingprograms.com](https://www.composingprograms.com/)
