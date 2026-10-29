# Módulo 05 — Texto e expressões regulares

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 04 · **Nível:** iniciante → intermediário

## O que você vai aprender

- Fatiar, procurar e limpar textos com os métodos certos de `str`.
- Quebrar e juntar textos com `split`, `partition` e `join`.
- Montar relatórios alinhados com f-strings (largura, alinhamento, milhar, casas).
- Converter `"1.250,50"` em `1250.5` (e o caminho de volta) sem cair nas armadilhas.
- Remover acentos e comparar nomes de forma confiável com `unicodedata`.
- Explicar a diferença entre `str` e `bytes` e consertar o famoso `ExpediÃ§Ã£o`.
- Escrever uma expressão regular do zero, testando cada pedaço no REPL.
- Usar `re.search`, `re.match`, `re.fullmatch`, `re.findall`, `re.finditer` e `re.sub`.
- Extrair dados com grupos e grupos nomeados, e usar as flags `IGNORECASE`,
  `MULTILINE` e `VERBOSE`.
- Transformar o e-mail da expedição numa lista de pedidos com OP, NF e peso.

## Por que isso importa

Quase todo dado do mundo real chega como **texto**. O e-mail da expedição, a célula da
planilha com `25,4`, o código `op-004512`, o nome do cliente digitado de três jeitos.
Antes de calcular qualquer coisa, alguém precisa ler e limpar esse texto.

No mercado isso tem nome: *parsing* e *limpeza de dados*. É uma parte enorme do trabalho
de quem faz automação e análise de dados. E é exatamente o que separa um script que
"funciona no meu exemplo" de um que aguenta o e-mail real da segunda-feira.

No projeto final, este módulo é a peça que lê os pedidos da expedição (OP, NF e peso),
entende números brasileiros e reconhece a observação "COF: liberado".

> 💡 **Dica:** deixe o REPL aberto (`python` no PowerShell) e digite os exemplos junto
> com a aula. Texto se aprende testando.

## 1. Strings por dentro

Uma string é uma **sequência de caracteres**. Cada caractere tem uma posição (o índice),
que começa em 0. Índices negativos contam a partir do fim.

```text
texto:     O   P   -   0   0   4   5   1   2
índice:    0   1   2   3   4   5   6   7   8
negativo: -9  -8  -7  -6  -5  -4  -3  -2  -1
```

```python
>>> op = "OP-004512"
>>> op[0]
'O'
>>> op[-1]
'2'
>>> op[3:]
'004512'
>>> len(op)
9
```

O fatiamento é `texto[início:fim:passo]`. O `início` entra, o `fim` não entra. Sem
`início`, começa do zero; sem `fim`, vai até o final.

```python
>>> lote = "2025-A-0153"
>>> lote[:4]      # ano
'2025'
>>> lote[5]       # linha de produção
'A'
>>> lote[-4:]     # sequencial
'0153'
>>> lote[::-1]    # passo -1: de trás para frente
'3510-A-5202'
>>> lote[7:100]   # fatiar além do fim não dá erro
'0153'
```

Já um índice isolado fora da faixa (`lote[50]`) dá `IndexError`.

### Strings são imutáveis

Você não troca uma letra "dentro" de uma string. Todo método devolve uma string **nova**
e deixa a original como estava.

```python
>>> codigo = "op-004512"
>>> codigo[0] = "O"
Traceback (most recent call last):
  ...
TypeError: 'str' object does not support item assignment
>>> codigo.upper()
'OP-004512'
>>> codigo
'op-004512'
>>> codigo = codigo.upper()   # para guardar o resultado, reatribua
>>> codigo
'OP-004512'
```

> ⚠️ **Erro comum:** escrever `texto.strip()` sozinho numa linha e achar que `texto`
> mudou. Não mudou. Escreva `texto = texto.strip()`.

> 🔮 **Preveja antes de rodar:** anote o que cada `print` mostra. Depois rode.
>
> ```python
> nf = "000012345"
> print(nf[-5:])
> print(nf[::2])
> print(nf[20:])
> ```

<details><summary>Resposta</summary>

`12345`, depois `00135` e por fim uma linha vazia.

`nf[::2]` pega as posições 0, 2, 4, 6 e 8 (`0`, `0`, `1`, `3`, `5`). `nf[20:]` começa
depois do fim: o resultado é a string vazia `''`, sem erro.

</details>

## 2. Procurando dentro do texto

Antes de pensar em expressão regular, conheça as ferramentas simples. Elas resolvem a
maioria dos casos.

```python
>>> assunto = "Liberação de carga - OP 004512 - Cliente Plastifort"
>>> "OP" in assunto
True
>>> assunto.find("OP")      # posição da primeira ocorrência
21
>>> assunto.find("NF")      # -1 quando não encontra
-1
>>> assunto.count("a")
4
>>> assunto.startswith("Liberação")
True
>>> "LAUDO_0153.PDF".lower().endswith((".pdf", ".xlsx"))
True
```

`startswith` e `endswith` aceitam uma **tupla** de opções. Muito útil para extensões de
arquivo.

> 💡 **Dica:** use `in` quando só quer saber "tem ou não tem". Use `find` quando precisa
> da posição. Existe também `index`, que faz o mesmo que `find`, mas dá
> `ValueError: substring not found` quando não acha.

## 3. Limpando e padronizando

Texto digitado por gente tem espaço sobrando, maiúscula aleatória e prefixo repetido.
Estes são os métodos de limpeza do dia a dia:

```python
>>> bruto = "   embalagens   DO sul  ltda \n"
>>> bruto.strip()                  # tira espaços e quebras de linha das pontas
'embalagens   DO sul  ltda'
>>> "***ATENÇÃO***".strip("*")     # tira os caracteres indicados
'ATENÇÃO'
>>> "NF-e 12345".removeprefix("NF-e ")
'12345'
>>> "laudo_0153.pdf".removesuffix(".pdf")
'laudo_0153'
>>> "12345".zfill(9)               # completa com zeros à esquerda
'000012345'
>>> "cof ESTÁTICO".capitalize()    # só a primeira letra maiúscula
'Cof estático'
>>> "tração na ruptura".title()    # primeira letra de cada palavra
'Tração Na Ruptura'
>>> "Peso: 1.250,5 kg".replace(" kg", "")
'Peso: 1.250,5'
```

Para checar o conteúdo, existem os métodos `is...`: `"123456".isdigit()` dá `True`,
`"25,4".isdigit()` dá `False` (a vírgula não é dígito), `"OP".isalpha()` dá `True`.

> 🔮 **Preveja antes de rodar:** você quer tirar a extensão `.csv` do nome do arquivo.
>
> ```python
> print("laudos.csv".rstrip(".csv"))
> print("laudos.csv".removesuffix(".csv"))
> ```

<details><summary>Resposta</summary>

A primeira linha mostra `laudo` (sumiu o `s`!). A segunda mostra `laudos`.

`strip`, `lstrip` e `rstrip` recebem um **conjunto de caracteres**, não uma palavra.
`rstrip(".csv")` vai arrancando do fim qualquer `.`, `c`, `s` ou `v` que encontrar,
inclusive o `s` de "laudos". Para tirar um prefixo ou sufixo exato, use
`removeprefix` e `removesuffix` (Python 3.9+).

</details>

## 4. Quebrando e juntando: split, partition e join

`split` quebra a string numa **lista** de pedaços. Você escolhe o separador.

```python
>>> linha = "OP: 123456 | NF: 98765 | Peso: 1.250,5 kg"
>>> linha.split("|")
['OP: 123456 ', ' NF: 98765 ', ' Peso: 1.250,5 kg']
>>> [parte.strip() for parte in linha.split("|")]
['OP: 123456', 'NF: 98765', 'Peso: 1.250,5 kg']
>>> "Peso: 1.250,5 kg".split(":", maxsplit=1)
['Peso', ' 1.250,5 kg']
```

