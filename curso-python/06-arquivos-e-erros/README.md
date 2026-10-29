# Módulo 06 — Arquivos e tratamento de erros

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 05 · **Nível:** iniciante → intermediário

## O que você vai aprender

- Ler um traceback de baixo para cima e reconhecer as exceções mais comuns.
- Tratar erros com `try`, `except`, `else` e `finally`, capturando só o que deve.
- Levantar erros com `raise`, com mensagens que dizem **onde** está o problema.
- Criar exceções próprias (`ValorForaDaTolerancia`, `ArquivoInvalido`) e organizá-las
  numa família.
- Abrir, ler e gravar arquivos de texto com `with open(...)`, escolhendo modo e encoding.
- Trabalhar com caminhos usando `pathlib` (`Path`, `/`, `glob`, `mkdir`, `read_text`).
- Ler e gravar CSV no padrão do Excel brasileiro: `;`, vírgula decimal, `utf-8-sig` e
  `cp1252`.
- Ler e gravar JSON (configurações e regras).
- Gravar arquivos de forma segura (sem corromper o que já existia) e validar dados na
  entrada.

## Por que isso importa

Programa de verdade conversa com arquivos: a planilha exportada do Excel, o JSON de
configuração, o log do robô. E arquivo de verdade vem com problema: célula vazia,
"#N/D", acento quebrado, coluna faltando, arquivo aberto no Excel por outra pessoa.

Iniciante escreve código que funciona com o arquivo perfeito. Profissional escreve
código que, diante do arquivo ruim, **para no lugar certo, com uma mensagem clara**, ou
segue em frente registrando o problema. Essa diferença aparece em qualquer entrevista de
dados, automação ou backend.

No projeto final, este módulo é a base de tudo: ler as medições, carregar as regras de
tolerância, gravar o resultado para o Excel e **não emitir certificado** de lote fora da
especificação.

> 💡 **Dica:** os exemplos completos estão em `exemplos/`, na ordem das seções. Os
> arquivos de dados ficam em `dados/`. Rode a partir da pasta `curso-python`, por
> exemplo: `python 06-arquivos-e-erros/exemplos/01_excecoes.py`.

## 1. Quando algo dá errado: exceções

Quando o Python encontra algo que não consegue fazer, ele **levanta uma exceção**: um
objeto que descreve o problema. Se ninguém trata a exceção, o programa para e mostra o
*traceback*.

```python
>>> int("25,4")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: '25,4'
```

### Lendo um traceback

Leia **de baixo para cima**. A última linha diz o quê; as de cima dizem onde.

```text
Traceback (most recent call last):
  File "C:\curso-python\conferir.py", line 12, in <module>      ← quem chamou
    media = calcular_media(valores)
  File "C:\curso-python\conferir.py", line 5, in calcular_media ← onde quebrou
    return sum(valores) / len(valores)
ZeroDivisionError: division by zero                              ← o QUE aconteceu
```

1. Última linha: o **tipo** (`ZeroDivisionError`) e a **mensagem**.
2. Linha logo acima: o arquivo, a linha e o código exato que quebrou.
3. Mais acima: o caminho de chamadas até ali. Procure a primeira linha que é **seu**
   código (e não de uma biblioteca).

### As exceções que você mais vai ver

```text
Exceção              Quando acontece                          Exemplo
------------------   --------------------------------------   ---------------------------
ValueError           tipo certo, valor impossível             float("25,4 kg")
TypeError            tipo errado para a operação              "25,4" + 1
KeyError             chave que não existe no dicionário       linha["lote"] sem coluna lote
IndexError           posição que não existe na lista          valores[10] numa lista de 3
ZeroDivisionError    divisão por zero                         sum([]) / len([])
AttributeError       atributo/método que não existe           None.group(1)
FileNotFoundError    arquivo ou pasta não existe              open("laudo.csv")
PermissionError      sem permissão (ou arquivo aberto no Excel) gravar em resultado.csv aberto
UnicodeDecodeError   bytes num encoding diferente do pedido   cp1252 lido como UTF-8
```

As exceções formam uma **família** (uma hierarquia). Capturar a "mãe" captura também
as filhas. Isso vai ser importante daqui a pouco.

