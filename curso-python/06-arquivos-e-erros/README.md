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

Com `ler_peso("1.250,5 kg")`, o traceback fica assim (resumido):

```text
ValueError: could not convert string to float: '1250.5 kg'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  ...
ValueError: peso inválido no e-mail da expedição: '1.250,5 kg'
```

Repare na primeira mensagem: ela mostra o texto **já transformado** (`'1250.5 kg'`),
que não existe em lugar nenhum do e-mail. A mensagem nova mostra o texto original, que
a pessoa consegue procurar e corrigir.

E se você só quer registrar algo e deixar o **mesmo** erro seguir? Use `raise` sozinho
dentro do `except`:

```python
try:
    processar(arquivo)
except PermissionError:
    print(f"Feche o arquivo {arquivo} no Excel e rode de novo.")
    raise   # relança o mesmo PermissionError
```

<details><summary>Tente você: escreva `validar_linha(texto)`, que devolve a linha de produção em maiúscula ("a" → "A") e levanta ValueError com uma mensagem clara se ela não for A, B, C ou D.</summary>

```python
def validar_linha(texto):
    linha = texto.strip().upper()
    if linha not in {"A", "B", "C", "D"}:
        raise ValueError(f"linha de produção inválida: {texto!r} (use A, B, C ou D)")
    return linha
```

`validar_linha(" b ")` devolve `'B'`; `validar_linha("E")` levanta
`ValueError: linha de produção inválida: 'E' (use A, B, C ou D)`. Repare no `!r`: as
aspas mostram espaços escondidos no valor digitado.

</details>

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

## 7. pathlib: caminhos sem dor

Caminho de arquivo como texto (`"C:\\Laudos\\2025\\linha_A.csv"`) dá trabalho: barras
diferentes no Windows e no Linux, `\n` virando quebra de linha, juntar pedaços com `+`.
O módulo `pathlib` resolve isso com o objeto `Path`. O operador `/` junta os pedaços.

```python
>>> from pathlib import Path
>>> laudo = Path("laudos") / "2025" / "linha_A.csv"
>>> laudo.name, laudo.stem, laudo.suffix
('linha_A.csv', 'linha_A', '.csv')
>>> laudo.parent.name
'2025'
>>> laudo.with_suffix(".xlsx").name
'linha_A.xlsx'
>>> laudo.exists()
False
>>> laudo.parent.mkdir(parents=True, exist_ok=True)
>>> laudo.write_text("lote;espessura\nL001;25,4\n", encoding="utf-8")
25
>>> laudo.exists(), laudo.is_file(), laudo.parent.is_dir()
(True, True, True)
>>> laudo.read_text(encoding="utf-8").splitlines()
['lote;espessura', 'L001;25,4']
```

- `mkdir(parents=True, exist_ok=True)`: cria as pastas que faltam e não reclama se já
  existirem.
- `read_text` e `write_text` abrem, leem (ou gravam) e fecham numa linha só. Ótimos
  para arquivos pequenos. Para ler bytes crus: `read_bytes`.

Ao imprimir, o `Path` usa a barra do sistema:

```text
>>> print(laudo)
laudos\2025\linha_A.csv      (Windows)
laudos/2025/linha_A.csv      (Linux e macOS)
```

### Percorrendo uma pasta

```python
>>> pasta = Path("laudos") / "2025"
>>> for nome in ["linha_B.csv", "linha_C.CSV", "notas.txt", "~$linha_D.xlsx"]:
...     (pasta / nome).touch()        # touch cria um arquivo vazio
...
>>> sorted(p.name for p in pasta.iterdir())
['linha_A.csv', 'linha_B.csv', 'linha_C.CSV', 'notas.txt', '~$linha_D.xlsx']
>>> sorted(p.name for p in pasta.glob("*.txt"))
['notas.txt']
>>> sorted(p.name for p in pasta.iterdir() if p.suffix.lower() == ".csv")
['linha_A.csv', 'linha_B.csv', 'linha_C.CSV']
```

`iterdir()` entrega tudo o que está na pasta; `glob("*.txt")` filtra por um padrão
(`rglob` faz o mesmo entrando nas subpastas). Cuidado: no Windows o `glob` ignora
maiúsculas e minúsculas, no Linux não. Para o mesmo resultado em qualquer sistema,
filtre com `p.suffix.lower()`. E os arquivos `~$...` são os temporários que o Excel
cria enquanto uma planilha está aberta: quase sempre você quer ignorá-los.

### Caminhos do Windows e a pasta do script

```python
Path(r"C:\Laudos\2025")      # raw string: as barras ficam como estão
Path("C:/Laudos/2025")       # barra normal também funciona no Windows
Path.home() / "Documents"    # a pasta do usuário (C:\Users\voce)
```

> ⚠️ **Erro comum:** escrever `"C:\novos\testes"` sem o `r`. O `\n` vira quebra de
> linha e o `\t` vira tab, e o caminho fica irreconhecível.

