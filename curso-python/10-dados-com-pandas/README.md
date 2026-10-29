# Módulo 10 — Análise de dados com pandas, Excel e gráficos

> **Tempo estimado:** 12 a 16 horas · **Pré-requisitos:** módulos 00 a 09 · **Nível:** intermediário

## O que você vai aprender

- Criar uma `Series` e um `DataFrame` e explicar a diferença entre os dois.
- Ler um CSV salvo pelo Excel brasileiro (`sep=";"`, `decimal=","`, `thousands="."`,
  `encoding`) sem perder o zero à esquerda da OP.
- Ler uma aba, várias abas ou todas as abas de uma planilha e juntar tudo numa tabela só.
- Inspecionar uma base nova com `shape`, `info`, `describe` e `value_counts`.
- Selecionar com colunas, `loc`, `iloc` e filtros booleanos (`&`, `|`, `~`, `isin`,
  `between`).
- Criar colunas calculadas sem laço `for` e alterar valores com `.loc` (sem cair na
  armadilha da atribuição encadeada).
- Limpar dados: texto, números em formato brasileiro, ausentes e duplicatas.
- Converter datas `dd/mm/aaaa`, extrair o mês e filtrar períodos.
- Resumir com `groupby`/`agg`, cruzar tabelas com `merge` e montar tabelas dinâmicas com
  `pivot_table`.
- Exportar CSV para o Excel brasileiro e Excel formatado (cabeçalho, largura, painel
  congelado, linhas reprovadas em vermelho).
- Desenhar gráficos de barras, linhas, histograma, dispersão e um gráfico de controle
  com média ± 3σ.
- Responder perguntas de carreira com 133 mil salários reais da área de dados.

## Por que isso importa

Você já faz análise de dados todo dia: no Excel. O pandas faz o mesmo trabalho, só que
**escrito**. Isso muda três coisas:

1. **Repetir é de graça.** O relatório do mês que vem é o mesmo script, rodado de novo.
2. **Escala.** O Excel engasga com 1 milhão de linhas; o pandas nem percebe.
3. **Rastreabilidade.** Cada passo da limpeza está no código. Num laboratório com
   auditoria, isso vale ouro.

No mercado, pandas e SQL (módulo 11) aparecem em praticamente toda vaga de analista de
dados, engenheiro de dados e automação. E no seu projeto final, é o pandas (ou o
openpyxl) que vai ler a planilha de valores com as abas das linhas A, B, C e D.

Lembra do seu script antigo, que lia o `salaries.csv` e contava diretores com um `for`?
No fim deste módulo você vai reescrevê-lo em uma linha e responder perguntas bem
melhores com o mesmo arquivo.

## 1. Preparando o terreno

O pandas já está no `requirements.txt` do curso, junto com o `openpyxl` (que o pandas
usa para ler e gravar `.xlsx`) e o `matplotlib` (gráficos). Com o ambiente virtual
ativado, na pasta `curso-python`:

```text
python -m pip install -r requirements.txt
python -c "import pandas, openpyxl, matplotlib; print(pandas.__version__)"
```

A convenção universal é importar assim:

```python
import pandas as pd
```

**Versões.** Este módulo funciona no pandas 2.2 e no 3.x. Onde a saída muda entre as
versões, o texto avisa. As duas diferenças que você vai ver:

- No pandas 3, colunas de texto têm o tipo `str`. No 2.2 aparecem como `object`.
- No pandas 3, o *copy-on-write* está sempre ligado: um filtro sempre se comporta como
  uma tabela nova (seção 7 explica o que isso muda na prática).

**Como rodar os exemplos.** Todos ficam em `exemplos/` e acham a pasta `dados/` sozinhos,
não importa de onde você rode. Na pasta `curso-python`:

```text
python 10-dados-com-pandas/exemplos/02_ler_csv_brasileiro.py
```

No REPL, use o caminho a partir de `curso-python`, por exemplo
`"10-dados-com-pandas/dados/medicoes.csv"`.

**Os dados da aula** (fictícios, mas com cara de laboratório) estão em `dados/`:

| Arquivo | O que é |
|---|---|
| `medicoes.csv` | 70 bobinas medidas: data, OP, linha, produto, espessura, gramatura, COF, peso |
| `medicoes_sujas.csv` | 10 linhas digitadas à mão, com todos os defeitos clássicos |
| `ops_protheus.csv` | OPs exportadas do ERP, em `cp1252` |
| `especificacoes.csv` | nominal, tolerância e COF máximo de cada produto |
| `planilha_linhas.xlsx` | a "planilha de valores": uma aba por linha de produção |
| `salarios_amostra.csv` | 600 linhas sorteadas do `salaries.csv`, para testes rápidos |

O script `dados/gerar_dados.py` recria todos eles (rode se apagar algum).

> 💡 **Dica:** para explorar dados, o Jupyter (ou os notebooks do VS Code) é ótimo: você
> roda um pedaço por vez e vê a tabela formatada. Instale com `python -m pip install
> notebook`. Mas o código que vai para produção mora em arquivos `.py`, com testes.

## 2. Series e DataFrame

Pense numa aba do Excel. Cada **coluna** é uma `Series`: uma sequência de valores do
mesmo tipo, com um rótulo para cada linha (o **índice**). A aba inteira é um
`DataFrame`: várias Series lado a lado, compartilhando o mesmo índice.

```text
DataFrame
            ┌─────────── Series ───────────┐
 índice     op       linha   espessura_um   peso_kg
   0      024412       A         40.2        1250.5
   1      024412       A         39.1         980.0
   2      024413       B         35.3        1310.2
```

Do arquivo `exemplos/01_series_e_dataframe.py`:

```python
import pandas as pd

espessuras = pd.Series([50.2, 49.1, 51.8, 47.9], name="espessura_um")
print(espessuras)
print("Média:", espessuras.mean())
print(espessuras - 50)
```

```text
0    50.2
1    49.1
2    51.8
3    47.9
Name: espessura_um, dtype: float64
Média: 49.75000000000001
0    0.2
1   -0.9
2    1.8
3   -2.1
Name: espessura_um, dtype: float64
```

Repare em `espessuras - 50`: a conta foi feita **em todos os valores de uma vez**, sem
`for`. Isso se chama **vetorização**, e é o coração do pandas. (O `49.75000000000001` é o
velho problema do float do módulo 01.)

Um DataFrame nasce de um dicionário de listas (cada chave vira uma coluna) ou de uma
lista de dicionários (a "tabela" do módulo 03):

```python
df = pd.DataFrame(
    {
        "op": ["024412", "024412", "024413", "024420"],
        "linha": ["A", "A", "B", "C"],
        "espessura_um": [40.2, 39.1, 35.3, 69.8],
        "peso_kg": [1250.5, 980.0, 1310.2, 845.7],
    }
)
print(df.shape)
print(df.dtypes)
print("Peso total:", df["peso_kg"].sum())
```

```text
(4, 4)
op                  str
linha               str
espessura_um    float64
peso_kg         float64
dtype: object
Peso total: 4386.4
```

`shape` é `(linhas, colunas)`. `dtypes` mostra o tipo de cada coluna (no pandas 2.2, as
colunas de texto aparecem como `object`). `df["peso_kg"]` devolve a coluna como Series.

> 🔮 **Preveja antes de rodar:** o que este código imprime?

```python
s = pd.Series([10, 20, 30])
print(s * 2)
print(s[s > 15])
```

<details><summary>Resposta</summary>

```text
0    20
1    40
2    60
dtype: int64
1    20
2    30
dtype: int64
```

`s * 2` multiplica cada valor. `s > 15` gera uma Series de `True/False`, e `s[...]` com
ela dentro devolve só os `True`. Repare que o índice original (1 e 2) é mantido: o
pandas não renumera sozinho.
</details>

> 🔧 **Modifique:** crie a Series com `index=["024412-01", "024412-02", "024412-03"]` e
> acesse um valor com `s["024412-02"]`. O índice pode ser texto, como uma chave de
> dicionário.

## 3. Lendo CSV brasileiro

O Excel em português salva CSV com **ponto e vírgula** separando colunas, **vírgula**
decimal e **ponto** de milhar. O começo do nosso `medicoes.csv`:

```text
data;op;linha;produto;bobina;espessura_um;gramatura_gm2;cof;peso_kg;observacao
03/07/2026;024412;A;PE-40;024412-01;38,1;35,3;0,21;1.558,5;
```

O `read_csv` espera o padrão americano (vírgula separa colunas). Leitura ingênua:

```python
ingenuo = pd.read_csv(DADOS / "medicoes.csv")
print("Leitura ingênua -> formato:", ingenuo.shape)
```

```text
Leitura ingênua -> formato: (70, 1)
```

Uma coluna só, com tudo grudado. A leitura correta (de `exemplos/02_ler_csv_brasileiro.py`):