Sem argumento, `split()` é especial: quebra em **qualquer** espaço em branco (espaço,
tab, quebra de linha) e ignora repetições. Com `split(" ")`, cada espaço conta.

```python
>>> "  embalagens   DO sul\tltda ".split()
['embalagens', 'DO', 'sul', 'ltda']
>>> "  embalagens   DO".split(" ")
['', '', 'embalagens', '', '', 'DO']
```

`partition` quebra só na **primeira** ocorrência e sempre devolve 3 partes: antes,
separador, depois. Ótimo para "rótulo: valor", porque o valor pode ter `:` dentro.

```python
>>> "Horário: 14:30".partition(":")
('Horário', ':', ' 14:30')
>>> "sem separador".partition(":")
('sem separador', '', '')
```

`splitlines` quebra um texto em linhas, entendendo `\n` (Linux) e `\r\n` (Windows):

```python
>>> email = "Bom dia!\r\nSeguem as OPs.\nAtt."
>>> email.splitlines()
['Bom dia!', 'Seguem as OPs.', 'Att.']
```

`join` é o contrário de `split`: junta uma lista de strings usando um "cola".

```python
>>> "-".join(["2025", "03", "05"])
'2025-03-05'
>>> " ".join("  embalagens   DO sul\tltda ".split())   # truque: espaços normalizados
'embalagens DO sul ltda'
```

> ⚠️ **Erro comum:** `join` só aceita strings; com números dá `TypeError`. Converta
> antes: `", ".join(str(x) for x in valores)`. E o separador vem **antes** do ponto:
> `", ".join(lista)`, e não `lista.join(", ")`.

### Exemplo resolvido: padronizar o código de lote

Problema: o operador digita o lote de vários jeitos (`" 2025 a 153 "`, `"2025-a-153"`).
O padrão da empresa é `2025-A-0153` (ano, linha, sequencial com 4 dígitos).

Primeiro eu penso nos **pedaços**: ano, linha, sequencial. Se eu trocar o hífen por
espaço, consigo usar `split()` para separar os três, não importa quantos espaços
tenham. Depois eu formato cada pedaço e junto com `-`.

```python
>>> def padronizar_lote(texto):
...     ano, linha, seq = texto.replace("-", " ").split()
...     return "-".join([ano, linha.upper(), seq.zfill(4)])
...
>>> padronizar_lote(" 2025 a 153 ")
'2025-A-0153'
>>> padronizar_lote("2025-b-7")
'2025-B-0007'
```

Repare no desempacotamento `ano, linha, seq = ...` (módulo 03). Se o texto tiver mais ou
menos de 3 pedaços, ele dá `ValueError`. Por enquanto, isso é aceitável: dado errado não
deve passar em silêncio. No módulo 06 você aprende a tratar esse erro.

> 🔧 **Modifique:** faça a função aceitar também `/` como separador
> (`"2025/a/153"`). Uma linha a mais resolve.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> print("a,,b".split(","))
> print(len("OP 1 | OP 2 | OP 3".split("|")))
> print("-".join("ABC"))
> ```

<details><summary>Resposta</summary>

`['a', '', 'b']`, depois `3` e por fim `A-B-C`.

Duas vírgulas seguidas geram um pedaço vazio entre elas. E `join` aceita qualquer coisa
que dê para percorrer com `for`, inclusive uma string: ela é percorrida letra por letra.

</details>

## 5. Formatação avançada com f-strings

No módulo 01 você viu `f"{valor:.2f}"`. O que vem depois dos dois-pontos é uma pequena
linguagem de formatação. Ela controla largura, alinhamento, preenchimento, sinal, milhar
e casas decimais.

```text
f"{valor:*>12,.2f}"
         ││ │ │ │
         ││ │ │ └── .2f = número com 2 casas decimais
         ││ │ └──── ,   = separador de milhar
         ││ └────── 12  = largura mínima (em caracteres)
         │└──────── >   = alinhar à direita  (< esquerda, ^ centro)
         └───────── *   = caractere de preenchimento (opcional)
```

```python
>>> valor = 1250.5
>>> f"{valor:,.2f}"
'1,250.50'
>>> f"[{valor:12.1f}]"
'[      1250.5]'
>>> f"[{valor:*>12,.2f}]"
'[****1,250.50]'
>>> f"[{'OP':<6}]", f"[{'OP':>6}]", f"[{'OP':^6}]"
('[OP    ]', '[    OP]', '[  OP  ]')
>>> f"{42:06d}"           # inteiro com zeros à esquerda
'000042'
>>> f"{0.987:.1%}"        # porcentagem: multiplica por 100
'98.7%'
>>> f"{3.5:+.1f} / {-3.5:+.1f}"   # sinal sempre visível
'+3.5 / -3.5'
```

Números se alinham à direita por padrão; textos, à esquerda. Dois extras muito úteis
para depurar:

```python
>>> espessura = 25.4
>>> f"{espessura=}"       # mostra nome e valor
'espessura=25.4'
>>> cliente = "Plastifort "
>>> print(f"{cliente!r}")     # !r mostra as aspas: revela espaços escondidos
'Plastifort '
```

A largura também pode vir de uma variável. Coloque-a entre chaves dentro da
especificação:

```python
>>> largura = 10
>>> f"[{'COF':>{largura}}]"
'[       COF]'
>>> casas = 3
>>> f"{0.21:.{casas}f}"
'0.210'
```

### Exemplo resolvido: tabela alinhada de medições

Problema: imprimir as medições de um lote em colunas, para colar no e-mail.

Primeiro eu decido as larguras: o nome mais longo ("COF estático") tem 12 letras, então
uso 14 para sobrar espaço. Valores à direita, com 2 casas, em 8 caracteres. Depois eu
escrevo o cabeçalho com **as mesmas larguras** das linhas, senão nada alinha.

```python
medicoes = [
    ("Espessura", 25.4, "µm"),
    ("Gramatura", 23.1, "g/m²"),
    ("COF estático", 0.21, "-"),
]
print(f"{'Ensaio':<14}{'Valor':>8}  Unidade")
print("-" * 31)
for ensaio, valor, unidade in medicoes:
    print(f"{ensaio:<14}{valor:>8.2f}  {unidade}")
```

Saída:

```text
Ensaio           Valor  Unidade
-------------------------------
Espessura        25.40  µm
Gramatura        23.10  g/m²
COF estático      0.21  -
```

O exemplo completo está em `exemplos/02_formatacao.py`.

> 🔧 **Modifique:** acrescente uma coluna "Status" com `OK` centralizado em 8
> caracteres (`:^8`). E troque o `"-" * 31` por um cálculo que use as larguras.

## 6. Números no formato brasileiro

O Python só entende ponto como separador decimal. O texto brasileiro usa ponto para
milhar e vírgula para decimal.

```python
>>> float("1250.5")
1250.5
>>> float("1.250,5")
Traceback (most recent call last):
  ...