Outra armadilha: caminho relativo (`Path("dados/regras.json")`) é relativo à pasta de
onde você **rodou** o comando, e não à pasta do script. Rodou de outro lugar, levou um
`FileNotFoundError`. A solução é partir da pasta do próprio script:

```python
PASTA_DO_SCRIPT = Path(__file__).resolve().parent     # onde este .py está
REGRAS = PASTA_DO_SCRIPT.parent / "dados" / "regras_tolerancia.json"
```

`__file__` é o caminho do arquivo `.py` que está rodando; `resolve()` transforma em
caminho completo. Todos os exemplos deste módulo usam esse truque.

### Exemplo resolvido: quantas medições tem cada CSV?

Problema: na pasta de laudos, contar as linhas de dados de cada CSV (sem o cabeçalho)
para conferir se a exportação veio completa.

Primeiro eu separei em passos: listar os CSVs (filtro pelo `suffix`), ler cada um
(`read_text`), contar as linhas não vazias e descontar o cabeçalho. O arquivo pode vir
do Excel, então leio com `utf-8-sig` (seção 8).

```python
from pathlib import Path

pasta = Path("laudos") / "2025"
for arquivo in sorted(pasta.iterdir()):
    if arquivo.suffix.lower() != ".csv":
        continue
    linhas = [l for l in arquivo.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    print(f"{arquivo.name:<14} {max(len(linhas) - 1, 0):>3} medições")
```

Saída:

```text
linha_A.csv      1 medições
linha_B.csv      0 medições
linha_C.CSV      0 medições
```

(Os arquivos B e C foram criados vazios com `touch`; por isso o `max(..., 0)`.)

> 🔧 **Modifique:** mostre também o tamanho de cada arquivo em bytes, com
> `arquivo.stat().st_size`.

## 8. Encoding na prática: Excel, utf-8-sig e cp1252

No módulo 05 você viu os dois encodings do dia a dia e o BOM. Agora, com `try/except`,
a estratégia para ler um arquivo vindo do Excel fica direta:

```python
def ler_texto_excel(caminho):
    try:
        return caminho.read_text(encoding="utf-8-sig")   # UTF-8, com ou sem BOM
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252")      # o "ANSI" do Windows
```

Por que tentar UTF-8 primeiro? Porque ele é exigente: bytes cp1252 com acento quase
nunca formam UTF-8 válido, então o erro aparece e o plano B entra. O contrário não
funciona: cp1252 aceita quase qualquer byte e "lê" um arquivo UTF-8 sem erro nenhum,
só que cheio de `Ã§`.

E para **gravar** um CSV que o Excel em português abre certo com duplo clique, use
`encoding="utf-8-sig"`. O BOM avisa ao Excel que o arquivo é UTF-8. Sem ele, o Excel
supõe cp1252 e mostra `LiberaÃ§Ã£o`.

```text
Situação                                   Encoding
----------------------------------------   ----------------------------------------
Ler arquivo seu (JSON, log, txt)           "utf-8"
Ler CSV/TXT vindo do Excel ou do ERP       tente "utf-8-sig"; se falhar, "cp1252"
Gravar CSV para alguém abrir no Excel      "utf-8-sig"
Gravar JSON, log, txt                      "utf-8"
```

## 9. CSV no padrão do Excel brasileiro

CSV quer dizer "valores separados por vírgula". Mas no Brasil a vírgula é o separador
decimal, então o Excel em português usa **ponto e vírgula** (`;`) para separar as
colunas. Um CSV de medições exportado no laboratório fica assim:

```text
lote;linha;espessura;observacao
L001;A;25,4;COF: liberado
L002;A;27,9;"Selagem; refazer"
```

Repare na última linha: a observação tem um `;` dentro, então o Excel a colocou entre
aspas. É por isso que `split(";")` não serve para ler CSV:

```python
>>> 'L002;A;27,9;"Selagem; refazer"'.split(";")
['L002', 'A', '27,9', '"Selagem', ' refazer"']
```

O módulo `csv` da biblioteca padrão entende aspas, quebras de linha dentro de células e
outras regras do formato. Vamos criar o arquivo e ler com `csv.reader`:

```python
>>> import csv
>>> conteudo = 'lote;linha;espessura;observacao\nL001;A;25,4;COF: liberado\nL002;A;27,9;"Selagem; refazer"\n'
>>> Path("medicoes.csv").write_text(conteudo, encoding="utf-8-sig")
89
>>> with open("medicoes.csv", encoding="utf-8-sig", newline="") as arquivo:
...     for linha in csv.reader(arquivo, delimiter=";"):
...         print(linha)
...
['lote', 'linha', 'espessura', 'observacao']
['L001', 'A', '25,4', 'COF: liberado']
['L002', 'A', '27,9', 'Selagem; refazer']
```