```python
df = pd.read_csv(
    DADOS / "medicoes.csv",
    sep=";",  # separador de colunas
    decimal=",",  # vírgula decimal: 47,7 -> 47.7
    thousands=".",  # ponto de milhar: 1.558,5 -> 1558.5
    encoding="utf-8-sig",  # UTF-8 com BOM (o "CSV UTF-8" do Excel)
    dtype={"op": str},  # OP é código, não número: preserva o zero à esquerda
)
print(df[["op", "bobina", "espessura_um", "cof", "peso_kg"]].head())
```

```text
       op     bobina  espessura_um   cof  peso_kg
0  024412  024412-01          38.1  0.21   1558.5
1  024412  024412-02          36.4  0.24   1256.6
2  024412  024412-03          39.6  0.27    782.2
3  024413  024413-01          32.9  0.37    790.0
4  024413  024413-02          36.4  0.30   1632.5
```

Cada parâmetro resolve um problema:

| Parâmetro | Sem ele... |
|---|---|
| `sep=";"` | tudo vira uma coluna só |
| `decimal=","` | `38,1` fica como texto |
| `thousands="."` | `1.558,5` fica como texto |
| `encoding` | acentos viram lixo ou dá `UnicodeDecodeError` |
| `dtype={"op": str}` | `024412` vira o número `24412` |

> ⚠️ **Erro comum:** esquecer o `dtype` da OP. O pandas vê só dígitos e converte para
> número. Resultado do exemplo: `OP sem dtype: 24412 | OP com dtype: 024412`. Na hora de
> cruzar com o ERP (que guarda `"024412"`), nada casa. Código (OP, NF, CEP, CNPJ) é
> **texto**, mesmo que só tenha dígitos.

**Encoding.** Arquivos antigos do Windows (e muitas exportações de ERP) usam `cp1252`.
Ler como UTF-8 quebra no primeiro acento:

```text
Erro de encoding: 'utf-8' codec can't decode byte 0xe7 in position 56: invalid continuation byte
```

O byte `0xe7` é o `ç` de "Torrefação" em cp1252. A correção é dizer o encoding certo:

```python
ops = pd.read_csv(DADOS / "ops_protheus.csv", sep=";", decimal=",", thousands=".",
                  encoding="cp1252", dtype={"op": str})
print(ops[["op", "cliente", "quantidade_kg"]].head(4))
```

```text
       op                cliente  quantidade_kg
0  024412  Torrefação Serra Ltda         4500.0
1  024413  Laticínios Serra Azul         3500.0
2  024420        Agro Campo S.A.         4750.0
3  024421  Torrefação Serra Ltda         4750.0
```

| Como o arquivo foi salvo | `encoding=` |
|---|---|
| Excel: "CSV UTF-8 (delimitado por vírgulas)" | `"utf-8-sig"` |
| Excel: "CSV (separado por vírgulas)", ERPs antigos | `"cp1252"` (ou `"latin-1"`) |
| Sistemas modernos, Linux, APIs | `"utf-8"` |

> 💡 **Dica:** arquivo grande e desconhecido? Espie antes:
> `pd.read_csv(..., nrows=5)` lê só 5 linhas e `usecols=["op", "linha"]` só as colunas
> que você quer. Rápido e leve.

> 🔮 **Preveja antes de rodar:** você leu com `sep=";"` mas esqueceu `decimal=","`. Qual
> o tipo da coluna `espessura_um`, e o que acontece com `df["espessura_um"].mean()`?

<details><summary>Resposta</summary>

A coluna fica como **texto** (`str` no pandas 3, `object` no 2.2), porque `38,1` não é
número para o pandas. O `mean()` dá erro:

```text
TypeError: Cannot perform reduction 'mean' with string dtype
```

No pandas 2.2 a mensagem é outra (`TypeError: Could not convert string ...`), mas a causa
é a mesma. Moral: depois de ler, **sempre** confira `df.dtypes`.
</details>

## 4. Lendo Excel: uma aba, várias, todas

`pd.read_excel` lê `.xlsx` usando o openpyxl por baixo. Nossa planilha de valores tem uma
aba por linha de produção, e cada aba tem um **título na linha 1** e o cabeçalho só na
linha 2, como muita planilha feita à mão. O parâmetro `header=1` diz "o cabeçalho está
na linha de índice 1" (a segunda). De `exemplos/03_ler_excel_varias_abas.py`:

```python
PLANILHA = DADOS / "planilha_linhas.xlsx"
aba_a = pd.read_excel(PLANILHA, sheet_name="Linha A", header=1, dtype={"OP": str})
print(aba_a.columns.tolist())
```

```text
['OP', 'Bobina', 'Data', 'Espessura (µm)', 'Gramatura (g/m²)', 'COF', 'Peso (kg)', 'Observação']
```

Com `sheet_name=None`, o pandas lê **todas** as abas e devolve um **dicionário**
`{nome da aba: DataFrame}`:

```python
abas = pd.read_excel(PLANILHA, sheet_name=None, header=1, dtype={"OP": str})
print(type(abas))
for nome, tabela in abas.items():
    print(f"{nome}: {len(tabela)} linhas")
```

```text
<class 'dict'>
Linha A: 28 linhas
Linha B: 15 linhas
Linha C: 10 linhas
Linha D: 17 linhas
```

Para analisar, queremos **uma** tabela, com uma coluna dizendo de que linha veio cada
bobina. `assign` cria a coluna e `pd.concat` empilha as partes:

```python
partes = []
for nome, tabela in abas.items():
    partes.append(tabela.assign(linha=nome.removeprefix("Linha ")))
todas = pd.concat(partes, ignore_index=True)
print("Total:", todas.shape)
```

```text
Total: (70, 9)
```

`ignore_index=True` renumera 0, 1, 2... (sem ele, cada aba recomeçaria do 0). Por fim,
nomes com acento, espaço e unidade são chatos de digitar. Renomeie logo:

```python
todas = todas.rename(columns={"OP": "op", "Espessura (µm)": "espessura_um", ...})
```

As datas já chegam como datas (`datetime64`): o Excel guarda data como data, ao
contrário do CSV, que guarda texto.

> ⚠️ **Erro comum:** `header=1` vale para **todas** as abas. Se a planilha tiver uma aba
> "Instruções" com uma linha só, o `read_excel` falha com
> `ValueError: Passed header=[1], len of 1, but only 1 lines in file (sheet: Instruções)`.
> Solução: descubra os nomes antes com `pd.ExcelFile(caminho).sheet_names`, escolha as
> abas que interessam e passe a lista em `sheet_name=[...]`. É o exercício 05.

> ⚠️ **Erro comum (Windows):** `PermissionError: [Errno 13] Permission denied` ao ler ou
> gravar um `.xlsx` quase sempre é **o arquivo aberto no Excel**. Feche e rode de novo.

## 5. Inspecionando uma base nova

Antes de qualquer análise, faça o "exame de admissão" da tabela. Cinco comandos (de
`exemplos/04_inspecionar_e_selecionar.py`):

```python
print(df.shape)
df.info()
```

```text
(70, 10)
<class 'pandas.DataFrame'>
RangeIndex: 70 entries, 0 to 69
Data columns (total 10 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   data           70 non-null     str
 1   op             70 non-null     str
 2   linha          70 non-null     str
 3   produto        70 non-null     str
 4   bobina         70 non-null     str
 5   espessura_um   70 non-null     float64
 6   gramatura_gm2  70 non-null     float64
 7   cof            70 non-null     float64
 8   peso_kg        70 non-null     float64
 9   observacao     3 non-null      str
dtypes: float64(4), str(6)
memory usage: 5.6 KB
```

`info()` responde: quantas linhas, quais colunas, de que tipo e **quantos valores não
vazios** cada uma tem (`observacao` só tem 3 preenchidos). Depois:

```python
print(df[["espessura_um", "cof", "peso_kg"]].describe().round(2))
print(df["linha"].value_counts())
```

```text
       espessura_um    cof  peso_kg
count         70.00  70.00    70.00
mean          52.92   0.27  1216.03
std           16.74   0.06   242.50
min           32.10   0.13   782.20
25%           37.82   0.22  1027.70
50%           48.55   0.27  1220.00
75%           65.18   0.31  1393.88
max           94.40   0.44  1632.50
linha
A    28
D    17
B    15
C    10
Name: count, dtype: int64
```

O roteiro, para levar para a vida:

| Pergunta | Comando |
|---|---|
| Qual o tamanho? | `df.shape` |
| Que colunas e tipos? Tem vazio? | `df.info()` |
| Como são os números? | `df.describe()` |
| Quais categorias e quantas de cada? | `df["col"].value_counts()` |
| Quantos valores diferentes? | `df["col"].nunique()`, `df["col"].unique()` |

Olhe o `describe` com olho de laboratório: a espessura vai de 32,1 a 94,4 µm. Faz
sentido? Sim, porque há produtos de 35 a 90 µm misturados. Se aparecesse 940, seria
vírgula digitada errada. **Desconfiar dos dados é parte do trabalho.**