ValueError: could not convert string to float: '1.250,5'
```

Pior que o erro é o caso que **não** dá erro:

```python
>>> float("1.250")     # na expedição, isso é mil duzentos e cinquenta quilos!
1.25
```

Para o Python, `"1.250"` é um vírgula vinte e cinco. Uma carga de 1.250 kg viraria
1,25 kg sem nenhum aviso. Por isso, texto brasileiro **sempre** passa pela conversão.

A receita tem duas trocas, nesta ordem: primeiro some com os pontos de milhar, depois
troque a vírgula por ponto.

```python
>>> texto = " 1.250,5 "
>>> texto.strip().replace(".", "").replace(",", ".")
'1250.5'
>>> float(texto.strip().replace(".", "").replace(",", "."))
1250.5
```

> 🔮 **Preveja antes de rodar:** e se eu inverter a ordem das trocas?
>
> ```python
> texto = "1.250,5"
> print(texto.replace(",", ".").replace(".", ""))
> print(texto.replace(".", "").replace(",", "."))
> ```

<details><summary>Resposta</summary>

`12505` e `1250.5`. Na primeira linha, a vírgula vira ponto e logo depois **todos** os
pontos somem, inclusive o decimal que você acabou de criar. A ordem das operações
importa.

</details>

O caminho de volta (número → texto brasileiro) usa a formatação americana e depois troca
os símbolos. O truque é não trocar vírgula por ponto e ponto por vírgula "ao mesmo
tempo" com dois `replace` (um desfaria o outro). Use um caractere provisório:

```python
>>> americano = f"{1250.5:,.2f}"
>>> americano
'1,250.50'
>>> americano.replace(",", "_").replace(".", ",").replace("_", ".")
'1.250,50'
```

Também existe `str.maketrans` com `translate`, que troca vários caracteres de uma vez:

```python
>>> trocas = str.maketrans(",.", ".,")    # ',' vira '.', e '.' vira ','
>>> "1,250.50".translate(trocas)
'1.250,50'
```

> 💡 **Dica:** o módulo `locale` também formata no padrão do país, mas depende da
> configuração do computador. Para dados e automação, prefira a conversão explícita.

> ⚠️ **Erro comum:** converter o peso para BR **antes** de fazer as contas. Regra: texto
> brasileiro entra, vira `float` logo na leitura, todas as contas são feitas em `float`,
> e só na hora de mostrar ele volta a ser texto brasileiro.

```text
 "1.250,5"  ──br_para_float──▶  1250.5  ──contas──▶  2230.5  ──float_para_br──▶ "2.230,50"
  (entrada)                      (Python trabalha aqui)               (saída para gente)
```

## 7. Unicode e acentos

Cada caractere tem um número único no padrão **Unicode** (o *code point*). `ord("ç")`
dá `231`; `chr(231)` faz o caminho contrário e dá `'ç'`.

### Mesma aparência, strings diferentes

Um "ã" pode ser guardado de dois jeitos: como **um** caractere pronto, ou como "a" +
"til que se encaixa na letra anterior" (um caractere *combinante*). Com `print`, os
dois aparecem como "ã". Para o Python, são diferentes.

```python
>>> composto = "ã"
>>> decomposto = "a\u0303"     # 'a' + til combinante (U+0303)
>>> composto == decomposto
False
>>> len(composto), len(decomposto)
(1, 2)
>>> import unicodedata
>>> unicodedata.normalize("NFC", decomposto) == composto   # normalizando, ficam iguais
True
```

Isso aparece de verdade: nomes de arquivo vindos de Mac, texto copiado de PDF ou de
sites. A solução é **normalizar** as duas strings para a mesma forma antes de comparar.

```text
NFC  = forma composta    "ã" é 1 caractere           (padrão do Windows e da web)
NFD  = forma decomposta  "ã" é "a" + "◌̃"              (útil para remover acentos)
NFKC/NFKD = como acima, e ainda simplifica "parecidos": "²" vira "2", "ﬁ" vira "fi"
```

### Exemplo resolvido: remover acentos

Problema: comparar "Tração" com "TRACAO" e achar que são iguais.

Primeiro eu pensei em fazer um `replace` para cada letra acentuada. Seriam dezenas de
`replace`, e eu ia esquecer algum (e o "ü"? e o "ñ"?). Melhor usar a NFD: ela separa
cada letra do seu acento. Aí basta jogar fora os caracteres combinantes. Vamos ver o que
a NFD faz com "ção":

```python
>>> for c in unicodedata.normalize("NFD", "ção"):
...     print(f"U+{ord(c):04X}", unicodedata.name(c), unicodedata.combining(c))
...
U+0063 LATIN SMALL LETTER C 0
U+0327 COMBINING CEDILLA 202
U+0061 LATIN SMALL LETTER A 0
U+0303 COMBINING TILDE 230
U+006F LATIN SMALL LETTER O 0
```

`unicodedata.combining(c)` devolve 0 para letras normais e outro número para os
acentos. Então a regra é: fique só com os caracteres em que `combining` dá 0.

```python
>>> def remover_acentos(texto):
...     decomposto = unicodedata.normalize("NFD", texto)
...     return "".join([c for c in decomposto if not unicodedata.combining(c)])
...
>>> remover_acentos("Tração na ruptura - São Paulo")
'Tracao na ruptura - Sao Paulo'
>>> remover_acentos("Tração").upper() == "TRACAO"
True
```

### NFKD: quando "parecido" deve virar igual

Cabeçalho de planilha tem `g/m²`. Para criar um nome de coluna "limpo", você quer
`g/m2`. A NFD não mexe no "²"; a NFKD troca pelo "2" comum.

```python
>>> unicodedata.normalize("NFD", "g/m²")
'g/m²'
>>> unicodedata.normalize("NFKD", "g/m²")
'g/m2'
```

> ⚠️ **Erro comum:** existem **dois** "µ" no Unicode: o "sinal de micro" (U+00B5, o do
> teclado) e a letra grega "mi" (U+03BC). A NFKD troca o primeiro pelo segundo. Se o seu
> código procura `"µm"` depois de uma NFKD, não acha. Na dúvida, troque o `µ` por `u`
> **antes** de normalizar.

Para comparar ignorando maiúsculas, prefira `casefold()`: é um `lower()` feito para
comparação (trata casos especiais como o "ß" alemão, que vira "ss").

```python
>>> remover_acentos("JOÃO da Silva").casefold() == remover_acentos("joao DA SILVA").casefold()
True
```

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import unicodedata
> x = "café"
> y = unicodedata.normalize("NFD", x)
> print(x == y, len(x), len(y))
> print(unicodedata.normalize("NFC", y) == x)
> ```

<details><summary>Resposta</summary>

`False 4 5` e depois `True`.

A forma NFD guarda o "é" como "e" + acento agudo combinante: 5 caracteres. Na tela as
duas aparecem iguais. Normalizando de volta para NFC, ficam idênticas.

</details>

## 8. Encodings: o mistério do "ExpediÃ§Ã£o"

Até agora você trabalhou com `str`: texto "na cabeça" do Python. Mas no disco, no e-mail
e na rede só existem **bytes** (números de 0 a 255). O **encoding** é a tabela que diz
como cada caractere vira bytes.

Analogia: o texto é a mensagem; o encoding é o idioma em que ela foi escrita. Se quem
escreveu usou um idioma e quem leu usou outro, sai bobagem.

```python
>>> texto = "Expedição"
>>> texto.encode("utf-8")
b'Expedi\xc3\xa7\xc3\xa3o'
>>> texto.encode("cp1252")
b'Expedi\xe7\xe3o'
>>> len(texto), len(texto.encode("utf-8")), len(texto.encode("cp1252"))
(9, 11, 9)
```

`encode` vai de `str` para `bytes`; `decode` faz o contrário. O `b'...'` indica um
objeto `bytes`, e `\xe7` é um byte escrito em hexadecimal. Os dois encodings do seu dia
a dia:

```text
caractere   UTF-8       cp1252 (Windows-1252, "ANSI" no Bloco de Notas)
A           41          41
ç           C3 A7       E7
ã           C3 A3       E3
µ           C2 B5       B5
€           E2 82 AC    80
```

**UTF-8** é o padrão da web, do Python e dos arquivos modernos: qualquer caractere do
mundo, de 1 a 4 bytes. **cp1252** é o padrão antigo do Windows em português (parente do
`latin-1`): um byte por caractere. Sem acento, os dois coincidem. Por isso o problema só
aparece no primeiro "ç". E aparece de dois jeitos.

### Problema 1: bytes UTF-8 lidos como cp1252