Dois detalhes que não podem faltar: `delimiter=";"` (o padrão do módulo é vírgula) e
`newline=""` no `open` (a documentação do `csv` pede isso: o próprio módulo cuida das
quebras de linha).

### DictReader: cada linha vira um dicionário

```python
>>> with open("medicoes.csv", encoding="utf-8-sig", newline="") as arquivo:
...     linhas = list(csv.DictReader(arquivo, delimiter=";"))
...
>>> linhas[0]
{'lote': 'L001', 'linha': 'A', 'espessura': '25,4', 'observacao': 'COF: liberado'}
>>> [float(l["espessura"].replace(",", ".")) for l in linhas]
[25.4, 27.9]
```

A primeira linha do arquivo vira as chaves. Tudo chega como **texto**: a conversão do
número brasileiro é com você (módulo 05).

> 🔮 **Preveja antes de rodar:** o que acontece se você esquecer o `utf-8-sig` (usando
> `"utf-8"`) ou esquecer o `delimiter=";"`?
>
> ```python
> import csv
> with open("medicoes.csv", encoding="utf-8", newline="") as arquivo:
>     print(list(csv.DictReader(arquivo, delimiter=";"))[0]["lote"])
> ```

<details><summary>Resposta</summary>

`KeyError: 'lote'`. Lido com `"utf-8"`, o BOM fica grudado no primeiro nome de coluna,
que passa a ser `'\ufefflote'`. A chave `'lote'` não existe.

E sem o `delimiter=";"`, o `csv` procura vírgulas: a linha inteira do cabeçalho vira
**uma** chave só, `'lote;linha;espessura;observacao'`, e o `25,4` é partido no meio.
Os dois erros são clássicos com arquivos do Excel brasileiro.

</details>

### Gravando com DictWriter

Para gravar, diga as colunas (`fieldnames`), escreva o cabeçalho e depois as linhas. Os
números você formata com vírgula antes de gravar:

```python
import csv

resultado = [
    {"lote": "L001", "espessura": 25.4, "status": "APROVADO"},
    {"lote": "L002", "espessura": 27.9, "status": "REPROVADO"},
]
with open("resultado.csv", "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["lote", "espessura", "status"], delimiter=";")
    escritor.writeheader()
    for item in resultado:
        linha = dict(item)  # cópia, para não alterar a lista original
        linha["espessura"] = f"{item['espessura']:.2f}".replace(".", ",")
        escritor.writerow(linha)

print(open("resultado.csv", "rb").read())
```

Saída:

```text
b'\xef\xbb\xbflote;espessura;status\r\nL001;25,40;APROVADO\r\nL002;27,90;REPROVADO\r\n'
```

Os bytes mostram tudo o que importa: o BOM no começo, o `;`, a vírgula decimal e o fim
de linha `\r\n` (padrão do `csv` e do Windows). Com duplo clique, o Excel abre em
colunas e com os números à direita, prontos para somar.

> ⚠️ **Erro comum:** esquecer o `newline=""` ao gravar. No Windows, cada linha ganha um
> `\r` extra e o Excel mostra uma linha em branco entre cada registro.

### Exemplo resolvido: média de espessura por linha de produção

Problema: ler o CSV de medições e gravar um resumo com a média de cada linha (A, B...).

Primeiro eu pensei na estrutura: um dicionário `{linha: [valores]}` (módulo 03). Leio
com `DictReader`, converto o número, acumulo na lista da linha. No fim, calculo as
médias e gravo com `DictWriter`.

```python
import csv

conteudo = "lote;linha;espessura\nA-1;A;25,4\nA-2;A;26,0\nB-1;B;50,2\nB-2;B;49,4\n"
with open("medicoes2.csv", "w", encoding="utf-8-sig") as arquivo:
    arquivo.write(conteudo)

por_linha = {}
with open("medicoes2.csv", encoding="utf-8-sig", newline="") as arquivo:
    for registro in csv.DictReader(arquivo, delimiter=";"):
        valor = float(registro["espessura"].replace(".", "").replace(",", "."))
        por_linha.setdefault(registro["linha"], []).append(valor)

with open("medias.csv", "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.writer(arquivo, delimiter=";")
    escritor.writerow(["linha", "medicoes", "media"])
    for linha, valores in sorted(por_linha.items()):
        media = sum(valores) / len(valores)
        escritor.writerow([linha, len(valores), f"{media:.2f}".replace(".", ",")])

with open("medias.csv", encoding="utf-8-sig") as arquivo:
    print(arquivo.read(), end="")
```

Saída:

```text
linha;medicoes;media
A;2;25,70
B;2;49,80
```

`setdefault(chave, [])` devolve a lista da chave, criando uma vazia na primeira vez. É
o jeito curto de "agrupar" valores num dicionário. E `csv.writer` (sem o `Dict`) grava
listas em vez de dicionários.