## 6. Selecionando linhas e colunas

| Quero... | Escreva | Devolve |
|---|---|---|
| uma coluna | `df["cof"]` | Series |
| várias colunas | `df[["op", "cof"]]` (lista dentro) | DataFrame |
| por rótulo | `df.loc[linhas, colunas]` | depende |
| por posição | `df.iloc[linhas, colunas]` | depende |
| por condição | `df[mascara]` | DataFrame |

```python
print(df.loc[0, "bobina"])
print(df.loc[0:2, ["bobina", "cof"]])
```

```text
024412-01
      bobina   cof
0  024412-01  0.21
1  024412-02  0.24
2  024412-03  0.27
```

> 🔮 **Preveja antes de rodar:** a tabela tem 4 linhas (índice 0 a 3). Quanto vale cada
> `len`?

```python
df = pd.DataFrame({"bobina": ["a", "b", "c", "d"], "cof": [0.21, 0.38, 0.27, 0.41]})
print(len(df.loc[0:2]), len(df.iloc[0:2]))
```

<details><summary>Resposta</summary>

```text
3 2
```

`loc` trabalha com **rótulos** e inclui o fim (0, 1 e 2). `iloc` trabalha com
**posições** e exclui o fim, igual ao fatiamento de listas do módulo 03 (0 e 1).
</details>

**Filtros booleanos.** Uma comparação com uma coluna gera uma **máscara** (Series de
`True/False`). Colocada dentro de `df[...]`, ela devolve só as linhas `True`:

```python
mascara = df["cof"] > 0.35
print("Bobinas com COF > 0,35:", mascara.sum())
print(df[mascara][["bobina", "linha", "cof", "observacao"]])
```

```text
Bobinas com COF > 0,35: 4
       bobina linha   cof     observacao
3   024413-01     B  0.37            NaN
14  024430-03     A  0.38  COF: liberado
36  024458-02     B  0.44            NaN
58  024483-04     A  0.37  COF: liberado
```

`mascara.sum()` conta os `True` (o Python trata `True` como 1). Para combinar condições,
use `&` (e), `|` (ou) e `~` (não), **com parênteses em cada condição**:

```python
linha_a_grossa = df[(df["linha"] == "A") & (df["espessura_um"] > 48)]
dentro = df["espessura_um"].between(57.66, 66.34)  # LAM-62: 62 µm ± 7%
print(df[(df["produto"] == "LAM-62") & ~dentro][["bobina", "espessura_um"]])
```

```text
       bobina  espessura_um
28  024447-03          67.5
43  024466-03          57.1
44  024466-04          56.9
```

Outros filtros úteis: `df["linha"].isin(["C", "D"])` ("está na lista?"),
`df["observacao"].notna()` ("está preenchido?"), `df["produto"].str.startswith("PE")`.
E o `loc` aceita máscara e colunas juntos: `df.loc[mascara, ["bobina", "cof"]]`.

> ⚠️ **Erro comum:** usar `and`/`or` do Python em vez de `&`/`|`:
> `df[df["linha"] == "A" and df["cof"] > 0.3]` dá
> `ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(),
> a.any() or a.all().` O `and` quer **um** True ou False; a máscara tem 70.

> 🔧 **Modifique:** no exemplo 04, liste as bobinas da linha B **ou** com COF acima de
> 0,40. Quantas são? (Resposta: 15, todas as da linha B; a única acima de 0,40 também é
> da B.)

## 7. Criando e alterando colunas

Coluna nova = atribuição com uma conta vetorizada (de `exemplos/05_criar_colunas.py`):

```python
df["desvio_pct"] = ((df["espessura_um"] - df["nominal_um"]) / df["nominal_um"] * 100).round(2)
df["status"] = "APROVADA"
df.loc[df["desvio_pct"].abs() > 7, "status"] = "REPROVADA"
print(df[["bobina", "desvio_pct", "status"]])
```

```text
      bobina  desvio_pct     status
0  024447-01       -0.32   APROVADA
1  024447-02       -5.00   APROVADA
2  024447-03        8.87  REPROVADA
3  024447-04        0.00   APROVADA
```

O padrão **"valor padrão + exceções"** é o jeito mais legível de criar colunas
condicionais: todo mundo começa `APROVADA` e o `.loc[mascara, "coluna"] = valor` troca só
onde a condição vale. Outras ferramentas:

| Quero | Use |
|---|---|
| traduzir códigos (`"A"` → `"Extrusora 1"`) | `df["col"].map(dicionario)` |
| faixas numéricas (leve/média/pesada) | `pd.cut(df["peso_kg"], bins=[...], labels=[...])` |
| apagar colunas | `df.drop(columns=[...])` |
| renomear | `df.rename(columns={"velho": "novo"})` |
| várias colunas novas sem mexer no original | `df.assign(nova=..., outra=...)` |

`drop`, `rename` e `assign` devolvem uma tabela **nova**. Guarde o resultado:
`df = df.drop(columns=["x"])`.

**Cópias e o copy-on-write.** Esta é a armadilha mais famosa do pandas.

> 🔮 **Preveja antes de rodar:** depois deste código, o status da bobina 02 é `"OK"` ou
> `"FORA"`?

```python
df = pd.DataFrame({"bobina": ["01", "02"], "cof": [0.25, 0.41], "status": ["OK", "OK"]})
df[df["cof"] > 0.35]["status"] = "FORA"
print(df)
```

<details><summary>Resposta</summary>

Continua `"OK"`, e o pandas avisa:

```text
ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series
through chained assignment.
...
  bobina   cof status
0     01  0.25     OK
1     02  0.41     OK
```

São **dois** colchetes seguidos (atribuição encadeada): o primeiro, `df[mascara]`, cria
uma tabela que se comporta como cópia; o segundo grava `"FORA"` nessa cópia, que é
jogada fora. No pandas 3 isso **nunca** funciona; no 2.2 o aviso se chama
`SettingWithCopyWarning` e o resultado também é `"OK"`. O jeito certo é **uma operação
só**, com `.loc`:

```python
df.loc[df["cof"] > 0.35, "status"] = "FORA"
```
</details>

Regras práticas que funcionam nas duas versões:

1. Para alterar valores, use sempre `df.loc[mascara, "coluna"] = valor`.
2. Filtrou e vai alterar o resultado? Faça `.copy()`:
   `reprovadas = df[df["status"] == "REPROVADA"].copy()`. Assim fica claro que é outra
   tabela, e o original não muda.
3. Função que recebe um DataFrame não altera o DataFrame de quem chamou: comece com
   `resultado = df.copy()` (efeito colateral, módulo 04).

## 8. Tipos, texto, ausentes e duplicatas

Dados digitados à mão chegam assim (`dados/medicoes_sujas.csv`, lido com `dtype=str` para
vermos tudo como foi digitado):

```text
         data      op linha     bobina espessura_um  peso_kg operador
0  01/09/2026  024470     A  024470-01         51,2  1.120,5   Marcos
1  01/09/2026  024470     a  024470-02         49,8  1.098,0  marcos
2  01/09/2026  024470     A  024470-02         49,8  1.098,0  marcos
3  02/09/2026  024470    A   024470-03          n/d  1.205,3   Marcos
4  04/09/2026  024474     c  024474-01         71,3    845,0    Júlia
5  04/09/2026  024474     C  024474-02          NaN    910,2    JÚLIA
6  04/09/2026  024474     C  024474-03         69,9      NaN    Júlia
7         NaN  024474     C  024474-04         70,1    877,7    Júlia
8  10/09/2026  024479     b  024479-01         35,4  1.310,0      Ana
9  10/09/2026  024479     B  024479-02        34,7   1.288,4      ana
```

Antes de limpar, faça o diagnóstico: `bruto["linha"].unique().tolist()` mostra
`['A', ' a', 'A ', 'c', 'C', 'b', 'B']` (sete "linhas" que na verdade são três), e
`bruto.isna().sum()` conta os vazios por coluna. `NaN` ("not a number") é como o pandas
marca um valor ausente.

**Exemplo resolvido: limpar passo a passo** (`exemplos/06_limpeza_tipos_ausentes.py`).
Primeiro eu listo os problemas, um por coluna. Depois resolvo um por vez, na ordem certa.

*Passo 1, texto.* Os métodos de string do módulo 05 existem para colunas inteiras, via
`.str`:

```python
df["linha"] = df["linha"].str.strip().str.upper()
df["operador"] = df["operador"].str.strip().str.title()
```

```text
['A', 'C', 'B'] ['Marcos', 'Júlia', 'Ana']
```

*Passo 2, números brasileiros guardados como texto.* A mesma receita do módulo 05: tira
o ponto de milhar, troca a vírgula por ponto, converte. `pd.to_numeric` converte a coluna
inteira; com `errors="coerce"`, o que não for número (como `"n/d"`) vira `NaN` em vez de
erro:

```python
df["peso_kg"] = pd.to_numeric(
    df["peso_kg"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
)
df["espessura_um"] = pd.to_numeric(
    df["espessura_um"].str.strip().str.replace(",", ".", regex=False), errors="coerce"
)
```

O `regex=False` diz que o `"."` é um ponto de verdade, não o "qualquer caractere" das
expressões regulares.

*Passo 3, duplicatas.* Só agora, com o texto padronizado, as linhas 1 e 2 ficaram
idênticas (antes, `" a"` e `"A"` eram diferentes):

```python
print("Linhas idênticas repetidas:", df.duplicated().sum())
print("Bobinas repetidas:", df.duplicated(subset=["bobina"]).sum())
df = df.drop_duplicates(subset=["bobina"], keep="first")
```

```text
Linhas idênticas repetidas: 1
Bobinas repetidas: 1
```

*Passo 4, ausentes: decida caso a caso.* Sem espessura não há o que avaliar: descarte.
Peso vazio não impede a análise da espessura: mantenha (aqui o exemplo preenche com 0
para mostrar o `fillna`, mas na vida real é melhor avisar alguém).

```python
df = df.dropna(subset=["espessura_um"])
df["peso_kg"] = df["peso_kg"].fillna(0)
df = df.reset_index(drop=True)
```

| Ferramenta | Para quê |
|---|---|
| `df.isna().sum()` | quantos vazios por coluna |
| `df.dropna(subset=[...])` | descartar linhas com vazio nessas colunas |
| `df["col"].fillna(valor)` | preencher vazios |
| `df.duplicated(subset=[...])` | máscara das repetições |
| `df.drop_duplicates(subset=[...], keep="first")` | descartar repetições |
| `df["col"].astype(int)` | converter quando você tem **certeza** de que tudo converte |
| `pd.to_numeric(..., errors="coerce")` | converter quando pode haver lixo |

> ⚠️ **Erro comum:** `pd.Series(["1", "n/d"]).astype(int)` dá
> `ValueError: invalid literal for int() with base 10: 'n/d'`. Com lixo possível, use
> `pd.to_numeric(..., errors="coerce")` e depois **conte** quantos viraram `NaN`: lixo
> demais é sinal de que o problema é outro (separador, encoding).

> 💡 **Dica:** `NaN` não entra nas contas. `pd.Series([1.0, None, 3.0]).mean()` dá `2.0`
> (média de 1 e 3), não 1.33. Às vezes é o que você quer; às vezes esconde um problema.

**Inteiro com vazio.** Uma coluna de inteiros com algum vazio vira `float` (2024 vira
`2024.0`), porque o `NaN` é um float. Se incomodar, `df["ano"].astype("Int64")` (com I
maiúsculo) usa o inteiro do pandas que aceita ausentes (`<NA>`). Você vai ver isso no
laboratório de salários.

## 9. Datas

No CSV, data é texto. Para fazer conta com data, converta com `pd.to_datetime` e **diga
o formato** (`exemplos/07_datas.py`):

```python
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
print("Depois:", df["data"].dtype, "| exemplo:", df.loc[0, "data"])
```

```text
Depois: datetime64[us] | exemplo: 2026-07-03 00:00:00
```

(No pandas 2.2 aparece `datetime64[ns]`: é só a precisão interna, não muda nada para
você.)

> 🔮 **Preveja antes de rodar:** que data sai daqui?

```python
print(pd.to_datetime(pd.Series(["03/07/2026"]))[0].date())
```

<details><summary>Resposta</summary>

```text
2026-03-07
```

**7 de março**, não 3 de julho! Sem `format`, o pandas assume o padrão americano
(mês/dia/ano). Num laudo, isso é um erro grave e silencioso. Use sempre
`format="%d/%m/%Y"` (ou, no mínimo, `dayfirst=True`).
</details>

Com a coluna convertida, o acessor `.dt` extrai as partes:

```python
df["mes"] = df["data"].dt.month
df["mes_ano"] = df["data"].dt.strftime("%m/%Y")
df["dia_semana"] = df["data"].dt.dayofweek  # 0 = segunda ... 6 = domingo
agosto = df[(df["data"] >= "2026-08-01") & (df["data"] <= "2026-08-31")]
print("Bobinas medidas em agosto:", len(agosto))
```

```text
Bobinas medidas em agosto: 19
```

Subtrair datas dá um intervalo (`Timedelta`); `.dt.days` tira o número de dias. O
exemplo 07 calcula quantos dias cada OP levou da emissão à primeira medição:

```text
       op    emissao       data  dias_ate_medir
0  024412 2026-07-02 2026-07-03               1
1  024413 2026-07-03 2026-07-05               2
```

E para agrupar por mês, `.dt.to_period("M")` transforma cada data no "mês dela":

```python
df["periodo"] = df["data"].dt.to_period("M")
print(df.groupby("periodo")["peso_kg"].sum())
```

```text
periodo
2026-07    33218.9
2026-08    22158.0
2026-09    29744.9
Freq: M, Name: peso_kg, dtype: float64
```

Data inválida (`"31/09/2026"`) com `format` dá `ValueError`. Se preferir marcar e seguir,
`errors="coerce"` troca por `NaT` (o `NaN` das datas).

> 💡 **Dica:** para usar o mês como **texto**, prefira `"%Y-%m"` (`"2026-07"`): ordena
> certo. Com `"%m/%Y"`, `"01/2027"` viria antes de `"12/2026"`.

## 10. Ordenando

```python
print(df.sort_values("peso_kg", ascending=False)[["bobina", "peso_kg"]].head(3))
print(df.nlargest(3, "cof")[["bobina", "cof"]])
```

```text
       bobina  peso_kg
4   024413-02   1632.5
30  024447-05   1614.2
64  024488-05   1601.5
       bobina   cof
36  024458-02  0.44
14  024430-03  0.38
3   024413-01  0.37
```

Várias chaves com direções diferentes:
`df.sort_values(["linha", "cof"], ascending=[True, False])` (linha crescente e, dentro
de cada linha, COF decrescente). `sort_index()` ordena pelo índice e
`reset_index(drop=True)` renumera depois de ordenar ou filtrar.

## 11. Agrupando: groupby e agg

`groupby` é a ferramenta que mais economiza seu tempo. A ideia tem nome: **separar,
aplicar, combinar**.

```text
 linha  peso_kg          separar         aplicar (sum)     combinar
   A     1558.5    ┌─ A: 1558.5, 1256.6 ─→  2815.1 ─┐
   A     1256.6 ───┤                                 ├─→  A 2815.1
   B      790.0    └─ B: 790.0           ─→   790.0 ─┘     B  790.0
```

De `exemplos/08_groupby_agg.py`:

```python
print(df.groupby("linha")["peso_kg"].sum())
```

```text
linha
A    33123.8
B    18543.5
C    12407.7
D    21046.8
Name: peso_kg, dtype: float64
```

Leia da esquerda para a direita: "agrupe por linha, pegue o peso, some". Para várias
estatísticas de uma vez, use `agg` com **agregação nomeada**:
`nome_da_coluna_nova=("coluna", "função")`.

```python
resumo = df.groupby("linha").agg(
    bobinas=("bobina", "count"),
    ops=("op", "nunique"),
    peso_total_kg=("peso_kg", "sum"),
    cof_medio=("cof", "mean"),
    cof_max=("cof", "max"),
)
print(resumo.round(3))
```

```text
       bobinas  ops  peso_total_kg  cof_medio  cof_max
linha
A           28    7        33123.8      0.292     0.38
B           15    4        18543.5      0.309     0.44
C           10    3        12407.7      0.219     0.34
D           17    4        21046.8      0.219     0.28
```

Funções mais usadas: `count`, `size`, `sum`, `mean`, `median`, `min`, `max`, `std`,
`nunique`, `first`. A chave do grupo vira o **índice**. Para tê-la como coluna normal (bom
para exportar), use `groupby("linha", as_index=False)` ou `.reset_index()` no fim. Duas
chaves: `groupby(["linha", "produto"])`.

**Exemplo resolvido: "qual linha tem mais COF alto, em %?"**

Primeiro eu penso na pergunta para **uma** linha: "das bobinas da linha A, que fração
tem COF acima de 0,30?". Isso é `contagem de True / total`, que é exatamente a **média**
de uma coluna `True/False`. Então eu crio a coluna e tiro a média por grupo:

```python
df["cof_alto"] = df["cof"] > 0.30
print((df.groupby("linha")["cof_alto"].mean() * 100).round(1))
```

```text
linha
A    35.7
B    46.7
C    10.0
D     0.0
Name: cof_alto, dtype: float64
```

Repare que a linha D aparece com 0.0. Se eu tivesse feito "filtrar os altos, contar por
linha e dividir pelo total", a D sumiria do primeiro resultado e a divisão daria `NaN`.
(Esse é um dos defeitos do exercício 07.)

> 🔮 **Preveja antes de rodar:** quais listas saem?