```python
>>> dados = "Expedição".encode("utf-8")
>>> dados.decode("cp1252")
'ExpediÃ§Ã£o'
```

Cada letra acentuada vira **duas** letras estranhas (`Ã§`, `Ã£`, `Ã©`). Isso se chama
*mojibake*. Se o estrago já foi feito, desfaça o caminho:

```python
>>> "ExpediÃ§Ã£o".encode("cp1252").decode("utf-8")
'Expedição'
```

### Problema 2: bytes cp1252 lidos como UTF-8

```python
>>> dados = "Expedição".encode("cp1252")
>>> dados.decode("utf-8")
Traceback (most recent call last):
  ...
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe7 in position 6: invalid continuation byte
>>> dados.decode("utf-8", errors="replace")
'Expedi��o'
```

Leia a mensagem: o byte `0xe7` (o "ç" no cp1252) na posição 6 não é UTF-8 válido. Com
`errors="replace"`, o Python troca o que não entende pelo losango `�` (U+FFFD) em vez de
dar erro.

### Onde isso morde no laboratório

- Excel, **"CSV (separado por vírgulas)"**, no Windows em português: grava em
  **cp1252**. Lido como UTF-8, dá o Problema 2.
- Excel, **"CSV UTF-8"**: grava em UTF-8 **com BOM** (veja abaixo). Lido como cp1252
  por um programa antigo, dá o Problema 1.
- **Python no Windows**: sem `encoding=`, usa o padrão regional (normalmente cp1252). O
  Python 3.15 muda esse padrão para UTF-8 (PEP 686), mas você não controla em que versão
  seu código vai rodar. Regra de ouro: **sempre diga o encoding**.
- **Exportações do ERP e e-mails salvos como `.txt`**: podem vir em qualquer um dos dois.

> 💡 **Dica:** no VS Code, a barra inferior mostra o encoding do arquivo aberto ("UTF-8"
> ou "Windows 1252"). Clique nela e use "Reopen with Encoding" para testar. No Bloco de
> Notas, "Salvar como" mostra a codificação embaixo.

### O BOM do "CSV UTF-8"

O Excel coloca 3 bytes invisíveis no começo do arquivo UTF-8 (`EF BB BF`), o **BOM**.
Lido com `"utf-8"`, ele vira o caractere `\ufeff` grudado na primeira palavra. Lido com
`"utf-8-sig"`, ele some.

```python
>>> dados = "lote;espessura".encode("utf-8-sig")
>>> dados
b'\xef\xbb\xbflote;espessura'
>>> dados.decode("utf-8")
'\ufefflote;espessura'
>>> dados.decode("utf-8-sig")
'lote;espessura'
```

Com o BOM grudado, a primeira coluna se chama `'\ufefflote'`, e procurar por `'lote'`
falha. Você vai ver muito isso no módulo 06, com CSV.

### Exemplo resolvido: decodificar sem saber o encoding

Problema: os e-mails salvos pela expedição às vezes estão em UTF-8 e às vezes em cp1252.

Primeiro eu pensei: "UTF-8 é mais exigente". Bytes cp1252 com acento quase nunca formam
UTF-8 válido. Então eu tento UTF-8 com `errors="replace"`. Se aparecer o losango, não
era UTF-8, e eu decodifico como cp1252. Uso `"utf-8-sig"` para já sumir com o BOM.

```python
>>> def decodificar(dados):
...     texto = dados.decode("utf-8-sig", errors="replace")
...     if "\ufffd" in texto:    # apareceu o losango: não era UTF-8
...         texto = dados.decode("cp1252")
...     return texto
...
>>> decodificar("Expedição".encode("utf-8"))
'Expedição'
>>> decodificar("Expedição".encode("cp1252"))
'Expedição'
>>> decodificar("Expedição".encode("utf-8-sig"))
'Expedição'
```

No módulo 06 você vai ver um jeito mais direto com `try/except`.