```text
Exception
 ├── ArithmeticError
 │    └── ZeroDivisionError
 ├── LookupError
 │    ├── IndexError
 │    └── KeyError
 ├── OSError
 │    ├── FileNotFoundError
 │    ├── FileExistsError
 │    └── PermissionError
 ├── TypeError
 └── ValueError
      ├── UnicodeDecodeError     (via UnicodeError)
      └── json.JSONDecodeError
```

> 🔮 **Preveja antes de rodar:** qual exceção (tipo e mensagem) cada linha levanta?
> Rode uma de cada vez no REPL.
>
> ```python
> medicoes = {"espessura": 25.4}
> valores = [25.4, 26.1]
> medicoes["cof"]
> valores[5]
> "25,4" + 1
> 10 / 0
> ```

<details><summary>Resposta</summary>

- `medicoes["cof"]` → `KeyError: 'cof'` (a mensagem é só a chave que faltou).
- `valores[5]` → `IndexError: list index out of range`.
- `"25,4" + 1` → `TypeError: can only concatenate str (not "int") to str`.
- `10 / 0` → `ZeroDivisionError: division by zero`.

</details>

## 2. try/except: tratando o erro

Quando você **sabe** que algo pode dar errado e sabe o que fazer nesse caso, use
`try/except`. O código "arriscado" vai no `try`; o plano B, no `except`.

```python
>>> texto = "25,4"
>>> try:
...     valor = float(texto)
... except ValueError:
...     print(f"Não consegui converter {texto!r}")
...
Não consegui converter '25,4'
```

Se nada der errado, o `except` é pulado. Se der um erro **de outro tipo**, ele não é
capturado e continua subindo. Com `as`, você pega o objeto da exceção e pode usar a
mensagem:

```python
>>> try:
...     float("abc")
... except ValueError as erro:
...     print("Problema:", erro)
...
Problema: could not convert string to float: 'abc'
```

### Exemplo resolvido: rendimento do filme

Problema: calcular o rendimento (m² por kg) a partir de dois textos da planilha. Podem
acontecer dois problemas diferentes, e cada um merece uma mensagem diferente.

Primeiro eu listei o que pode dar errado: texto que não é número (`ValueError`) e peso
zero (`ZeroDivisionError`). Depois escrevi um `except` para cada um. Deixei no `try` só
as linhas que podem falhar.

```python
>>> def rendimento(area_texto, peso_texto):
...     try:
...         area = float(area_texto.replace(",", "."))
...         peso = float(peso_texto.replace(",", "."))
...         return area / peso
...     except ValueError:
...         print(f"Número inválido: área={area_texto!r}, peso={peso_texto!r}")
...     except ZeroDivisionError:
...         print("Peso zero: não dá para calcular o rendimento")
...     return None
...
>>> rendimento("1250", "25,5")
49.01960784313726
>>> rendimento("1250", "")
Número inválido: área='1250', peso=''
>>> rendimento("1250", "0")
Peso zero: não dá para calcular o rendimento
```

Quando o tratamento é igual para vários tipos, junte-os numa tupla:
`except (ValueError, ZeroDivisionError):`.

> ⚠️ **Erro comum:** o `except` "pega-tudo". Um `except:` sozinho (ou
> `except Exception:`) captura **qualquer** erro, inclusive os seus bugs:
>
> ```python
> def media(valores):
>     try:
>         return sum(valores) / len(valroes)   # erro de digitação!
>     except:
>         return 0
> ```
>
> `media([25.4, 26.1])` devolve `0`. O `NameError` do `valroes` foi engolido, e você
> vai passar horas procurando por que a média é zero. **Capture só o tipo que você sabe
> tratar.**

### Pedir perdão ou pedir permissão?

Existem dois estilos para lidar com problemas previsíveis:

```python
# Pedir permissão (verificar antes): "Look Before You Leap"
if "lote" in linha:
    lote = linha["lote"]

# Pedir perdão (tentar e tratar): "Easier to Ask Forgiveness than Permission"
try:
    lote = linha["lote"]
except KeyError:
    lote = None
```