```python
t = pd.DataFrame({"linha": ["A", "A", "B"], "obs": ["COF: liberado", None, None]})
print(t.groupby("linha").size().tolist(), t.groupby("linha")["obs"].count().tolist())
```

<details><summary>Resposta</summary>

```text
[2, 1] [1, 0]
```

`size()` conta **linhas** do grupo. `count()` conta valores **não vazios** da coluna.
Para "quantas bobinas", use `size()` ou `count()` numa coluna sempre preenchida.
</details>

**transform** devolve um valor **por linha** (do tamanho da tabela original), em vez de
um por grupo. Serve para comparar cada item com o próprio grupo:

```python
df["media_da_op"] = df.groupby("op")["espessura_um"].transform("mean")
df["dif_da_op"] = (df["espessura_um"] - df["media_da_op"]).round(2)
```

```text
      bobina  espessura_um  media_da_op  dif_da_op
0  024412-01          38.1        38.03       0.07
1  024412-02          36.4        38.03      -1.63
```

> ⚠️ **Erro comum:** `df.groupby("linha").mean()` com colunas de texto na tabela dá
> `TypeError: dtype 'str' does not support operation 'mean'`. Escolha as colunas
> (`df.groupby("linha")[["cof", "peso_kg"]].mean()`) ou use `mean(numeric_only=True)`.

## 12. Juntando tabelas: merge e concat

`merge` é o PROCV (VLOOKUP) do pandas, só que melhor: junta tabelas por uma ou mais
colunas-chave. De `exemplos/09_merge.py`, medições + especificação de cada produto:

```python
com_spec = medicoes.merge(specs, on="produto", how="left", validate="many_to_one")
sem_spec = com_spec[com_spec["espessura_nominal"].isna()]
print("Produtos sem especificação:", sem_spec["produto"].unique().tolist())
```

```text
Produtos sem especificação: ['PE-90']
```

O `how` decide o que acontece com quem **não** casa:

```text
how="inner"  só o que existe nos dois lados (quem não casou SOME)
how="left"   tudo da esquerda; o que faltar da direita vira NaN
how="right"  tudo da direita
how="outer"  tudo dos dois lados
```

Para conferência de qualidade, quase sempre é `left`: **nenhuma medição pode sumir**.
Veja o perigo do `inner` cruzando medições com as OPs do ERP:

```python
inner = medicoes.merge(ops[["op", "cliente"]], on="op", how="inner")
print("Medições:", len(medicoes), "| depois do inner com OPs:", len(inner))
checagem = medicoes.merge(ops[["op", "cliente"]], on="op", how="left", indicator=True)
print(checagem["_merge"].value_counts())
```

```text
Medições: 70 | depois do inner com OPs: 65
_merge
both          65
left_only      5
right_only     0
Name: count, dtype: int64
```

Cinco bobinas sumiram em silêncio: são da OP 024499, medida mas não cadastrada no ERP.
O `indicator=True` cria a coluna `_merge`, que mostra de onde veio cada linha. Use-a
sempre que estiver em dúvida.

Mais três detalhes:

- `validate="many_to_one"` garante que a direita não tem chave repetida. Se a tabela de
  especificações tiver o mesmo produto duas vezes, o merge para com `MergeError` (um tipo
  de `ValueError`) em vez de **duplicar** medições sem avisar.
- Colunas com o mesmo nome dos dois lados ganham sufixos `_x` e `_y`. Escolha nomes
  melhores com `suffixes=("_medido", "_erp")`.
- Chaves com nomes diferentes: `left_on="op", right_on="numero_op"`.

`pd.concat([t1, t2], ignore_index=True)` é outra coisa: **empilha** tabelas com as mesmas
colunas (ex.: um CSV por mês, ou as abas da seção 4).

> ⚠️ **Erro comum:** chave com tipos diferentes. Se a OP é texto de um lado e número do
> outro: `ValueError: You are trying to merge on str and int64 columns for key 'op'.` (no
> 2.2: `object and int64`). Padronize antes, de preferência como texto.

## 13. Tabela dinâmica: pivot_table

A tabela dinâmica do Excel, em uma chamada (`exemplos/10_pivot_table.py`):

```python
df["mes"] = df["data"].dt.strftime("%Y-%m")
tabela = pd.pivot_table(
    df, index="linha", columns="mes", values="peso_kg", aggfunc="sum",
    fill_value=0, margins=True, margins_name="Total",
)
print(tabela.round(0))
```

```text
mes    2026-07  2026-08  2026-09    Total
linha
A      14393.0   3376.0  15355.0  33124.0
B      10292.0   3353.0   4898.0  18544.0
C       4274.0   4843.0   3291.0  12408.0
D       4260.0  10586.0   6201.0  21047.0
Total  33219.0  22158.0  29745.0  85122.0
```

| Excel (tabela dinâmica) | `pivot_table` |
|---|---|
| Linhas | `index=` |
| Colunas | `columns=` |
| Valores | `values=` |
| Resumir valores por (Soma, Média...) | `aggfunc=` |
| Mostrar itens sem dados (vazio → 0) | `fill_value=0` |
| Totais gerais | `margins=True` |

Para só **contar** combinações, `pd.crosstab(df["linha"], df["mes"])` é mais curto. E o
caminho inverso existe: uma planilha "larga" (um mês por coluna) vira "longa" (uma linha
por linha+mês) com `melt`, o formato que o pandas prefere para agrupar e plotar:

```python
longa = larga.melt(id_vars="linha", var_name="mes", value_name="toneladas")
```

```text
  linha   jul   ago   set            linha  mes  toneladas
0     A  33.2  22.1  29.7    ──→   0     A  jul       33.2
1     B  18.5  12.0  15.3          1     B  jul       18.5
                                    2     A  ago       22.1  ...
```

## 14. Vetorização x apply x laço for

O seu script antigo contava diretores assim:

```python
diretores = 0
for i in df["job_title"]:
    if i == "Director":
        diretores += 1
```

Funciona, mas é Python puro passando por 133 mil valores, um de cada vez. O jeito pandas
é uma linha: `(df["job_title"] == "Director").sum()`. O exemplo 11 mede os dois (e o
`apply`, que chama uma função Python para cada valor). Na máquina em que esta aula foi
escrita:

```text
133.349 linhas
Resultados iguais? True -> 322
for:            34.45 ms
apply:          14.76 ms
vetorizado:      6.69 ms
Iguais? True
apply: 25.68 ms | vetorizado: 0.64 ms
```

Com texto, a diferença é de 5 vezes; com números (a segunda medição, dividir o salário
por 1000), passa de **40 vezes**. Os seus números vão ser outros, mas a ordem se mantém.

A regra:

1. **Primeiro** procure a operação vetorizada: aritmética com colunas, comparações,
   `.str`, `.dt`, `.map(dicionario)`, `.loc` com máscara, `groupby`.
2. Se a lógica for complicada demais para isso, `apply` com uma função sua é aceitável.
3. `for` em linhas de DataFrame (`iterrows`) é o último recurso, para coisas que não são
   conta (ex.: gerar um certificado por linha).

## 15. Exportando: CSV e Excel formatado

**CSV para o Excel brasileiro abrir certinho** (separador, vírgula decimal e BOM):

```python
df.to_csv("saida.csv", sep=";", decimal=",", index=False, encoding="utf-8-sig")
```

`index=False` evita uma primeira coluna com 0, 1, 2... que ninguém pediu.

**Excel com várias abas:** um `pd.ExcelWriter` e vários `to_excel`. E dá para
**formatar** com o openpyxl, dentro do mesmo `with`, porque `escritor.sheets[nome]` é a
aba do openpyxl. O núcleo de `exemplos/12_exportar_excel_formatado.py`:

```python
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

with pd.ExcelWriter(caminho, engine="openpyxl") as escritor:
    resumo.to_excel(escritor, sheet_name="Resumo", index=False)
    df.to_excel(escritor, sheet_name="Medições", index=False)

    aba = escritor.sheets["Medições"]
    for celula in aba[1]:  # linha 1 = cabeçalho
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill("solid", fgColor="1F4E78")
    for i, coluna in enumerate(df.columns, start=1):
        maior = max(len(str(coluna)), *(len(str(v)) for v in df[coluna]))
        aba.column_dimensions[get_column_letter(i)].width = min(maior + 2, 40)
    aba.freeze_panes = "A2"  # congela o cabeçalho
    aba.auto_filter.ref = aba.dimensions  # liga o filtro do Excel

    col_status = df.columns.get_loc("status")  # posição da coluna (0, 1, 2...)
    for linha in aba.iter_rows(min_row=2):
        if linha[col_status].value == "REPROVADA":
            for celula in linha:
                celula.fill = PatternFill("solid", fgColor="FFC7CE")
# ao sair do with, o arquivo é salvo
```

O exemplo completo ainda pinta de amarelo as bobinas com COF fora mas liberadas
("COF: liberado") e formata números (`number_format = "0.000"`). Abra o
`saida/relatorio_cof.xlsx` gerado e confira. O módulo 12 aprofunda o openpyxl.