Para ler um arquivo de verdade, uma prévia do módulo 06: `Path` (do módulo `pathlib`)
representa um caminho de arquivo. `Path("email.txt").read_bytes()` devolve os bytes
crus, e `Path("email.txt").read_text(encoding="utf-8")` já devolve a `str`. O arquivo
`exemplos/05_encodings.py` usa os dois com os e-mails da pasta `dados/emails/`.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> s = "µm"
> print(len(s), len(s.encode("utf-8")), len(s.encode("cp1252")))
> print(s.encode("utf-8").decode("cp1252"))
> ```

<details><summary>Resposta</summary>

`2 3 2` e depois `Âµm`.

O "µ" ocupa 2 bytes em UTF-8 (`C2 B5`) e 1 em cp1252 (`B5`). Lendo os bytes UTF-8 como
cp1252, o `C2` vira "Â" e o `B5` vira "µ". Por isso tanto relatório mostra "Âµm".

</details>

## 9. Expressões regulares: a ideia

Os métodos de string resolvem padrões **fixos**: "começa com OP", "tem um `|`". Mas o
e-mail real traz `OP 123456`, `op-123456`, `OP:123456`. Você precisa descrever a
**forma** do texto: "as letras OP, talvez um separador, e seis dígitos".

Uma **expressão regular** (regex) é uma minilinguagem para descrever formas de texto. O
módulo `re` da biblioteca padrão faz a busca.

```python
>>> import re
>>> re.search(r"\d+", "Peso: 980 kg")
<re.Match object; span=(6, 9), match='980'>
>>> print(re.search(r"\d+", "Sem números aqui"))
None
```

`re.search(padrão, texto)` procura a primeira ocorrência. Se acha, devolve um objeto
`Match` (com o trecho encontrado e a posição). Se não acha, devolve `None`.

### Por que o `r` antes das aspas?

Dentro de uma string normal, a barra invertida é especial: `"\n"` é **um** caractere
(quebra de linha). Regex usa muitas barras (`\d`, `\s`, `\b`). O `r` cria uma *raw
string*: a barra fica sendo só uma barra.

```python
>>> len("\n"), len(r"\n")
(1, 2)
```

> ⚠️ **Erro comum:** esquecer o `r`. `"\d"` até funciona por sorte, mas o Python 3.12+
> avisa `SyntaxWarning: invalid escape sequence '\d'`. E `"\b"` (que em regex significa
> "fronteira de palavra") vira o caractere de *backspace* e quebra o padrão sem avisar.
> **Regex sempre com `r"..."`.**

### As peças básicas

```text
Peça        Significa                                     Exemplo        Casa com
---------   -------------------------------------------   ------------   -----------
abc         o texto literal "abc"                         OP             OP
.           qualquer caractere (menos quebra de linha)     O.             OP, O-, O1
\d          um dígito (0 a 9)                             \d\d           45
\s          um espaço em branco (espaço, tab, \n)         OP\s1          OP 1
\w          letra, dígito ou _ (inclui letras com acento) \w+            Tração
[abc]       um caractere da lista                         [-:]           - ou :
[^abc]      um caractere FORA da lista                    [^|]+          tudo até o |
[0-9a-f]    faixa de caracteres                           [A-D]          A, B, C, D
?           o anterior 0 ou 1 vez (opcional)              kg?            k, kg
*           o anterior 0 ou mais vezes                    \s*            "", " ", "   "
+           o anterior 1 ou mais vezes                    \d+            7, 980, 1250
{n}         exatamente n vezes                            \d{6}          123456
{n,m}       de n a m vezes                                \d{1,3}        7, 98, 980
^   $       começo / fim do texto                         ^OP            OP no início
\b          fronteira de palavra                          \bOP\b         OP (não TOP)
a|b         a OU b                                        kg|t           kg, t
( )         grupo: junta peças e captura o trecho         (\d+)          (ver seção 12)
\. \| \(    o caractere literal (escapado)                \d+\.\d+       25.4
```

Não precisa decorar: volte nesta tabela sempre que precisar.

## 10. Construindo um padrão aos poucos

Ninguém escreve uma regex grande de uma vez. O método é:

1. Junte **exemplos reais**: os que devem casar e os que **não** devem.
2. Comece com o padrão mais simples possível.
3. Teste. Veja o que falhou. Ajuste **uma** peça. Teste de novo.

Para testar rápido, crie uma função de apoio no REPL. `re.fullmatch` responde: "o texto
**inteiro** tem essa forma?".

```python
>>> def testar(padrao, exemplos, flags=0):
...     for texto in exemplos:
...         casou = re.fullmatch(padrao, texto, flags)
...         print("✔" if casou else "✘", repr(texto))
...
>>> exemplos = ["OP 123456", "OP-123456", "OP123456", "op 123456",
...             "OP 12345", "OP 1234567", "OS 123456"]
```

Os quatro primeiros devem casar. Os três últimos, não (5 dígitos, 7 dígitos, "OS").

**Passo 1.** O mais simples: "OP", espaço, dígitos.

```python
>>> testar(r"OP \d+", exemplos)
✔ 'OP 123456'
✘ 'OP-123456'
✘ 'OP123456'
✘ 'op 123456'
✔ 'OP 12345'
✔ 'OP 1234567'
✘ 'OS 123456'
```

Dois problemas: casou números com 5 e 7 dígitos, e não aceitou hífen nem "op".

**Passo 2.** Exatamente 6 dígitos: `\d{6}`.

```python
>>> testar(r"OP \d{6}", exemplos)
✔ 'OP 123456'
✘ 'OP-123456'
✘ 'OP123456'
✘ 'op 123456'
✘ 'OP 12345'
✘ 'OP 1234567'
✘ 'OS 123456'
```

Os negativos agora estão certos. Faltam as variações.

**Passo 3.** O separador é "espaço ou hífen, ou nada": `[ -]?`.

```python
>>> testar(r"OP[ -]?\d{6}", exemplos)
✔ 'OP 123456'
✔ 'OP-123456'
✔ 'OP123456'
✘ 'op 123456'
✘ 'OP 12345'
✘ 'OP 1234567'
✘ 'OS 123456'
```

**Passo 4.** Ignorar maiúsculas e minúsculas: a flag `re.IGNORECASE`.

```python
>>> testar(r"OP[ -]?\d{6}", exemplos, re.IGNORECASE)
✔ 'OP 123456'
✔ 'OP-123456'
✔ 'OP123456'
✔ 'op 123456'
✘ 'OP 12345'
✘ 'OP 1234567'
✘ 'OS 123456'
```

Pronto: todos os ✔ e ✘ estão onde deveriam. Repare no processo: a cada passo, **um**
ajuste, e a lista inteira de exemplos é testada de novo. Assim você nunca conserta um
caso e quebra outro sem perceber.

> 💡 **Dica:** o site regex101.com (escolha "Python" no menu *Flavor*) mostra, peça por
> peça, o que o seu padrão está fazendo. Ótimo para depurar. Só não cole lá dados
> sigilosos da empresa.

> 🔧 **Modifique:** acrescente `"OP: 123456"` e `"OP - 123456"` aos exemplos e ajuste o
> padrão para aceitar dois-pontos e espaços em volta do hífen. Dica: `[\s:-]*`.

## 11. search, match, fullmatch, findall e finditer

Todas recebem `(padrão, texto)`. A diferença é **onde** procuram e **o que** devolvem.

```text
Função         Procura...                         Devolve
------------   --------------------------------   -----------------------------
re.search      em qualquer lugar (1ª ocorrência)   Match ou None
re.match       só no começo do texto              Match ou None
re.fullmatch   o texto inteiro                    Match ou None
re.findall     todas as ocorrências               lista de str (ou de tuplas)
re.finditer    todas as ocorrências               um Match de cada vez (for)
```

```python
>>> texto = "Liberar OP 123456 hoje"
>>> re.search(r"OP \d{6}", texto)
<re.Match object; span=(8, 17), match='OP 123456'>
>>> print(re.match(r"OP \d{6}", texto))
None
>>> print(re.fullmatch(r"OP \d{6}", texto))
None
>>> re.findall(r"\d{6}", "OPs 123456, 123457 e 123458")
['123456', '123457', '123458']
```

O objeto `Match` guarda o que foi encontrado:

```python
>>> achado = re.search(r"\d+", "Peso: 980 kg")
>>> achado.group()
'980'
>>> achado.start(), achado.end()
(6, 9)
```

`finditer` é o `findall` que entrega um `Match` de cada vez, num `for`. Use quando
precisa de mais do que o texto (posição, grupos). Você vai usá-lo na seção 15.

> ⚠️ **Erro comum:** encadear `.group()` direto no `search`. Se não achar, `search`
> devolve `None`, e `None.group()` quebra com
> `AttributeError: 'NoneType' object has no attribute 'group'`. Guarde numa variável e
> teste: `if achado:`.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import re
> texto = "OP 123456, OP 7654321, op 111111"
> print(re.findall(r"OP \d{6}", texto))
> ```

<details><summary>Resposta</summary>

`['OP 123456', 'OP 765432']`.

O "OP 7654321" tem 7 dígitos, mas `\d{6}` casa com os 6 primeiros e pronto: a regex não
sabe que tinha mais um dígito depois. E "op 111111" ficou de fora porque não usamos
`re.IGNORECASE`. A correção é exigir fronteira de palavra: `r"\bOP \d{6}\b"`. O `\b`
depois dos dígitos garante que não vem outro dígito colado.

</details>

## 12. Grupos e grupos nomeados

Achar o trecho é metade do trabalho. Quase sempre você quer só **uma parte** dele: o
número da OP, sem o "OP". Para isso servem os parênteses: eles **capturam** um pedaço.

```python
>>> achado = re.search(r"OP[ -]?(\d{6})", "Liberar OP-004512 hoje")
>>> achado.group(0)     # o trecho inteiro
'OP-004512'
>>> achado.group(1)     # só o que estava no 1º par de parênteses
'004512'
```

Com vários grupos, `groups()` devolve todos numa tupla:

```python
>>> linha = "Espessura: 25,4 µm"
>>> achado = re.fullmatch(r"(\w+): ([\d.,]+) (\S+)", linha)
>>> achado.groups()
('Espessura', '25,4', 'µm')
```

Contar parênteses fica confuso rápido. Dê **nomes** aos grupos com `(?P<nome>...)`:

```python
>>> padrao = r"(?P<ensaio>\w+): (?P<valor>[\d.,]+) (?P<unidade>\S+)"
>>> achado = re.fullmatch(padrao, linha)
>>> achado["valor"]
'25,4'
>>> achado.groupdict()
{'ensaio': 'Espessura', 'valor': '25,4', 'unidade': 'µm'}
```

`groupdict()` já devolve um dicionário, pronto para a sua "tabela" (lista de dicts).

### Grupos no findall

Quando o padrão tem **um** grupo, `findall` devolve só o conteúdo do grupo. Com
**vários**, devolve tuplas:

```python
>>> re.findall(r"OP (\d{6})", "OP 123456 e OP 654321")
['123456', '654321']
>>> re.findall(r"(OP|NF) (\d+)", "OP 123456 NF 98765")
[('OP', '123456'), ('NF', '98765')]
```

Às vezes você precisa de parênteses só para agrupar (por exemplo, numa alternativa), sem
capturar. Use `(?:...)`:

```python
>>> re.findall(r"(?:OP|NF) (\d+)", "OP 123456 NF 98765")
['123456', '98765']
```

### Guloso e preguiçoso

Os quantificadores `*` e `+` são **gulosos**: pegam o máximo que conseguirem. Colocando
`?` depois (`*?`, `+?`), viram **preguiçosos**: pegam o mínimo.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> import re
> obs = 'Obs: "COF liberado" e "Selagem ok"'
> print(re.findall(r'"(.*)"', obs))
> print(re.findall(r'"(.*?)"', obs))
> ```

<details><summary>Resposta</summary>

`['COF liberado" e "Selagem ok']` e depois `['COF liberado', 'Selagem ok']`.

O `.*` guloso vai da primeira aspa até a **última** aspa do texto. O `.*?` preguiçoso
para na primeira aspa que fecha. Uma alternativa sem `?` é dizer "qualquer coisa que
não seja aspa": `r'"([^"]*)"'`.

</details>

> 🔧 **Modifique:** o padrão com `\w+` para o ensaio falha em `"COF estático: 0,21"`
> (tem espaço no nome) e em `"Tração: 32 MPa"`? Teste os dois. Depois troque `\w+` por
> `[^:]+` ("tudo que não for dois-pontos") e veja o que muda.

## 13. Substituindo e dividindo: re.sub e re.split

`re.sub(padrão, troca, texto)` substitui **todas** as ocorrências.

```python
>>> re.sub(r"\s+", " ", "Embalagens    do   Sul\t Ltda")
'Embalagens do Sul Ltda'
>>> re.sub(r"\d", "#", "CPF 123.456.789-00")
'CPF ###.###.###-##'
```

Na troca, `\1`, `\2`... reaproveitam os grupos capturados. Com grupos nomeados, use
`\g<nome>`. Exemplo clássico: data brasileira para o formato ISO (ano-mês-dia), que
ordena certo no Excel e em qualquer sistema.

```python
>>> re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", "Produzido em 05/03/2025")
'Produzido em 2025-03-05'
>>> re.sub(r"(?P<d>\d{2})/(?P<m>\d{2})/(?P<a>\d{4})", r"\g<a>-\g<m>-\g<d>", "05/03/2025")
'2025-03-05'
```

E quando a troca depende de uma conta? Passe uma **função** no lugar do texto de troca.
O `re.sub` chama a função para cada ocorrência, entregando o `Match`, e usa o que ela
devolver (funções como valores: módulo 04).

```python
>>> def br_para_ponto(achado):
...     return achado.group().replace(",", ".")
...
>>> re.sub(r"\d+,\d+", br_para_ponto, "Espessura 25,4 e gramatura 23,1")
'Espessura 25.4 e gramatura 23.1'
>>> re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "3 bobinas e 12 caixas")
'6 bobinas e 24 caixas'
```

`re.split` quebra o texto onde o padrão casar. Bom quando há **vários** separadores
possíveis:

```python
>>> re.split(r"\s*[|;]\s*", "OP: 123456 | NF: 98765; Peso: 980 kg")
['OP: 123456', 'NF: 98765', 'Peso: 980 kg']
```

<details><summary>Tente você: troque cada "kg" (com ou sem espaço antes) por " quilos". Ex.: "980kg e 1.250 kg" → "980 quilos e 1.250 quilos".</summary>

```python
>>> re.sub(r"\s*kg\b", " quilos", "980kg e 1.250 kg")
'980 quilos e 1.250 quilos'
```

O `\s*` engole os espaços que existirem antes (zero ou mais), e a troca sempre coloca
exatamente um.

</details>

## 14. Flags e re.compile

Flags mudam o comportamento do padrão. As três que você mais vai usar:

- `re.IGNORECASE` (ou `re.I`): maiúsculas e minúsculas tanto faz.
- `re.MULTILINE` (ou `re.M`): `^` e `$` passam a valer para **cada linha**, e não só
  para o começo e o fim do texto todo.
- `re.VERBOSE` (ou `re.X`): espaços e quebras de linha no padrão são ignorados, e `#`
  começa um comentário. Permite escrever a regex "em pé", explicada.