<details><summary>Tente você: grave o arquivo `cof.csv` com as colunas lote e cof, para os lotes A-1 (0.215) e A-2 (0.3), com 3 casas e vírgula decimal, pronto para o Excel.</summary>

```python
import csv

dados = [("A-1", 0.215), ("A-2", 0.3)]
with open("cof.csv", "w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.writer(arquivo, delimiter=";")
    escritor.writerow(["lote", "cof"])
    for lote, cof in dados:
        escritor.writerow([lote, f"{cof:.3f}".replace(".", ",")])
```

O arquivo fica com as linhas `lote;cof`, `A-1;0,215` e `A-2;0,300`.

</details>

### CSV a partir de um texto já lido

Às vezes você já tem o conteúdo numa `str` (por exemplo, depois de decidir o encoding
com `try/except`). O `csv.reader` aceita qualquer lista de linhas:

```python
>>> texto = "lote;espessura\nA-1;25,4\n"
>>> list(csv.reader(texto.splitlines(), delimiter=";"))
[['lote', 'espessura'], ['A-1', '25,4']]
```

Só não funciona se alguma célula tiver quebra de linha dentro das aspas (raro em
planilhas de medição).

## 10. JSON: configurações e regras

JSON é o formato de texto mais usado para trocar dados entre programas (APIs web,
configurações, regras). Ele parece muito com dicionários e listas do Python:

```json
{
  "linha": "A",
  "espessura": {"nominal": 25.0, "tolerancia_pct": 10},
  "cof": [0.15, 0.30],
  "liberacao": "COF: liberado",
  "ativo": true,
  "observacao": null
}
```

```text
Python            JSON
---------------   ----------------------------
dict              objeto  {"chave": valor}
list, tuple       array   [1, 2, 3]
str               string  "texto" (só aspas DUPLAS)
int, float        number  25.4
True / False      true / false
None              null
```

O módulo `json` converte nos dois sentidos. `dumps`/`loads` trabalham com `str`;
`dump`/`load` (sem o "s") trabalham direto com arquivos.

```python
>>> import json
>>> regras = {"linha": "A", "cof": [0.15, 0.30], "liberacao": "COF: liberado", "ativo": True}
>>> texto = json.dumps(regras, ensure_ascii=False)
>>> texto
'{"linha": "A", "cof": [0.15, 0.3], "liberacao": "COF: liberado", "ativo": true}'
>>> json.loads(texto) == regras
True
>>> json.dumps({"obs": "Liberação"})
'{"obs": "Libera\\u00e7\\u00e3o"}'
>>> json.dumps({"obs": "Liberação"}, ensure_ascii=False)
'{"obs": "Liberação"}'
```

Por padrão, o `json` troca cada acento por um código (`\u00e7`). Funciona, mas fica
ilegível para quem abre o arquivo no Bloco de Notas. Use `ensure_ascii=False` (e grave
em UTF-8). Com `indent=2`, o arquivo fica indentado e fácil de editar à mão:

```python
>>> with open("regras.json", "w", encoding="utf-8") as arquivo:
...     json.dump(regras, arquivo, ensure_ascii=False, indent=2)
...
>>> print(Path("regras.json").read_text(encoding="utf-8"))
{
  "linha": "A",
  "cof": [
    0.15,
    0.3
  ],
  "liberacao": "COF: liberado",
  "ativo": true
}
>>> with open("regras.json", encoding="utf-8") as arquivo:
...     lidas = json.load(arquivo)
...
>>> lidas["cof"][1], lidas["ativo"]
(0.3, True)
```

Como o JSON pode trazer qualquer coisa, confira o tipo antes de usar:
`isinstance(dados, dict)` responde se `dados` é um dicionário (você verá `isinstance` a
fundo no módulo 08).

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import json
> dados = {"faixa": (0.15, 0.30), "linhas": {"A", "B"}}
> print(json.dumps(dados["faixa"]))
> print(json.dumps(dados))
> ```

<details><summary>Resposta</summary>

A primeira linha imprime `[0.15, 0.3]`: a tupla vira lista (JSON não tem tupla; ao ler
de volta, você recebe uma lista). A segunda dá
`TypeError: Object of type set is not JSON serializable`: conjuntos não existem em
JSON. Converta antes: `sorted(dados["linhas"])`.

</details>

### Quando o JSON está quebrado

Arquivo editado à mão quebra: aspas simples, vírgula esquecida. O `json` levanta
`json.JSONDecodeError` (uma filha de `ValueError`) dizendo linha e coluna:

```python
>>> json.loads("{'linha': 'A'}")
Traceback (most recent call last):
  ...
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
>>> try:
...     json.loads('{"casas": 3\n "pasta": "laudos"}')
... except json.JSONDecodeError as erro:
...     print("Erro na linha", erro.lineno, "->", erro.msg)
...
Erro na linha 2 -> Expecting ',' delimiter
```

Em programa de verdade, você captura esse erro e levanta um `ArquivoInvalido` com o nome
do arquivo e a linha, encadeado com `from erro` (é o exercício 10).

## 11. Leitura e escrita segura

Gravar arquivo parece simples até dar errado no meio. Três situações reais:

1. **Abrir em `"w"` apaga o arquivo na hora.** Se o erro acontece depois do `open` e
   antes do fim da gravação, o arquivo antigo já era e o novo ficou pela metade.
2. **O Excel tranca o arquivo.** No Windows, se `resultado.csv` está aberto no Excel,
   gravar nele dá `PermissionError: [Errno 13] Permission denied: 'resultado.csv'`.
3. **O programa cai** (energia, Ctrl+C, erro) no meio da gravação de um JSON de regras.
   No dia seguinte, o robô não consegue nem ler a configuração.

A técnica profissional é a **gravação atômica**: grave num arquivo temporário na mesma
pasta e, só quando tudo deu certo, troque pelo definitivo com `Path.replace`. A troca é
uma operação única: quem abrir o arquivo vê o antigo inteiro ou o novo inteiro, nunca
um pedaço.

```python
from pathlib import Path