```text
status
APROVADA             62
SEM ESPECIFICAÇÃO     5
LIBERADA              2
REPROVADA             1
Name: count, dtype: int64
```

> 💡 **Dica:** produto sem especificação **não** é aprovado. No exemplo, o `cof_max` dele
> é `NaN`, e `cof > NaN` dá `False`: sem a linha que marca `SEM ESPECIFICAÇÃO`, essas
> bobinas sairiam "APROVADAS" sem regra nenhuma. Sempre trate o "não sei" explicitamente.

## 16. Gráficos com matplotlib

Um gráfico bom responde **uma** pergunta. Escolha o tipo pela pergunta:

| Pergunta | Gráfico | Exemplo |
|---|---|---|
| Comparar categorias | barras | peso por linha |
| Evolução no tempo | linhas | peso por semana |
| Como os valores se espalham? | histograma | espessuras do LAM-62 |
| Duas medidas andam juntas? | dispersão | espessura x gramatura |
| O processo está estável? | gráfico de controle | seção 17 |

O matplotlib desenha numa **Figure** (a folha) que contém um ou mais **Axes** (cada
gráfico, com seus eixos, título e rótulos). Quase tudo que você configura é método do
Axes: `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.legend`.

```text
┌──────────── Figure ────────────┐
│  ┌───────── Axes ───────────┐  │
│  │  título                  │  │
│  │  ▇▇   ▇▇                 │  │
│  │  ▇▇   ▇▇   ▇▇            │  │
│  └──────────────────────────┘  │
│        rótulo do eixo x        │
└────────────────────────────────┘
```

Há dois jeitos de desenhar, e eles se misturam bem (`exemplos/13_graficos.py`):

**1) Pelo pandas:** `Series.plot` e `DataFrame.plot` desenham com o matplotlib e
**devolvem o Axes**.

```python
peso_t = df.groupby("linha")["peso_kg"].sum() / 1000
ax = peso_t.plot.bar(color="#1F4E78", rot=0)
ax.set_title("Peso medido por linha (jul–set/2026)")
ax.set_xlabel("Linha")
ax.set_ylabel("Peso (t)")
ax.figure.tight_layout()
ax.figure.savefig(SAIDA / "barras_peso_por_linha.png", dpi=120)
print("Barras desenhadas:", len(ax.patches))
```

```text
Barras desenhadas: 4
```

**2) Pelo pyplot:** você cria a figura e o Axes e chama os métodos de desenho.

```python
import matplotlib.pyplot as plt

semanal = df.set_index("data").resample("W")["peso_kg"].sum() / 1000
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(semanal.index, semanal.values, marker="o")
ax.set_title("Peso medido por semana")
fig.autofmt_xdate()  # inclina as datas
fig.savefig(SAIDA / "linhas_peso_semanal.png", dpi=120)
```

Os outros dois do exemplo: `ax.hist(valores, bins=6)` (histograma) e
`df.plot.scatter(x="espessura_um", y="gramatura_gm2")` (dispersão). A dispersão mostra
uma correlação de 0,99 entre espessura e gramatura, o que faz sentido físico:
gramatura ≈ espessura × densidade.

**Mostrar ou salvar?** `fig.savefig("arquivo.png", dpi=120)` grava a imagem (vai no
relatório, no e-mail, no portfólio). `plt.show()` abre uma janela e **para o programa**
até você fechá-la. Os exemplos só salvam; rode com `--mostrar` para abrir as janelas:

```text
python 10-dados-com-pandas/exemplos/13_graficos.py --mostrar
```

Em scripts automáticos (e nos testes do curso), usa-se `matplotlib.use("Agg")`: o
matplotlib desenha só na memória, sem janela. Feche figuras que não vai mais usar com
`plt.close(fig)` ou `plt.close("all")`, senão elas acumulam memória.

> 🔮 **Preveja antes de rodar:** quantos itens tem `ax.patches`, e qual é o texto de
> `ax.get_ylabel()`?

```python
ax = pd.Series({"A": 3, "B": 5, "C": 2}).plot.bar()
ax.set_title("Bobinas reprovadas")
print(len(ax.patches), repr(ax.get_ylabel()))
```

<details><summary>Resposta</summary>

```text
3 ''
```

Uma barra (um retângulo, um "patch") por categoria. E o rótulo do eixo y é vazio: o
pandas não inventa rótulo. Gráfico sem rótulo nos eixos é gráfico pela metade. É isso que
os testes dos exercícios 11 e 12 conferem: eles inspecionam o objeto Axes.
</details>

> 🔧 **Modifique:** no exemplo 13, troque `plot.bar` por `plot.barh` (barras
> horizontais). Quando os nomes das categorias são longos (cargos, clientes), barras
> horizontais leem muito melhor.

**E o Power BI?** No mercado, muitos painéis são feitos no Power BI (ou Tableau, Looker
Studio). Eles não competem com o pandas, se completam: o Python faz a parte pesada e
repetível (ler, limpar, cruzar, conferir regras) e grava uma tabela limpa (Excel, CSV ou
um banco); o Power BI conecta nessa tabela e monta o painel interativo para a gerência.
Saber os dois aumenta bastante suas chances em vagas de analista. Gráficos em código,
como os desta seção, brilham em relatórios automáticos e laudos.

## 17. Gráfico de controle (média ± 3σ)

No laboratório, a pergunta mais importante não é "esta bobina passou?", e sim "o
**processo** está estável?". O gráfico de controle de valores individuais responde:

- **Linha central:** a média.
- **LSC e LIC** (limites superior e inferior de controle): média ± 3 desvios-padrão (σ).
- Ponto fora dos limites indica **causa especial** (troca de matéria-prima, ajuste de
  máquina, erro de medição): vale investigar.

**Exemplo resolvido** (`exemplos/14_grafico_controle.py`). Eu quero vigiar a espessura do
LAM-62. Primeiro eu separo os dados e ponho na ordem em que as bobinas foram medidas
(gráfico de controle é sobre **tempo**). Depois calculo os limites. Por fim, desenho
pontos, média, limites e, para comparar, os limites de **especificação** (62 µm ± 7%):

```python
lam = df[df["produto"] == "LAM-62"].sort_values(["data", "bobina"]).reset_index(drop=True)
valores = lam["espessura_um"]
media = valores.mean()
sigma = valores.std()  # desvio-padrão amostral, igual ao DESVPAD do Excel
lsc, lic = media + 3 * sigma, media - 3 * sigma

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(valores.index + 1, valores, marker="o", label="Espessura")
ax.axhline(media, color="green", label=f"Média {media:.1f}")
ax.axhline(lsc, color="red", linestyle="--", label=f"LSC {lsc:.1f}")
ax.axhline(lic, color="red", linestyle="--", label=f"LIC {lic:.1f}")
ax.axhline(62 * 1.07, color="orange", linestyle=":", label="LSE")
ax.axhline(62 * 0.93, color="orange", linestyle=":", label="LIE")
```

```text
Média 61.54 | σ 3.22 | LIC 51.86 | LSC 71.21
Pontos fora de CONTROLE: 0
Pontos fora de ESPECIFICAÇÃO: [67.5, 56.9, 57.1]
Linhas no gráfico: 6
```

Leia com calma, porque essa é uma lição de qualidade de verdade:

- **Limites de controle** são a "voz do processo": calculados dos dados.
- **Limites de especificação** são a "voz do cliente": vêm do contrato.

Aqui o processo está **sob controle** (nenhum ponto fora de 51,9 a 71,2) e mesmo assim
3 bobinas saíram **fora de especificação**. Ou seja: a variação é "normal" para esse
processo, mas grande demais para a tolerância do cliente. Não adianta caçar causa
especial; é preciso reduzir a variação (ou rever a especificação). Isso se chama
**capacidade** do processo (índices Cp e Cpk, veja "Para ir além").

> ⚠️ **Erro comum:** calcular os limites com os mesmos dados que você quer vigiar, com
> poucos pontos. Um ponto muito fora puxa a média e infla o σ. Com 10 pontos, é
> matematicamente impossível um deles ficar a mais de 3σ da média calculada com ele
> mesmo. O certo: calcule os limites num período de **referência** estável (20 a 25
> pontos, no mínimo) e use-os para vigiar as bobinas **novas**. É o que o exercício 12
> faz.

> 💡 **Dica:** o gráfico de valores individuais "de livro" (I-MR) estima o σ pela média
> das amplitudes móveis (MR̄ / 1,128), que é menos sensível a tendências. A versão com
> `std()` é uma boa primeira aproximação e é a que muitos laboratórios usam no Excel.

## 18. Laboratório guiado: o mercado de dados em 133 mil salários

Hora de usar tudo num arquivo real e grande: `../arquivos/salaries.csv` (a partir da
pasta `curso-python`), com salários de profissionais de dados de 2020 a 2025. Colunas:
`work_year`, `experience_level` (EN júnior, MI pleno, SE sênior, EX executivo),
`employment_type` (FT tempo integral...), `job_title`, `salary_in_usd`,
`employee_residence`, `remote_ratio` (0, 50, 100), `company_location`, `company_size`.