Em Python, o segundo estilo é muito comum, principalmente com arquivos: entre o
`if caminho.exists()` e o `open`, outra pessoa pode apagar ou abrir o arquivo. Tentar e
tratar o erro é mais seguro. Para coisas simples, como uma chave de dicionário, use o
que ficar mais legível (aqui, `linha.get("lote")` seria ainda melhor).

## 3. else e finally

O `try` tem mais duas partes opcionais:

```text
try:       o código que pode dar erro
except:    roda SE deu erro (do tipo indicado)
else:      roda SE NÃO deu erro
finally:   roda SEMPRE: deu erro ou não, com return ou sem
```

```python
>>> def converter(texto):
...     try:
...         valor = float(texto)
...     except ValueError:
...         print("  except: inválido")
...         return None
...     else:
...         print("  else: convertido")
...         return valor
...     finally:
...         print("  finally: sempre")
...
>>> converter("25.4")
  else: convertido
  finally: sempre
25.4
>>> converter("x")
  except: inválido
  finally: sempre
```

Repare: o `finally` roda **antes** de a função de fato devolver o valor, mesmo com
`return` no meio. Por que usar `else` em vez de pôr o código no fim do `try`? Para
deixar no `try` só a linha que pode dar o erro tratado. Assim um erro no código do
`else` não é capturado por engano.

O `finally` serve para "arrumar a casa" sempre: fechar uma conexão, apagar um arquivo
temporário, registrar no log que o processo terminou. Para fechar arquivos, porém,
existe um jeito melhor: o `with` (seção 6).

> 🔮 **Preveja antes de rodar:** o que aparece na tela, e em que ordem?
>
> ```python
> for texto in ["10", "0", "x"]:
>     try:
>         resultado = 100 / int(texto)
>     except ZeroDivisionError:
>         print(texto, "-> divisão por zero")
>     except ValueError:
>         print(texto, "-> não é número")
>     else:
>         print(texto, "->", resultado)
>     finally:
>         print("fim de", texto)
> ```

<details><summary>Resposta</summary>

```text
10 -> 10.0
fim de 10
0 -> divisão por zero
fim de 0
x -> não é número
fim de x
```

Cada volta do `for` passa por exatamente um entre `except` e `else`, e sempre pelo
`finally`. O resultado de `100 / 10` é `10.0` (a barra `/` sempre devolve `float`).

</details>

## 4. raise: levantando seus próprios erros

Até agora o Python levantou os erros. Você também pode: `raise TipoDoErro("mensagem")`.
Use quando a sua função recebe algo com que **não dá para continuar**.

```python
>>> def checar_faixa(minimo, maximo):
...     if minimo > maximo:
...         raise ValueError(f"faixa inválida: mínimo {minimo} maior que máximo {maximo}")
...     return (minimo, maximo)
...
>>> checar_faixa(20, 30)
(20, 30)
>>> checar_faixa(30, 20)
Traceback (most recent call last):
  ...
ValueError: faixa inválida: mínimo 30 maior que máximo 20
```

Uma boa mensagem de erro diz **o que** está errado e **com qual valor**. Compare
"erro na leitura" com "linha 7: valor inválido em espessura: '2O,1'". A segunda poupa
meia hora de quem vai corrigir a planilha.

### Trocar o erro por outro mais claro: raise ... from

Às vezes você captura um erro técnico e quer levantar um erro com mais contexto. Use
`from erro` para **encadear**: o traceback mostra os dois.

```python
>>> def ler_peso(texto):
...     try:
...         return float(texto.replace(".", "").replace(",", "."))
...     except ValueError as erro:
...         raise ValueError(f"peso inválido no e-mail da expedição: {texto!r}") from erro
...
>>> ler_peso("1.250,5")
1250.5
```

Com `ler_peso("a confirmar")`, o traceback fica assim (resumido):

```text
ValueError: could not convert string to float: 'aconfirmar'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
ValueError: peso inválido no e-mail da expedição: 'a confirmar'
```

Repare no `'aconfirmar'` da primeira mensagem: o `replace(".", "")` não mexeu em nada,
mas o texto original tinha espaço, e o erro técnico mostra o texto **já transformado**.
Por isso a mensagem nova, com o texto original, ajuda tanto.

E se você só quer registrar algo e deixar o **mesmo** erro seguir? Use `raise` sozinho
dentro do `except`:

```python
try:
    processar(arquivo)
except PermissionError:
    print(f"Feche o arquivo {arquivo} no Excel e rode de novo.")
    raise   # relança o mesmo PermissionError
```

### Devolver None ou levantar erro?

```text
Situação                                              Faça
---------------------------------------------------   -----------------------------------
"Não achei" é normal e esperado (OP sem e-mail hoje)    devolva None (ou lista vazia)
Dado de entrada impossível (faixa invertida)            raise ValueError
Arquivo fora do formato (falta coluna)                  raise ArquivoInvalido (seção 5)
Resultado de negócio esperado (lote reprovado)          devolva o status ("REPROVADO")
Ação que NÃO pode acontecer (certificado de reprovado)  raise ValorForaDaTolerancia
```

## 5. Exceções personalizadas

`ValueError` serve para muita coisa. Quando o problema é do **seu domínio** (qualidade,
certificados), crie exceções com nomes que falam a língua do negócio. Quem chama pode
tratar cada uma de um jeito.

Criar uma exceção é criar uma **classe** filha de `Exception`. Classes são o assunto do
módulo 08; por enquanto, basta saber que `class Nome(Mae):` cria um tipo novo que "é
um" `Mae`, e que o corpo pode ter só uma docstring.

```python
>>> class ErroDeQualidade(Exception):
...     """Base de todos os erros do sistema de qualidade."""
...
>>> class ValorForaDaTolerancia(ErroDeQualidade):
...     """Uma medição saiu da faixa permitida."""
...
>>> class ArquivoInvalido(ErroDeQualidade):
...     """O arquivo existe, mas não está no formato esperado."""
...
```

```text
Exception
 └── ErroDeQualidade
      ├── ValorForaDaTolerancia
      └── ArquivoInvalido
```

Você usa do mesmo jeito que as exceções do Python: `raise ArquivoInvalido("...")` e
`except ArquivoInvalido:`. E `except ErroDeQualidade:` captura as duas filhas de uma vez.

### Exemplo resolvido: certificado só de lote aprovado

Problema: a função que emite o certificado **nunca** pode emitir para lote fora da
faixa, mesmo que quem a chamou esqueça de conferir.

Primeiro pensei em devolver `None` quando o lote estiver fora. Mas `None` é fácil de
ignorar: o robô poderia seguir e mandar um certificado vazio. Um erro não dá para
ignorar sem querer: ou alguém trata, ou o programa para. Por isso a função levanta
`ValorForaDaTolerancia`, e o laço que emite os certificados decide o que fazer.

```python
>>> def emitir_certificado(lote, espessura, minimo, maximo):
...     if not minimo <= espessura <= maximo:
...         raise ValorForaDaTolerancia(
...             f"lote {lote}: espessura {espessura} fora de [{minimo}, {maximo}]"
...         )
...     return f"Certificado do lote {lote}: espessura {espessura} µm (OK)"
...
>>> for lote, espessura in [("L001", 25.1), ("L002", 28.3), ("L003", 24.0)]:
...     try:
...         print(emitir_certificado(lote, espessura, 22.5, 27.5))
...     except ValorForaDaTolerancia as erro:
...         print("NÃO EMITIDO:", erro)
...
Certificado do lote L001: espessura 25.1 µm (OK)
NÃO EMITIDO: lote L002: espessura 28.3 fora de [22.5, 27.5]
Certificado do lote L003: espessura 24.0 µm (OK)
```

O programa não parou no L002: o erro foi tratado no lugar certo, e os outros lotes
seguiram. Repare na divisão de tarefas: `emitir_certificado` **detecta** o problema; o
laço **decide** o que fazer com ele.

> 🔧 **Modifique:** troque `except ValorForaDaTolerancia` por `except ErroDeQualidade` e
> rode de novo. Continua funcionando? Por quê? Depois troque por `except ArquivoInvalido`
> e veja o que acontece no L002.

> 🔮 **Preveja antes de rodar:** o que é impresso?
>
> ```python
> class ErroDeQualidade(Exception):
>     """Base."""
>
> class ArquivoInvalido(ErroDeQualidade):
>     """Arquivo fora do formato."""
>
> try:
>     raise ArquivoInvalido("cabeçalho sem a coluna lote")
> except ValueError:
>     print("A")
> except ErroDeQualidade as erro:
>     print("B", erro)
> except ArquivoInvalido:
>     print("C")
> ```