def gravar_texto_seguro(caminho, texto):
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(texto, encoding="utf-8")   # se falhar, o original está intacto
    temporario.replace(caminho)                      # troca de uma vez


destino = Path("relatorio.txt")
gravar_texto_seguro(destino, "versão 1\n")
gravar_texto_seguro(destino, "versão 2\n")
print(destino.read_text(encoding="utf-8"), end="")
print(sorted(p.name for p in Path(".").glob("relatorio*")))
```

Saída:

```text
versão 2
['relatorio.txt']
```

Outras proteções baratas:

- **Valide e prepare tudo antes de abrir para gravar.** Gere o texto, a lista de
  linhas, o JSON; só depois abra o arquivo.
- **Modo `"x"`** quando o arquivo não pode ser sobrescrito (por exemplo, um certificado
  já emitido): se ele existir, dá `FileExistsError` em vez de apagar.
- **Mensagem útil para o `PermissionError`**: capture e diga "feche o arquivo no
  Excel", em vez de mostrar o traceback para o usuário.

## 12. Validação defensiva

Dados ruins devem ser barrados **na entrada**, perto de onde chegam, e não descobertos
três funções depois como um `TypeError` misterioso. Três regras práticas:

1. **Valide cedo, com cláusulas de guarda.** No começo da função, confira o que
   recebeu e saia com `raise` se não der para continuar (módulo 04: retorno antecipado).
2. **Mensagens com contexto.** Arquivo, linha, coluna e valor: `"linha 7: valor
   inválido em espessura: '2O,1'"`.
3. **Decida: parar ou continuar?** Se o problema invalida tudo (regras de tolerância
   corrompidas), pare. Se afeta só uma parte (um entre quatro arquivos de laudo), registre
   o problema e siga com o resto.

```text
                         um arquivo com problema
                                   │
              ┌────────────────────┴────────────────────┐
     o resto depende dele?                     os outros são independentes?
     (regras, configuração)                    (laudos de cada linha)
              │                                         │
        PARE com raise                    REGISTRE o erro e CONTINUE
        mensagem clara                    (try/except dentro do for)
```

### Exemplo resolvido: processar a pasta sem parar no primeiro erro

Problema: somar as espessuras de todos os CSVs da pasta. Se um arquivo estiver ruim,
ele fica de fora, o erro é anotado, e os outros são processados.

Primeiro eu separei o trabalho de **um** arquivo numa função que pode levantar erro.
Depois, no laço da pasta, coloquei o `try/except` em volta da chamada: o erro de um
arquivo fica preso naquela volta do `for`. E capturei só os tipos que eu sei explicar
(`KeyError` para coluna que falta, `ValueError` para número inválido).

```python
import csv
from pathlib import Path


def somar_espessuras(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        return sum(
            float(linha["espessura"].replace(",", "."))
            for linha in csv.DictReader(arquivo, delimiter=";")
        )


pasta = Path("lote_do_dia")
pasta.mkdir(exist_ok=True)
(pasta / "a.csv").write_text("lote;espessura\nA-1;25,4\nA-2;26,0\n", encoding="utf-8")
(pasta / "b.csv").write_text("lote;espessura\nB-1;abc\n", encoding="utf-8")
(pasta / "c.csv").write_text("lote;gramatura\nC-1;18,4\n", encoding="utf-8")

erros = {}
for caminho in sorted(pasta.glob("*.csv")):
    try:
        total = somar_espessuras(caminho)
    except KeyError as erro:
        erros[caminho.name] = f"falta a coluna {erro}"
    except ValueError as erro:
        erros[caminho.name] = f"valor inválido ({erro})"
    else:
        print(f"{caminho.name}: soma {total:.1f}")
print("Com problema:", erros)
```

Saída:

```text
a.csv: soma 51.4
Com problema: {'b.csv': "valor inválido (could not convert string to float: 'abc')", 'c.csv': "falta a coluna 'espessura'"}
```