```python
>>> re.findall(r"op \d{6}", "OP 123456 e op 654321", flags=re.IGNORECASE)
['OP 123456', 'op 654321']
>>> email = "Assunto: carga\nOP 123456\nobs: a OP 999999 saiu\nOP 654321"
>>> re.findall(r"^OP (\d{6})", email)
[]
>>> re.findall(r"^OP (\d{6})", email, flags=re.MULTILINE)
['123456', '654321']
```

Sem `MULTILINE`, `^` só casa no começo do texto inteiro (que começa com "Assunto").
Com ela, casa no começo de cada linha. A OP 999999 não está no começo da linha.

Para combinar flags, use `|`: `re.IGNORECASE | re.MULTILINE`.

Quando um padrão é usado muitas vezes, **compile** uma vez e guarde numa constante.
Junto com `VERBOSE`, fica legível como código comum:

```python
>>> PADRAO_OP = re.compile(
...     r"""
...     \b OP        # a sigla, como palavra inteira
...     [\s:-]*      # separador opcional: espaços, dois-pontos ou hífen
...     (\d{6})      # o número: exatamente 6 dígitos (grupo 1)
...     \b           # nada de dígito colado depois
...     """,
...     re.VERBOSE | re.IGNORECASE,
... )
>>> PADRAO_OP.findall("Liberar OP: 123456, op-654321 e a TOP 111111")
['123456', '654321']
```

> ⚠️ **Erro comum:** no modo `VERBOSE`, o espaço literal do padrão é **ignorado**. Para
> casar um espaço de verdade, use `\s`, `[ ]` ou `\ `.

## 15. Projeto guiado: lendo o e-mail da expedição

Hora de juntar tudo. Este é o e-mail padrão que a expedição manda ao laboratório:

```text
De: expedicao@plastifort.com.br
Assunto: Certificados - carga de 28/10

Bom dia, laboratório!

Favor emitir os certificados dos pedidos abaixo:

OP: 123456 | NF: 98765 | Peso: 1.250,5 kg
OP: 123457 | NF: 98766 | Peso: 980,0 kg
OP: 123458 | NF: 98767 | Peso: 2.040,75 kg

A OP 123459 vai na próxima carga.

Obrigado,
Expedição
```

Objetivo: uma lista de dicionários, um por pedido, com a OP, a NF e o peso em `float`.

### Passo 1: decompor o problema

```text
e-mail (str)
  └─▶ achar as linhas de pedido          (ignorar saudação, assinatura, "A OP 123459...")
        └─▶ em cada uma, extrair OP, NF, peso   (regex com grupos nomeados)
              └─▶ converter o peso "1.250,5" → 1250.5   (seção 6)
                    └─▶ juntar num dicionário e acumular numa lista
```

Repare: a linha "A OP 123459 vai na próxima carga" **tem** uma OP, mas não é um pedido.
Por isso o padrão não pode ser só "ache OPs": tem que descrever a **linha inteira** do
pedido.

### Passo 2: uma peça de cada vez, numa linha só

```python
>>> linha = "OP: 123456 | NF: 98765 | Peso: 1.250,5 kg"
>>> re.search(r"OP:\s*(\d{6})", linha).group(1)
'123456'
>>> re.search(r"NF:\s*(\d+)", linha).group(1)
'98765'
>>> re.search(r"Peso:\s*([\d.]+(?:,\d+)?)\s*kg", linha).group(1)
'1.250,5'
```

O peso é a peça mais difícil. Leia assim: `[\d.]+` são dígitos e pontos de milhar;
`(?:,\d+)?` é "uma vírgula com dígitos", opcional (o peso pode vir sem decimais, como
`980 kg`). Aqui eu uso `.group(1)` direto porque **acabei** de ver que a linha casa;
no código de verdade, teste o `None` antes.

### Passo 3: juntar as peças num padrão só

As peças já funcionam. Agora eu junto, com `VERBOSE` para comentar cada parte e grupos
nomeados para não contar parênteses.