<details><summary>Resposta</summary>

`B cabeçalho sem a coluna lote`.

`ArquivoInvalido` não é filha de `ValueError`, então o primeiro `except` não serve. O
segundo serve (`ArquivoInvalido` é uma `ErroDeQualidade`) e, como só **um** `except`
roda, o terceiro nunca é alcançado. Lição: coloque os `except` mais específicos
**antes** dos mais genéricos.

</details>

## 6. Arquivos de texto: open e with

Para ler ou gravar um arquivo, você o **abre** com `open(caminho, modo, encoding=...)`
e recebe um objeto arquivo. O jeito certo é sempre dentro de um `with`:

```python
>>> with open("laudo.txt", "w", encoding="utf-8") as arquivo:
...     arquivo.write("Lote: L001\n")
...     arquivo.write("Espessura: 25,4 µm\n")
...
11
19
```

O `with` **fecha o arquivo sozinho** quando o bloco termina, mesmo que aconteça um erro
no meio. É como uma porta com mola: você não precisa lembrar de fechar. (Os números
`11` e `19` são o REPL mostrando o que `write` devolve: quantos caracteres gravou.)

> ⚠️ **Erro comum:** esperar que `write` pule de linha. Ele grava exatamente o texto
> que você passou. A quebra de linha é o `"\n"`, e é você quem coloca.

Para ler, há três jeitos principais:

```python
>>> with open("laudo.txt", encoding="utf-8") as arquivo:
...     conteudo = arquivo.read()          # o arquivo inteiro numa str
...
>>> conteudo
'Lote: L001\nEspessura: 25,4 µm\n'
>>> with open("laudo.txt", encoding="utf-8") as arquivo:
...     for linha in arquivo:              # uma linha por vez, com o "\n"
...         print(repr(linha))
...
'Lote: L001\n'
'Espessura: 25,4 µm\n'
>>> with open("laudo.txt", encoding="utf-8") as arquivo:
...     linhas = [linha.strip() for linha in arquivo]
...
>>> linhas
['Lote: L001', 'Espessura: 25,4 µm']
```

O `for linha in arquivo` lê aos poucos: serve até para arquivos de vários gigabytes.
O `read()` carrega tudo na memória de uma vez, o que é ótimo para arquivos pequenos.

### Modos de abertura

```text
Modo   Faz                                                   Se o arquivo não existe
----   ---------------------------------------------------   ------------------------
"r"    ler (é o padrão; pode omitir)                          FileNotFoundError
"w"    gravar do zero: APAGA o conteúdo anterior              cria
"a"    acrescentar no fim (append)                            cria
"x"    criar: dá erro se já existir (não sobrescreve nada)    cria
"b"    junto com outro ("rb", "wb"): bytes em vez de texto    -
```

> 🔮 **Preveja antes de rodar:** o que o último `print` mostra?
>
> ```python
> with open("teste.txt", "w", encoding="utf-8") as f:
>     f.write("A")
>     f.write("B")
> with open("teste.txt", "a", encoding="utf-8") as f:
>     f.write("C\n")
> with open("teste.txt", "w", encoding="utf-8") as f:
>     f.write("D")
> with open("teste.txt", encoding="utf-8") as f:
>     print(f.read())
> ```

<details><summary>Resposta</summary>

Só `D`.

O primeiro bloco grava `AB`; o segundo acrescenta `C` e uma quebra de linha (`ABC\n`).
Mas o terceiro abre em `"w"`, que **apaga tudo** antes de gravar. Esse é o erro que
mais destrói arquivos de log: abrir em `"w"` quando a intenção era `"a"`.

</details>

### Sempre diga o encoding

Você viu no módulo 05: sem `encoding=`, o Python usa o padrão do sistema, que no
Windows costuma ser cp1252. O mesmo programa lê certo no seu computador e quebra no do
colega. Regra: **todo `open` de texto leva `encoding=`**. Para arquivos seus, use
`"utf-8"`. Para arquivos do Excel, veja a seção 8.