Rode `python 10-dados-com-pandas/exemplos/15_laboratorio_salarios.py` e acompanhe. (Sem o
arquivo grande, ele usa a amostra de 600 linhas em `dados/` e os números mudam.)

**Pergunta 0: posso confiar nesta base?**

```text
(133349, 11)
Anos: {2020.0: 75, 2021.0: 216, 2022.0: 1660, 2023.0: 8521, 2024.0: 62240, 2025.0: 60627}
work_year vazio: 10
Linhas idênticas a outra: 68722
```

Três achados antes de qualquer conta: 2020 e 2021 têm pouquíssimos registros (não
compare com 2024 sem cuidado); 10 linhas sem ano (por isso `work_year` veio como float,
e o script converte para `Int64`); e **68 mil linhas idênticas a outra**. Duplicata?
Talvez não: sem um identificador da pessoa, duas pessoas com mesmo cargo, nível, país e
salário geram linhas iguais. Decisão consciente: manter, e registrar essa decisão. Em
análise de dados, **escrever as premissas** é metade do trabalho.

**Pergunta 1: quanto ganha cada nível?** (só tempo integral, em mil USD/ano)

```python
NIVEIS = {"EN": "Júnior", "MI": "Pleno", "SE": "Sênior", "EX": "Executivo"}
df = df[df["employment_type"] == "FT"].copy()
df["nivel"] = pd.Categorical(
    df["experience_level"].map(NIVEIS), categories=list(NIVEIS.values()), ordered=True
)
df["salario_mil_usd"] = df["salary_in_usd"] / 1000
por_nivel = df.groupby("nivel", observed=True)["salario_mil_usd"].agg(
    ["count", "median", "mean"]
)
```

```text
           count  median   mean
nivel
Júnior     12106    87.5   99.9
Pleno      40203   130.0  143.4
Sênior     77057   161.3  173.0
Executivo   3197   190.0  202.0
```