O exercício 14 usa essa mesma ideia, com um detalhe a mais: o arquivo com erro precisa
ficar de fora **inteiro**, mesmo que as primeiras linhas estivessem certas.

## Lendo mensagens de erro deste módulo

- **`FileNotFoundError: [Errno 2] No such file or directory: 'dados/regras.json'`**: o
  caminho não existe **a partir da pasta onde você rodou o comando**. Confira com
  `Path("dados/regras.json").resolve()` onde o Python está procurando. Solução
  definitiva: `Path(__file__).resolve().parent` (seção 7).
- **`PermissionError: [Errno 13] Permission denied: 'resultado.csv'`**: no Windows,
  quase sempre o arquivo está aberto no Excel. Feche e rode de novo. Também acontece
  ao tentar abrir uma **pasta** como se fosse arquivo.
- **`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe7 in position 31`**:
  arquivo cp1252 lido como UTF-8. Use a estratégia da seção 8.
- **`KeyError: 'lote'`** ao ler um CSV: confira o BOM (use `utf-8-sig`), o
  `delimiter=";"` e espaços no nome da coluna (`" lote"`). Imprima
  `list(linha.keys())` para ver as chaves de verdade.
- **`json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes:
  line 1 column 2 (char 1)`**: JSON com aspas simples ou com vírgula sobrando depois do
  último item. JSON só aceita aspas duplas e não aceita vírgula no fim.
- **`TypeError: Object of type set is not JSON serializable`**: você tentou gravar algo
  que o JSON não conhece (set, Path, objetos). Converta antes (`sorted(conjunto)`,
  `str(caminho)`).
- **`ValueError: I/O operation on closed file.`**: usou o arquivo **depois** do bloco
  `with`, quando ele já foi fechado. Faça a leitura dentro do bloco.
- **`io.UnsupportedOperation: not writable`**: abriu em modo leitura (o padrão) e tentou
  gravar. Passe `"w"` ou `"a"`.
- **`FileExistsError: [Errno 17] File exists: 'certificado_L001.pdf'`**: o modo `"x"`
  (ou `mkdir` sem `exist_ok=True`) encontrou o arquivo ou a pasta já criados.
- **Traceback com "During handling of the above exception, another exception
  occurred"**: um erro aconteceu **dentro** do seu `except`. Confira o código do
  tratamento. (Se a frase for "was the direct cause of", foi um `raise ... from`
  proposital.)

## Boas práticas

- **Capture só o que sabe tratar**, com o tipo exato. Nada de `except:` sozinho.
- **`try` curto**: dentro dele, só as linhas que podem levantar o erro tratado.
- **Erros do domínio com nome do domínio**: `ArquivoInvalido`, `ValorForaDaTolerancia`,
  numa família com uma mãe (`ErroDeQualidade`).
- **Mensagem de erro com contexto**: arquivo, linha, coluna e valor.
- **`raise ... from erro`** ao trocar um erro técnico por um erro com mais contexto.
- **Sempre `with open(...)`** e **sempre `encoding=`** em arquivos de texto.
- **`pathlib` em vez de juntar texto** para montar caminhos; `Path(__file__)` para achar
  os arquivos do projeto.
- **CSV com o módulo `csv`**, nunca com `split(";")`; para o Excel brasileiro:
  `delimiter=";"`, vírgula decimal, `utf-8-sig` e `newline=""`.
- **JSON legível**: `ensure_ascii=False` e `indent=2`.
- **Grave de forma atômica** arquivos importantes (temporário + `replace`).
- **Em lote, um arquivo ruim não derruba os outros**: `try/except` dentro do `for`,
  erros registrados num dicionário ou num log.

## No mundo real

Fim do turno na linha A. O analista exporta as medições do Excel e precisa saber, antes
de liberar a expedição, quais lotes estão dentro da especificação. As regras de
tolerância ficam num JSON (`dados/regras_tolerancia.json`), uma entrada por linha de
produção: espessura e gramatura com tolerância sobre o nominal, COF com mínimo e máximo
fixos.

```json
"A": {
  "espessura": {"nominal": 25.0, "tolerancia_pct": 10},
  "gramatura": {"nominal": 23.0, "tolerancia_pct": 5},
  "cof": {"min": 0.15, "max": 0.3}
}
```

O programa abaixo junta o módulo inteiro: lê o CSV com o encoding certo, valida o
cabeçalho e os números (com mensagens que dizem a linha), carrega as regras do JSON,
confere cada lote e grava o resultado para o Excel.