```python
>>> PEDIDO = re.compile(
...     r"""
...     OP:   \s* (?P<op>\d{6})              # OP com 6 dígitos
...     \s* \| \s*                           # separador | (escapado!)
...     NF:   \s* (?P<nf>\d+)                # NF: só dígitos
...     \s* \| \s*
...     Peso: \s* (?P<peso>[\d.]+(?:,\d+)?)  # peso no formato brasileiro
...     \s* kg
...     """,
...     re.VERBOSE | re.IGNORECASE,
... )
>>> PEDIDO.search(linha).groupdict()
{'op': '123456', 'nf': '98765', 'peso': '1.250,5'}
```

> ⚠️ **Erro comum:** esquecer de escapar o `|`. Sem a barra, `|` significa "OU" e o
> padrão vira "OP... OU NF... OU Peso...". Ele passa a casar com pedaços soltos e os
> grupos vêm `None`. Todo caractere especial que você quer literal (`| . ( ) [ ] ? * +`)
> precisa de `\` na frente.

### Passo 4: o e-mail inteiro

`finditer` percorre todas as ocorrências do padrão no texto. Para cada uma, eu converto
o peso e monto o dicionário.

```python
>>> def ler_pedidos(email):
...     pedidos = []
...     for achado in PEDIDO.finditer(email):
...         peso = float(achado["peso"].replace(".", "").replace(",", "."))
...         pedidos.append({"op": achado["op"], "nf": achado["nf"], "peso_kg": peso})
...     return pedidos
...
>>> email = """Bom dia, laboratório!
... OP: 123456 | NF: 98765 | Peso: 1.250,5 kg
... OP: 123457 | NF: 98766 | Peso: 980,0 kg
... OP: 123458 | NF: 98767 | Peso: 2.040,75 kg
... A OP 123459 vai na próxima carga."""
>>> for pedido in ler_pedidos(email):
...     print(pedido)
...
{'op': '123456', 'nf': '98765', 'peso_kg': 1250.5}
{'op': '123457', 'nf': '98766', 'peso_kg': 980.0}
{'op': '123458', 'nf': '98767', 'peso_kg': 2040.75}
>>> sum(p["peso_kg"] for p in ler_pedidos(email))
4271.25
```

A linha "A OP 123459..." ficou de fora, como queríamos. O programa completo, com o
e-mail inteiro e um resumo formatado, está em `exemplos/08_email_expedicao.py`.

### Passo 5: quando não casa, como depurar

Na semana seguinte chega esta linha, e `ler_pedidos` devolve lista vazia para ela:

```text
OP: 123460 | NF: 98.768 | Peso: 500 kg
```

Não fique olhando para o padrão inteiro. **Corte ao meio** e teste os pedaços, do começo
para o fim, até achar o primeiro que falha:

```python
>>> problema = "OP: 123460 | NF: 98.768 | Peso: 500 kg"
>>> re.search(r"OP:\s*(\d{6})", problema) is not None
True
>>> re.search(r"OP:\s*(\d{6})\s*\|\s*NF:\s*(\d+)\s*\|", problema) is not None
False
>>> re.search(r"NF:\s*(\d+)", problema).group(1)
'98'
```

Achado: a NF veio com ponto de milhar (`98.768`), e `\d+` para no ponto. Agora é só
decidir a regra (aceitar `[\d.]+` e tirar os pontos depois) e testar de novo **todos**
os exemplos antigos. É exatamente isso que o exercício 12 pede, com mais variações.

## Lendo mensagens de erro deste módulo

- **`AttributeError: 'NoneType' object has no attribute 'group'`**: o `search` (ou
  `match`, `fullmatch`) não achou nada e devolveu `None`. Teste antes (`if achado:`) e
  depois descubra **por que** não casou (seção 15, passo 5).
- **`ValueError: could not convert string to float: '1.250,5'`**: texto brasileiro
  entrou direto no `float`. Converta antes (seção 6). Se aparece `'25,4 kg'` ou `''`,
  sobrou unidade ou a célula estava vazia.
- **`TypeError: 'str' object does not support item assignment`**: tentou mudar uma
  letra (`texto[0] = "X"`). Monte uma string nova: `"X" + texto[1:]`.
- **`TypeError: sequence item 1: expected str instance, int found`**: o `join` recebeu
  algo que não é string na posição 1. Converta com `str()` antes.
- **`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe7 in position 6`**: bytes
  cp1252 lidos como UTF-8. O `0xe7` é o "ç" do cp1252 (`0xe3` é "ã", `0xe9` é "é").
  Use `encoding="cp1252"` ou a estratégia da seção 8.
- **Texto com `Ã§`, `Ã£`, `Âµ`, sem erro nenhum**: UTF-8 lido como cp1252. Leia com
  `encoding="utf-8"`; se já veio estragado, `texto.encode("cp1252").decode("utf-8")`.
- **`SyntaxWarning: invalid escape sequence '\d'`**: faltou o `r` antes das aspas da
  regex. Escreva `r"\d+"`.
- **`re.error: missing ), unterminated subpattern at position 0`**: abriu parêntese no
  padrão e não fechou. Se queria um `(` literal, escape: `\(`. Parecidas:
  `unterminated character set` (`[` sem fechar) e `nothing to repeat` (um `*`, `+` ou
  `?` sem nada antes, como em `r"+55"`).

```text
>>> re.search(r"(OP \d+", "OP 123")
Traceback (most recent call last):
  ...
re.error: missing ), unterminated subpattern at position 0
```

No Python 3.13+, o nome aparece como `re.PatternError`. É o mesmo erro.

## Boas práticas

- **Métodos de string primeiro, regex depois.** Se `startswith`, `split` ou `in`
  resolvem, use. Regex é para quando a forma varia.
- **Regex sempre com `r"..."`.** Sem exceção.
- **Ancore quando validar.** Para "este texto É um código de OP", use `fullmatch` (ou
  `^...$`). Com `search`, "XYZOP 1234567" passaria.
- **Use `\b` em volta de números e siglas** para não casar pedaço de algo maior.
- **Padrões grandes: `re.compile` + `re.VERBOSE` + grupos nomeados**, numa constante
  com nome claro (`PADRAO_PEDIDO`). Seu "eu" de daqui a seis meses agradece.
- **Guarde exemplos reais** (positivos e negativos) e teste o padrão contra todos a cada
  mudança. No módulo 09 isso vira teste automatizado com `pytest.mark.parametrize`.
- **Converta na entrada, formate na saída.** Texto brasileiro vira `float` na leitura;
  volta a ser texto só na hora de mostrar.
- **Sempre diga o encoding** ao ler e gravar. Na dúvida sobre arquivos que vêm do Excel,
  tente `utf-8-sig` e caia para `cp1252`.
- **Normalize antes de comparar**: `strip`, `casefold`, remover acentos, espaços
  repetidos. Compare a versão normalizada, mas guarde a original para mostrar.

## No mundo real

Na planilha de resultados, a coluna "Observação" diz quais ensaios foram liberados. Cada
analista escreve de um jeito: `COF: liberado`, `cof liberado`, `Selagem - PENDENTE`,
`Tração: Liberada; COF: reprovado`. O robô dos certificados precisa transformar isso
num dicionário confiável e só emitir quando tudo estiver liberado.

O raciocínio:

1. Uma observação pode ter vários ensaios: quebro em `;` ou `,` (`re.split`).
2. Em cada pedaço, o formato é "ensaio, separador opcional (`:` ou `-`), status".
3. Normalizo tudo (sem acento, minúsculas) para comparar sem surpresas.
4. "liberado" e "liberada" contam igual: comparo só o começo da palavra (`liberad`).

```python
import re
import unicodedata

PADRAO_ITEM = re.compile(
    r"""
    (?P<ensaio>[a-z ]+?)   # nome do ensaio (já sem acento e minúsculo)
    \s* [:-]? \s*          # separador opcional
    (?P<status>[a-z]+)     # a palavra do status
    $
    """,
    re.VERBOSE,
)


def normalizar(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join([c for c in decomposto if not unicodedata.combining(c)])
    return " ".join(sem_acento.casefold().split())


def ler_liberacoes(observacao):
    resultado = {}
    for pedaco in re.split(r"[;,]", observacao):
        pedaco = normalizar(pedaco)
        achado = PADRAO_ITEM.match(pedaco)
        if not achado:
            continue
        status = "liberado" if achado["status"].startswith("liberad") else achado["status"]
        resultado[achado["ensaio"].strip()] = status
    return resultado


observacoes = [
    "COF: liberado",
    "cof LIBERADO",
    "Tração: Liberada; COF: reprovado",
    "Selagem - PENDENTE, cof: liberado",
]
for obs in observacoes:
    liberacoes = ler_liberacoes(obs)
    pode_emitir = all(s == "liberado" for s in liberacoes.values())
    print(f"{obs:<36} -> {liberacoes} | emitir? {'sim' if pode_emitir else 'não'}")
```

Saída:

```text
COF: liberado                        -> {'cof': 'liberado'} | emitir? sim
cof LIBERADO                         -> {'cof': 'liberado'} | emitir? sim
Tração: Liberada; COF: reprovado     -> {'tracao': 'liberado', 'cof': 'reprovado'} | emitir? não
Selagem - PENDENTE, cof: liberado    -> {'selagem': 'pendente', 'cof': 'liberado'} | emitir? não
```

Três escolhas de profissional: o padrão roda **depois** de normalizar (por isso basta
`[a-z ]`); pedaços que não casam são ignorados em vez de quebrar o programa; e
"liberada" vira "liberado". O arquivo está em `exemplos/09_liberacoes.py`.

## Resumo

| Tarefa | Como |
|---|---|
| Fatiar | `s[ini:fim]`, `s[-4:]`, `s[::-1]` |
| Procurar | `"x" in s`, `s.find("x")` (-1), `s.count("x")`, `s.startswith(("a", "b"))` |
| Limpar | `strip()`, `strip("*")`, `removeprefix`, `removesuffix`, `zfill(9)` |
| Caixa | `upper`, `lower`, `title`, `capitalize`, `casefold` (para comparar) |
| Quebrar e juntar | `split()`, `split(";", maxsplit=1)`, `partition(":")`, `splitlines()`, `"-".join(lista)` |
| Espaços repetidos | `" ".join(s.split())` |
| Formatar | `f"{v:>10,.2f}"`, `f"{t:<12}"`, `f"{n:06d}"`, `f"{p:.1%}"`, `f"{v=}"`, `f"{t!r}"` |
| BR → float | `float(s.strip().replace(".", "").replace(",", "."))` |
| float → BR | `f"{v:,.2f}".translate(str.maketrans(",.", ".,"))` |
| Remover acento | `normalize("NFD", s)` + descartar `unicodedata.combining(c)` |
| "²" → "2" | `unicodedata.normalize("NFKD", s)` |
| Encoding | `s.encode("utf-8")`, `b.decode("cp1252")`, `"utf-8-sig"` tira o BOM |
| Consertar "Ã§" | `s.encode("cp1252").decode("utf-8")` |
| Regex: achar 1 | `re.search(p, s)` → `Match` ou `None` |
| Regex: validar | `re.fullmatch(p, s)` |
| Regex: achar todos | `re.findall(p, s)` (lista), `re.finditer(p, s)` (Matches) |
| Grupos | `(...)`, `(?P<nome>...)`, `(?:...)`; `m.group(1)`, `m["nome"]`, `m.groupdict()` |
| Trocar | `re.sub(p, r"\2-\1", s)`, `re.sub(p, funcao, s)` |
| Dividir | `re.split(r"\s*[|;]\s*", s)` |
| Flags | `re.IGNORECASE`, `re.MULTILINE`, `re.VERBOSE`, combine com `\|` |
| Reusar | `PADRAO = re.compile(r"...", flags)` |

## Você domina este módulo se...

- [ ] Explico sem consultar a diferença entre `strip(".csv")` e `removesuffix(".csv")`.
- [ ] Converto `"1.250,5"` em `1250.5` e `1250.5` em `"1.250,50"`, e sei por que
      `float("1.250")` é perigoso.
- [ ] Monto uma tabela alinhada com f-strings sem tentativa e erro.
- [ ] Removo acentos com `unicodedata` e explico o que é NFD.
- [ ] Olho para `ExpediÃ§Ã£o` ou para um `UnicodeDecodeError` e digo qual encoding foi
      usado errado e como consertar.
- [ ] Explico a diferença entre `search`, `match`, `fullmatch` e `findall`.
- [ ] Construo uma regex aos poucos, testando contra exemplos que devem e que não devem
      casar.
- [ ] Extraio OP, NF e peso de um e-mail com grupos nomeados e converto o peso.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_limpar_nome` | ★☆☆ | `split`, `join`, `capitalize`, regras com `if` |
| 02 | `ex02_formatar_nf` | ★☆☆ | filtrar dígitos, `zfill`, fatiamento |
| 03 | `ex03_separar_campo` | ★☆☆ | `partition`, `strip`, tuplas |
| 04 | `ex04_br_para_float` | ★☆☆ | número brasileiro → `float` |
| 05 | `ex05_validar_op` | ★☆☆ | primeira regex: `fullmatch` e `IGNORECASE` |
| 06 | `ex06_float_para_br` | ★★☆ | formatação dinâmica, troca de símbolos |
| 07 | `ex07_normalizar_chave` | ★★☆ | `unicodedata` (NFKD), `re.sub` |
| 08 | `ex08_extrair_ops` | ★★☆ | `findall` com grupo, `\b`, sem repetir |
| 09 | `ex09_ler_medicao` | ★★☆ | grupos nomeados, `fullmatch`, `None` |
| 10 | `ex10_padronizar_datas` | ★★☆ | `re.sub` com função |
| 11 | `ex11_depurar_peso` | ★★☆ | leitura de código: prever e consertar |
| 12 | `ex12_ler_email_expedicao` | ★★★ | o parser da expedição, com variações reais |
| 13 | `ex13_revisao_tolerancias` | ★★★ | revisão: regex + dicionários + decisões (módulos 02 a 04) |
| 14 | `ex14_revisao_resumo` | ★★★ | revisão: formatação + `sorted` + acumuladores (módulos 01 a 03) |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 05 ex01
```

Para testar o módulo inteiro: `python curso.py testar 05`.

## Desafio do módulo

**Leitor de e-mails da expedição.** Um programa que lê todos os e-mails salvos em
`dados/emails/` (alguns em UTF-8, outros em cp1252), extrai os pedidos, aponta as linhas
suspeitas, padroniza o nome do cliente e imprime um resumo com o peso total no formato
brasileiro. Enunciado completo em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md).

## Para ir além

- Métodos de string: https://docs.python.org/pt-br/3/library/stdtypes.html#string-methods
- Formatação: https://docs.python.org/pt-br/3/library/string.html#formatspec
- HOWTO de expressões regulares (excelente): https://docs.python.org/pt-br/3/howto/regex.html
- Módulo `re`: https://docs.python.org/pt-br/3/library/re.html
- HOWTO de Unicode: https://docs.python.org/pt-br/3/howto/unicode.html
- Encodings disponíveis: https://docs.python.org/pt-br/3/library/codecs.html#standard-encodings
- Leitura extra: capítulo 7 (regex) do livro gratuito *Automate the Boring Stuff with
  Python*: https://automatetheboringstuff.com/2e/chapter7/
- Leitura extra: Joel Spolsky, "The Absolute Minimum Every Software Developer Must Know
  About Unicode": https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
- Praticar regex com explicação visual: https://regex101.com (*Flavor*: Python).