O `pd.Categorical(..., ordered=True)` faz os níveis aparecerem na ordem da carreira, e
não em ordem alfabética. Repare que a **média é sempre maior que a mediana**: poucos
salários muito altos puxam a média para cima. Para salário, use a mediana ("metade ganha
menos que isso").

**Pergunta 2: quais cargos aparecem mais?**

```text
Cargos diferentes: 387
job_title
Data Scientist               17244
Software Engineer            14955
Data Engineer                14794
Data Analyst                 12209
Engineer                      9412
...
```

**Pergunta 3: cargo x nível** (mediana, mil USD), com `pivot_table`:

```text
nivel               Júnior  Pleno  Sênior  Executivo
job_title
Analytics Engineer    98.9  130.0   153.0      204.0
Data Analyst          81.9   90.0   120.0      114.4
Data Engineer         84.0  120.0   153.1      194.5
Data Scientist        97.0  129.0   160.0      189.4
```

Leitura de carreira: o analista de dados é a porta de entrada mais comum, mas o salário
cresce menos com a senioridade. Engenharia de dados e analytics engineering (SQL +
Python + pipelines, exatamente a trilha deste curso) crescem mais.

**Pergunta 4: trabalho remoto paga menos?**

```text
             count  median
regime
Híbrido        304    69.6
Presencial  104802   148.0
Remoto       27457   145.0
```

Parece que híbrido paga a metade. Mas **cuidado**: híbrido tem só 304 registros, de
países e anos variados. Para comparar de forma justa, fixe o que puder: só empresas dos
EUA, só 2025, e compare **dentro de cada nível**:

```text
regime     Híbrido  Presencial  Remoto
nivel
Júnior        26.3        92.9    88.6
Pleno        101.5       138.2   129.9
Sênior         NaN       168.4   160.0
Executivo      NaN       190.0   194.9
Registros híbridos nessa fatia: 3
```

Agora a conclusão honesta: remoto paga um pouco menos que presencial (uns 5%) nos níveis
júnior a sênior; sobre híbrido **não dá para concluir nada** (3 registros). Isso é pensar
como analista: desconfiar da primeira resposta, controlar variáveis e olhar o tamanho da
amostra.

**Pergunta 5: e quem mora no Brasil?**

```text
Registros: 85
           count  median
nivel
Júnior         5    40.0
Pleno         32    57.0
Sênior        45    66.7
Executivo      3   110.0
```

Só 85 registros, a maioria pleno e sênior, e provavelmente gente que trabalha para fora
(salário em dólar). Serve como pista, não como tabela salarial do Brasil.

O script ainda mostra a evolução por ano e salva `saida/salario_por_nivel.png`, um bom
começo para um projeto de portfólio.

> 🔧 **Modifique:** escolha **o seu** cargo-alvo (ex.: `"Data Analyst"` ou
> `"Data Engineer"`) e calcule a mediana por nível e por `company_size` (S, M, L). Depois
> faça um gráfico de barras com o resultado.

## Lendo mensagens de erro deste módulo

**`KeyError: 'Espessura'`**
A coluna não existe com esse nome. Rode `print(df.columns.tolist())` e compare: acento,
maiúscula, espaço sobrando ou unidade no nome (`"Espessura (µm)"`). Renomeie logo depois
de ler.

**`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe7 in position 56`**
O arquivo não está em UTF-8. Tente `encoding="cp1252"` (Windows/ERP antigo).

**`ValueError: The truth value of a Series is ambiguous...`**
Você usou `and`, `or`, `not` ou um `if` com uma Series inteira. Em máscaras, use `&`,
`|`, `~` com parênteses.

**`TypeError: Cannot perform reduction 'mean' with string dtype`** (ou
`dtype 'str' does not support operation 'mean'`)
A coluna é texto. Faltou `decimal=","` ou `thousands="."` na leitura, ou há lixo
(`"n/d"`) na coluna: use `pd.to_numeric(..., errors="coerce")`.

**`ValueError: You are trying to merge on str and int64 columns for key 'op'`**
A chave tem tipos diferentes nas duas tabelas. Converta uma delas (`astype(str)`), e
cuidado com zeros à esquerda que já se perderam.

**`ChainedAssignmentError`** (pandas 3) ou **`SettingWithCopyWarning`** (pandas 2.2)
Você fez `df[...][...] = valor`. A alteração não chega na tabela original. Use
`df.loc[mascara, "coluna"] = valor`.

**`ValueError: time data "31/09/2026" doesn't match format "%d/%m/%Y"`** (ou
`day is out of range for month`)
Data inexistente ou em outro formato. Corrija na origem ou use `errors="coerce"` e trate
os `NaT`.

**`PermissionError: [Errno 13] Permission denied: '...xlsx'`**
O arquivo está aberto no Excel (Windows não deixa outro programa gravar). Feche-o.

**`ModuleNotFoundError: No module named 'openpyxl'`** (ou `ImportError: Missing optional
dependency 'openpyxl'`)
Instale com `python -m pip install openpyxl`, com o ambiente virtual ativado.

## Boas práticas

- **Leia com os tipos certos** (`sep`, `decimal`, `thousands`, `encoding`, `dtype`) e
  confira `df.dtypes` logo depois.
- **Renomeie colunas para `snake_case`** sem acento logo após ler.
- **Não altere a tabela de quem chamou:** `df.copy()` no começo da função.
- **Altere valores com `.loc`**, numa operação só. Nada de `df[...][...] = ...`.
- **Prefira operações vetorizadas**; `apply` e `for` só quando não houver alternativa.
- **`merge` com `how="left"`, `validate=` e, na dúvida, `indicator=True`.** Conte as
  linhas antes e depois.
- **Trate o "não sei" explicitamente:** sem especificação não é aprovado nem reprovado.
- **Datas sempre com `format=`.**
- **Separe leitura, regras e saída em funções** (como no "No mundo real" abaixo). As
  regras viram funções testáveis com DataFrames pequenos, como nos exercícios.
- **Gráfico com título e rótulos nos eixos**, sempre. Uma pergunta por gráfico.

## No mundo real

Juntando tudo, `exemplos/16_conferencia_planilha.py` faz uma versão em pandas do núcleo
do seu projeto final: lê as 4 abas da planilha de valores, descobre o produto de cada OP
no CSV do ERP, cruza com as especificações, confere espessura e gramatura (nominal ±
tolerância) e COF (máximo, aceitando a observação "COF: liberado"), e marca como
**pendente** o que não dá para decidir. O coração é uma função pura:

```python
def conferir(medicoes: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta as colunas 'status' e 'motivo' a cada bobina."""
    df = medicoes.merge(specs, on="produto", how="left")
    folga = df["espessura_nominal"] * df["tolerancia_pct"] / 100
    esp_fora = ~df["espessura_um"].between(
        df["espessura_nominal"] - folga, df["espessura_nominal"] + folga
    )
    folga_g = df["gramatura_nominal"] * df["tolerancia_pct"] / 100
    gram_fora = ~df["gramatura_gm2"].between(
        df["gramatura_nominal"] - folga_g, df["gramatura_nominal"] + folga_g
    )
    cof_fora = df["cof"] > df["cof_max"]
    cof_liberado = df["observacao"].fillna("").str.contains("cof: liberado", case=False)

    df["motivo"] = ""
    df.loc[esp_fora, "motivo"] += "espessura; "
    df.loc[gram_fora, "motivo"] += "gramatura; "
    df.loc[cof_fora & ~cof_liberado, "motivo"] += "COF; "
    df["motivo"] = df["motivo"].str.rstrip("; ")

    df["status"] = "APROVADA"
    df.loc[df["motivo"] != "", "status"] = "REPROVADA"
    df.loc[df["espessura_nominal"].isna(), ["status", "motivo"]] = [
        "PENDENTE",
        "produto sem especificação",
    ]
    df.loc[(df["op"].notna()) & (df["produto"].isna()), ["status", "motivo"]] = [
        "PENDENTE",
        "OP sem cadastro no ERP",
    ]
    return df
```

Saída (trecho):

```text
status
APROVADA     54
PENDENTE     10
REPROVADA     6
Name: count, dtype: int64
linha    bobina    status                    motivo
    A 024483-01  PENDENTE produto sem especificação
  ...
    A 024499-05  PENDENTE    OP sem cadastro no ERP
    B 024433-01 REPROVADA                 gramatura
    B 024458-02 REPROVADA                       COF
    C 024451-02 REPROVADA      espessura; gramatura
    D 024447-03 REPROVADA      espessura; gramatura
    D 024466-03 REPROVADA                 espessura
    D 024466-04 REPROVADA      espessura; gramatura
```

Repare: a bobina 024430-03 tem COF 0,38 (máximo 0,35), mas está aprovada porque a
planilha diz "COF: liberado". E nenhuma bobina "some" ou é aprovada sem regra. No módulo
14, essa mesma lógica volta com regras vindas do banco SQLite (módulo 11) e testes para
cada caso.

## Resumo

| Tarefa | Sintaxe |
|---|---|
| CSV brasileiro | `pd.read_csv(c, sep=";", decimal=",", thousands=".", encoding="utf-8-sig", dtype={"op": str})` |
| Excel, todas as abas | `pd.read_excel(c, sheet_name=None, header=1)` → dict |
| Nomes das abas | `pd.ExcelFile(c).sheet_names` |
| Empilhar | `pd.concat([t1, t2], ignore_index=True)` |
| Inspecionar | `df.shape`, `df.info()`, `df.describe()`, `df["c"].value_counts()` |
| Colunas | `df["c"]`, `df[["a", "b"]]` |
| Rótulo / posição | `df.loc[linhas, colunas]`, `df.iloc[i, j]` |
| Filtro | `df[(df["a"] > 1) & (df["b"].isin(["x", "y"]))]`, `~`, `between` |
| Alterar valores | `df.loc[mascara, "c"] = valor` |
| Texto | `df["c"].str.strip().str.upper()`, `.str.contains(...)` |
| Números com lixo | `pd.to_numeric(s, errors="coerce")` |
| Ausentes | `isna().sum()`, `dropna(subset=[...])`, `fillna(v)` |
| Duplicatas | `duplicated(subset=[...])`, `drop_duplicates(subset=[...])` |
| Datas | `pd.to_datetime(s, format="%d/%m/%Y")`, `.dt.month`, `.dt.strftime("%Y-%m")` |
| Ordenar | `sort_values(["a", "b"], ascending=[True, False])`, `nlargest(n, "c")` |
| Agrupar | `df.groupby("g", as_index=False).agg(novo=("c", "sum"))` |
| Por linha do grupo | `df.groupby("g")["c"].transform("mean")` |
| Juntar | `a.merge(b, on="k", how="left", validate="many_to_one", indicator=True)` |
| Tabela dinâmica | `df.pivot_table(index=, columns=, values=, aggfunc=, fill_value=0)` |
| Exportar | `to_csv(..., sep=";", decimal=",", index=False, encoding="utf-8-sig")`, `pd.ExcelWriter` |
| Gráfico rápido | `ax = serie.plot.bar()`; `ax.set_title(...)`; `ax.figure.savefig("x.png")` |
| Gráfico pyplot | `fig, ax = plt.subplots()`; `ax.plot`, `ax.hist`, `ax.scatter`, `ax.axhline` |

## Você domina este módulo se...

- [ ] Consigo ler um CSV do Excel brasileiro e um CSV em cp1252 sem consultar, e explicar
      para que serve cada parâmetro.
- [ ] Consigo explicar a diferença entre `loc` e `iloc`, e entre `size()` e `count()`.
- [ ] Consigo filtrar com duas condições sem cair no erro do `and`.
- [ ] Consigo explicar por que `df[mascara]["col"] = valor` não funciona e escrever a
      versão certa.
- [ ] Consigo limpar uma coluna de números brasileiros com lixo e dizer quantos valores
      viraram ausentes.
- [ ] Consigo resumir uma tabela com `groupby`/`agg` e cruzar duas tabelas com `merge`,
      sabendo dizer o que acontece com quem não casa.
- [ ] Consigo escolher o gráfico certo para uma pergunta e salvá-lo em PNG com título e
      rótulos.
- [ ] Consigo explicar a diferença entre limite de controle e limite de especificação.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_primeiro_dataframe` | ★☆☆ | criar DataFrame, `sum`, `idxmax`, `loc` |
| 02 | `ex02_ler_csv_brasileiro` | ★☆☆ | `read_csv` com `sep`, `decimal`, `thousands`, `encoding`, `dtype` |
| 03 | `ex03_filtrar_fora_da_faixa` | ★☆☆ | máscaras, `\|`, `isin`, `reset_index` |
| 04 | `ex04_nova_coluna_desvio` | ★☆☆ | colunas calculadas, `.loc`, não alterar o original |
| 05 | `ex05_ler_abas_excel` | ★★☆ | `read_excel` com várias abas, `concat`, `rename` |
| 06 | `ex06_limpar_medicoes` | ★★☆ | `.str`, `to_numeric`, `dropna`, `drop_duplicates` |
| 07 | `ex07_corrija_o_relatorio` | ★★☆ | **leitura de código e depuração**: 4 defeitos clássicos |
| 08 | `ex08_resumo_por_linha` | ★★☆ | `groupby` + agregação nomeada, `round` |
| 09 | `ex09_conferir_especificacao` | ★★★ | `merge` left com `validate`, regras de status |
| 10 | `ex10_tabela_por_mes` | ★★☆ | `to_datetime` com formato, `pivot_table` |
| 11 | `ex11_grafico_barras` | ★☆☆ | gráfico de barras, título e rótulos, salvar PNG |
| 12 | `ex12_grafico_controle` | ★★★ | média ± 3σ, pontos fora, `axhline`, `scatter` |
| 13 | `ex13_revisao_emails_expedicao` | ★★☆ | **revisão**: regex e números BR (mód. 05) + pandas |
| 14 | `ex14_revisao_relatorio_excel` | ★★★ | **revisão**: dataclass (mód. 08) + pathlib (mód. 06) + Excel formatado |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError`, e rode, na pasta `curso-python`:

```text
python curso.py testar 10 ex01
```

Os testes criam DataFrames pequenos e arquivos temporários; nenhum usa o arquivo grande
de salários. Para os gráficos, eles usam o backend "Agg" e inspecionam o objeto Axes
(título, rótulos, quantidade de barras e linhas), então nenhuma janela abre.

## Desafio do módulo

**Relatório mensal da qualidade:** um programa de linha de comando que lê as medições,
as OPs do ERP e as especificações, filtra um mês (`--mes 2026-08`), confere cada bobina e
gera um Excel formatado com as abas Resumo, Não conformidades e Medições, mais um
gráfico de controle em PNG. Enunciado completo em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou com o [quiz do módulo](quiz.md) (14 perguntas, gabarito no final).

## Para ir além

- Guia oficial "10 minutes to pandas":
  <https://pandas.pydata.org/docs/user_guide/10min.html>
- pandas para quem vem do Excel ("Comparison with spreadsheets"):
  <https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_spreadsheets.html>
- Copy-on-Write no pandas (o que mudou no 3.0):
  <https://pandas.pydata.org/docs/user_guide/copy_on_write.html>
- Tutoriais do matplotlib (comece por "Quick start guide"):
  <https://matplotlib.org/stable/tutorials/index.html>
- Formatação de planilhas com openpyxl: <https://openpyxl.readthedocs.io/en/stable/styles.html>
- Livro gratuito do criador do pandas, *Python for Data Analysis*, 3ª edição:
  <https://wesmckinney.com/book/>
- Controle estatístico de processo (gráficos de controle, Cp e Cpk), no manual do NIST:
  <https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm>