```python
import csv
import json
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"
SAIDA = Path(__file__).resolve().parent / "saida"
ENSAIOS = ("espessura", "gramatura", "cof")


class ErroDeQualidade(Exception):
    """Base dos erros do sistema de qualidade."""


class ArquivoInvalido(ErroDeQualidade):
    """O arquivo existe, mas não está no formato esperado."""


def numero_br(texto):
    return float(texto.strip().replace(".", "").replace(",", "."))


def ler_texto_excel(caminho):
    try:
        return caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252")


def carregar_regras(caminho):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ArquivoInvalido(f"{caminho.name}: JSON inválido (linha {erro.lineno})") from erro


def faixa(regra):
    """Converte a regra do JSON em (mínimo, máximo): nominal ± % ou mín/máx fixos."""
    if "nominal" in regra:
        variacao = regra["nominal"] * regra["tolerancia_pct"] / 100
        return regra["nominal"] - variacao, regra["nominal"] + variacao
    return regra["min"], regra["max"]


def ler_medicoes(caminho):
    linhas = list(csv.reader(ler_texto_excel(caminho).splitlines(), delimiter=";"))
    if not linhas:
        raise ArquivoInvalido(f"{caminho.name}: arquivo vazio")
    cabecalho = [nome.strip().lower() for nome in linhas[0]]
    faltando = {"lote", "linha", *ENSAIOS} - set(cabecalho)
    if faltando:
        raise ArquivoInvalido(f"{caminho.name}: faltam as colunas {sorted(faltando)}")
    medicoes = []
    for numero, valores in enumerate(linhas[1:], start=2):
        registro = dict(zip(cabecalho, valores, strict=False))
        try:
            for ensaio in ENSAIOS:
                registro[ensaio] = numero_br(registro[ensaio])
        except ValueError as erro:
            raise ArquivoInvalido(f"{caminho.name}, linha {numero}: {erro}") from erro
        medicoes.append(registro)
    return medicoes


def conferir(medicao, regras_da_linha):
    problemas = []
    for ensaio in ENSAIOS:
        minimo, maximo = faixa(regras_da_linha[ensaio])
        if not minimo <= medicao[ensaio] <= maximo:
            problemas.append(
                f"{ensaio} {medicao[ensaio]} fora de [{minimo:.2f}, {maximo:.2f}]"
            )
    return problemas


def main():
    regras = carregar_regras(DADOS / "regras_tolerancia.json")
    medicoes = ler_medicoes(DADOS / "medicoes_linha_a.csv")
    SAIDA.mkdir(exist_ok=True)
    destino = SAIDA / "conferencia_linha_a.csv"
    with open(destino, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["lote", "status", "motivo"])
        for medicao in medicoes:
            problemas = conferir(medicao, regras[medicao["linha"]])
            status = "REPROVADO" if problemas else "APROVADO"
            escritor.writerow([medicao["lote"], status, "; ".join(problemas)])
            print(f"{medicao['lote']}: {status:<9} {'; '.join(problemas)}".rstrip())
    print(f"Resultado gravado em {destino.name}")


# Roda main() só quando o arquivo é executado diretamente (detalhes no módulo 07).
if __name__ == "__main__":
    main()
```

Resultado ao rodar `python 06-arquivos-e-erros/exemplos/09_conferencia_da_linha.py`:

```text
A-0153: APROVADO
A-0154: REPROVADO espessura 27.9 fora de [22.50, 27.50]
A-0155: REPROVADO gramatura 21.2 fora de [21.85, 24.15]; cof 0.33 fora de [0.15, 0.30]
Resultado gravado em conferencia_linha_a.csv
```

Repare nas decisões: as regras corrompidas **param** o programa (sem regra não há
conferência), com `ArquivoInvalido` dizendo a linha do JSON; o CSV é validado na
entrada; a função `faixa` esconde a diferença entre "nominal ± %" e "mín/máx"; e o
resultado sai num CSV que o pessoal da qualidade abre com duplo clique. O desafio deste
módulo leva isso para a pasta inteira, com as quatro linhas de produção.

## Resumo

| Tarefa | Como |
|---|---|
| Tratar um erro | `try: ... except ValueError as erro: ...` |
| Vários tipos | `except (KeyError, ValueError):` ou um `except` para cada |
| Só se não deu erro / sempre | `else:` / `finally:` |
| Levantar | `raise ValueError("mensagem com contexto")` |
| Encadear | `raise ArquivoInvalido("...") from erro` |
| Relançar o mesmo | `raise` sozinho, dentro do `except` |
| Exceção própria | `class ArquivoInvalido(ErroDeQualidade): """Docstring."""` |
| Ler texto | `with open(c, encoding="utf-8") as f: texto = f.read()` |
| Linha a linha | `for linha in f: linha.strip()` |
| Gravar / acrescentar | `open(c, "w", ...)` (apaga) / `open(c, "a", ...)` |
| Caminhos | `Path("dados") / "regras.json"`, `.name`, `.stem`, `.suffix`, `.parent` |
| Pastas | `mkdir(parents=True, exist_ok=True)`, `iterdir()`, `glob("*.csv")` |
| Atalhos | `read_text`, `write_text`, `read_bytes` (sempre com `encoding=` no texto) |
| Pasta do script | `Path(__file__).resolve().parent` |
| Arquivo do Excel | tente `"utf-8-sig"`; `except UnicodeDecodeError`: `"cp1252"` |
| Ler CSV BR | `csv.DictReader(f, delimiter=";")` com `open(..., newline="")` |
| Gravar CSV BR | `csv.DictWriter(f, fieldnames=..., delimiter=";")`, `"utf-8-sig"`, `newline=""` |
| JSON | `json.load(f)`, `json.dump(d, f, ensure_ascii=False, indent=2)` |
| JSON quebrado | `except json.JSONDecodeError as erro: erro.lineno` |
| Gravação segura | grava `nome.tmp` e depois `tmp.replace(destino)` |

## Você domina este módulo se...

- [ ] Leio um traceback de baixo para cima e digo em que linha do **meu** código está o
      problema.
- [ ] Explico sem consultar a diferença entre `except`, `else` e `finally`.
- [ ] Sei por que `except:` sozinho é perigoso e capturo só o tipo certo.
- [ ] Crio uma família de exceções próprias e uso `raise ... from erro`.
- [ ] Escolho o modo de abertura certo (`"r"`, `"w"`, `"a"`, `"x"`) e sei qual deles
      apaga o arquivo.
- [ ] Leio e gravo CSV no padrão do Excel brasileiro sem `KeyError` por causa do BOM e
      sem linhas em branco.
- [ ] Leio e gravo JSON com acentos legíveis e trato um JSON quebrado com mensagem
      clara.
- [ ] Processo uma pasta inteira sem que um arquivo ruim derrube os outros.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_ler_numero` | ★☆☆ | `try/except ValueError`, valor padrão |
| 02 | `ex02_conferir_tolerancia` | ★☆☆ | `raise` com exceção própria e `ValueError` |
| 03 | `ex03_ler_linhas` | ★☆☆ | `with open`, ler linha a linha, `encoding` |
| 04 | `ex04_registrar_evento` | ★☆☆ | modo `"a"`, `mkdir(parents=True)` |
| 05 | `ex05_listar_planilhas` | ★☆☆ | `pathlib`: `iterdir`, `suffix`, `is_file` |
| 06 | `ex06_ler_texto_excel` | ★★☆ | BOM, `UnicodeDecodeError`, fallback cp1252 |
| 07 | `ex07_ler_csv_br` | ★★☆ | `csv.DictReader` com `;` e vírgula decimal |
| 08 | `ex08_escrever_csv_br` | ★★☆ | `csv.DictWriter`, `utf-8-sig`, `newline=""` |
| 09 | `ex09_hierarquia_excecoes` | ★★☆ | criar exceções, capturar pela "mãe" |
| 10 | `ex10_carregar_config` | ★★☆ | JSON, `ArquivoInvalido`, `raise ... from` |
| 11 | `ex11_depurar_media` | ★★☆ | leitura de código: prever e consertar |
| 12 | `ex12_salvar_json_seguro` | ★★★ | gravação atômica, limpeza e `raise` |
| 13 | `ex13_revisao_ler_medicoes` | ★★★ | revisão: CSV validado + acentos e números BR (módulos 02, 03 e 05) |
| 14 | `ex14_revisao_conferir_pasta` | ★★★ | revisão: lote de arquivos + funções e contadores (módulos 02 a 05) |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 06 ex01
```

Os testes criam arquivos numa pasta temporária (`tmp_path` do pytest): nada é gravado
na sua pasta do curso. Para testar o módulo inteiro: `python curso.py testar 06`.

## Desafio do módulo

**Conferência de laudos em lote.** Um programa que lê os CSVs das quatro linhas de
produção em `dados/laudos/` (em encodings diferentes, um com número digitado errado e
outro sem uma coluna), aplica as regras de tolerância do JSON, respeita a observação de
liberação ("COF: liberado") e gera um CSV para o Excel, um resumo em JSON e um log de
erros, sem parar no primeiro problema. Enunciado completo em
[desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md).

## Para ir além

- Erros e exceções (tutorial oficial): https://docs.python.org/pt-br/3/tutorial/errors.html
- Hierarquia das exceções nativas:
  https://docs.python.org/pt-br/3/library/exceptions.html#exception-hierarchy
- Leitura e escrita de arquivos: https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files
- `pathlib`: https://docs.python.org/pt-br/3/library/pathlib.html
- `csv`: https://docs.python.org/pt-br/3/library/csv.html
- `json`: https://docs.python.org/pt-br/3/library/json.html
- Leitura extra: capítulos 9 e 10 (arquivos e pastas) do livro gratuito *Automate the
  Boring Stuff with Python*: https://automatetheboringstuff.com/2e/chapter9/
- Leitura extra: o verbete EAFP (o estilo "tentar e tratar") no glossário oficial:
  https://docs.python.org/pt-br/3/glossary.html#term-EAFP
