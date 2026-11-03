# Módulo 14 — Projeto final: Validador de Certificados

> **Tempo estimado:** 15 a 25 horas · **Pré-requisitos:** módulos 00 a 13 (08, 09, 11 e
> 12 são essenciais; 13 para a extensão da API) · **Nível:** intermediário (projeto
> integrador)

## O que você vai aprender

- Transformar uma descrição de trabalho ("leio a planilha, confiro, emito no TOTVS")
  numa lista de requisitos e numa arquitetura em camadas.
- Dizer, para cada pedaço de código, em qual camada ele mora e do que ele pode
  depender.
- Modelar o domínio com dataclasses que se recusam a existir com dados inválidos.
- Carregar regras de qualidade de um banco SQLite aberto só para leitura.
- Implementar tolerância fixa (mín/máx) e nominal ± % sem cair na armadilha do float.
- Ler uma planilha de 4 abas com openpyxl, sendo tolerante no formato e rígido no
  conteúdo.
- Escolher a especificação da OP (cliente ou padrão da linha) sem nunca chutar.
- Extrair OP, NF e peso dos e-mails da expedição e separar os fora do padrão.
- Montar a fila de emissão, emitir em **modo ensaio** com idempotência, e gerar o
  relatório da série.
- Juntar tudo numa CLI com argparse, logging e códigos de saída.
- Montar um projeto profissional (src layout, pyproject, testes, GitHub Actions) e
  publicá-lo como portfólio.
- Planejar as extensões: robô Playwright no Edge, leitura do Outlook e API FastAPI.

## Por que isso importa

Este é o projeto que você descreveu no começo do curso. Não é exercício de livro: é a
automação que vai tirar horas de digitação da sua semana e evitar um certificado
emitido com valor fora da tolerância.

Para o mercado, ele vale ainda mais. Um recrutador de dados, automação ou backend vê
um sistema com regras de negócio reais, banco de dados, leitura de Excel, testes
automatizados, CI no GitHub e decisões de projeto explicadas. Isso conta mais que dez
certificados de curso. Na entrevista, você conta a história: "tinha um processo
manual, construí isso, e funciona assim".

Neste módulo você vai **construir** o sistema em 14 etapas testadas e, no fim,
encontrar a montagem completa na pasta `projeto-completo/`, pronta para virar o seu
repositório.

## 1. O problema, em uma página

Antes de qualquer código, escreva o problema em português. Se não cabe numa página,
ainda não está entendido.

**Hoje (manual):** a expedição manda e-mail pedindo certificado ("OP 24518, NF 123456,
1.250,5 kg"). Alguém abre a planilha de valores, acha a OP na aba da linha certa,
confere cada característica contra a especificação do cliente (ou o padrão da
linha), olha se o COF foi liberado, e digita o certificado no TOTVS.

**Amanhã (com o sistema):**

```text
e-mails da expedição ─┐
planilha de valores ──┼─> triagem ─> fila de emissão ─> emissor (TOTVS) ─> relatório
banco de regras ──────┘      │                                                 ▲
                             └─> bloqueados, com motivo ───────────────────────┘
```

**O que a versão 1 faz:**

1. Lê as regras (especificações e tolerâncias) de um banco SQLite.
2. Lê a planilha de valores (4 abas: Linha A, B, C e D).
3. Lê os pedidos dos e-mails (OP, NF e peso) e separa os fora do padrão.
4. Para cada pedido: acha a OP, confere a linha, escolhe a especificação, valida as
   tolerâncias e a liberação do COF.
5. Emite os certificados das OPs aprovadas e liberadas (por enquanto, em ensaio).
6. Grava um relatório da série: emitidos, bloqueados e o motivo de cada bloqueio.

**O que a versão 1 NÃO faz** (e está tudo bem): não clica no TOTVS de verdade, não lê
o Outlook direto, não tem tela. Escopo pequeno e terminado vence escopo grande pela
metade.

### Exemplo resolvido: dos verbos às funções

Primeiro eu pego a descrição do processo e sublinho os **substantivos** e os
**verbos**. Substantivos viram modelos (dados). Verbos viram funções (ações).

```text
"A expedição manda o PEDIDO (OP, NF, peso). Eu acho a OP na PLANILHA, confiro cada
CARACTERÍSTICA contra a ESPECIFICAÇÃO e a TOLERÂNCIA, vejo a OBSERVAÇÃO de liberação
e emito o CERTIFICADO."

substantivos -> Pedido, Medicao (linha da planilha), Especificacao, Tolerancia,
                ResultadoValidacao, ItemFila (o pedido depois da triagem)
verbos       -> ler_email, ler_planilha, escolher_especificacao, validar_medicao,
                esta_liberado, montar_fila, emitir_fila, escrever_relatorio
```

Depois eu pergunto, para cada verbo: "isso precisa de arquivo, rede ou tela?". Se não
precisa, é regra pura e vai para o núcleo. Se precisa, é borda. É assim que nasce a
arquitetura da próxima seção.

> 💡 **Dica:** escreva essa lista num papel antes de abrir o VS Code. Dez minutos aqui
> economizam um fim de semana de refatoração.

**Tente você:** na frase "o supervisor recebe um aviso quando alguma OP fica
bloqueada", quais são os substantivos e os verbos? Viraria modelo, função, ou os dois?

<details><summary>Resposta</summary>

Substantivos: supervisor, aviso, OP. Verbos: receber (o aviso), ficar bloqueada.
"Aviso" pode virar um modelo pequeno (destinatário, assunto, texto) e uma função
`montar_aviso(bloqueados) -> Aviso` (regra pura). Enviar o e-mail é borda (precisa de
rede): outra função, `enviar_aviso(aviso)`, que fica isolada como o emissor do TOTVS.

</details>

## 2. Arquitetura em camadas

Pense no laboratório. O técnico **mede**. A norma **decide** se passou. O supervisor
**assina**. Ninguém mistura os papéis: o técnico não muda a norma porque a bobina está
quase boa. O sistema segue a mesma divisão.

```text
┌───────────────────────────── CLI (cli.py) ─────────────────────────────┐
│ argumentos, logging, códigos de saída                                  │
├───────────────────── SERVIÇO (fila.py, serie.py) ──────────────────────┤
│ triagem: junta as peças, decide emitir ou bloquear                     │
├──────────── NÚCLEO PURO (modelos.py, regras.py, texto.py) ─────────────┤
│ dataclasses, tolerâncias, escolha da especificação, liberação          │
│ NÃO lê arquivo, NÃO acessa banco, NÃO abre navegador                   │
├──────────────────────────────── BORDAS ────────────────────────────────┤
│ banco.py (SQLite)  planilha.py (openpyxl)  expedicao.py (e-mails)      │
│ emissao.py / robo_playwright.py (TOTVS)   relatorio.py (Excel/CSV)     │
└────────────────────────────────────────────────────────────────────────┘
```

**Regra de dependência:** as dependências apontam para dentro. As bordas e o serviço importam
o núcleo; o núcleo não importa ninguém de fora. Consequência prática: se amanhã a
planilha virar um banco, ou o TOTVS ganhar uma API, só a borda muda. As regras, que são
o que vale dinheiro, ficam intactas.

O exemplo `exemplos/01_nucleo_e_casca.py` mostra a ideia em 30 linhas:

```python
def verificar_espessura(valor: float, nominal: float, percentual: float) -> str | None:
    """None se passou; senão, o motivo. Não sabe de onde vieram os números."""
    folga = nominal * percentual / 100
    minimo, maximo = round(nominal - folga, 4), round(nominal + folga, 4)
    if minimo <= valor <= maximo:
        return None
    return (
        f"espessura {valor:g} fora de {nominal:g} ± {percentual:g}% ({minimo:g} a {maximo:g})"
    )
```

```text
python exemplos/01_nucleo_e_casca.py
OP 24518: OK
OP 24519: espessura 44.8 fora de 40 ± 10% (36 a 44)
OP 24520: OK
núcleo testado sem abrir arquivo nenhum
```

> 🔧 **Modifique:** troque o `10` da chamada em `main()` por `12` e rode de novo. A OP
> 24519 passa? Calcule o novo máximo de cabeça antes de rodar (40 + 12% de 40).

| Camada | Arquivo no projeto | Etapas (exercícios) |
|---|---|---|
| Núcleo: modelos | `modelos.py` | 1 |
| Borda: banco de regras | `banco.py` | 2 |
| Núcleo: regras | `regras.py` | 3, 4, 5, 9 |
| Núcleo: texto | `texto.py` | 6 |
| Borda: planilha | `planilha.py` | 7, 8 |
| Borda: e-mails | `expedicao.py` | 10 |
| Serviço: triagem | `fila.py` | 11 |
| Borda: emissão (TOTVS) | `emissao.py` | 12 |
| Borda: relatório | `relatorio.py` | 13 |
| Entrada: CLI | `cli.py` | 14 |

**Tente você:** em qual camada fica uma função que decide se a OP pode ter certificado
**sem** o COF liberado quando o cliente é "Biscoitos Aurora"?

<details><summary>Resposta</summary>

No núcleo (regras). É uma regra de negócio: recebe dados (cliente, observação) e
devolve uma decisão. Onde o nome do cliente é lido (planilha ou banco) é borda; a
decisão em si não depende de arquivo nenhum.

</details>

## 3. Decisões de projeto (e por quê)

Projetos profissionais registram as decisões, não só o código. Daqui a seis meses,
você (ou quem herdar o sistema) vai perguntar "por que é assim?". Estas são as do
Validador:

1. **Regra devolve motivo, não True/False.** `verificar_fixa` devolve `None` (passou)
   ou `"cof 0.38 acima do máximo 0.35"`. O relatório precisa do porquê; um booleano
   joga a informação fora.
2. **Nunca chutar.** Título de especificação desconhecido, linha divergente da aba, OP
   repetida na planilha, e-mail com duas OPs: tudo vira **pendência** com motivo. Uma
   pendência custa um minuto do técnico. Um certificado errado custa um cliente.
3. **Especificação do cliente herda do padrão da linha.** O cliente lista só o que muda
   (ex.: COF de 0,18 a 0,25). O resto vem do padrão. Menos cadastro, menos erro.
4. **Limites inclusivos e arredondados.** Valor igual ao limite passa. Os limites são
   arredondados em 4 casas para o float não reprovar 33,3 num mínimo de 33,3.
5. **Modo ensaio é o padrão.** Emitir de verdade exige pedir (`--emitir`). O erro mais
   caro é emitir errado; o padrão seguro protege contra o esquecimento.
6. **Idempotência por (OP, NF).** Rodar a série duas vezes não emite duas vezes. A
   chave inclui a NF porque a mesma OP pode sair em entregas parciais.
7. **Robô isolado atrás de uma interface.** O sistema conversa com um `Emissor`
   (`emitir(item) -> comprovante`). Hoje existe o de ensaio; o robô Playwright vai
   implementar a mesma interface.
8. **Uma falha não derruba a série.** Se a tela do TOTVS travar numa OP, ela vira
   "falha" e a próxima segue. Mas bug (erro inesperado) sobe e para tudo.
9. **Regras no SQLite, não numa planilha de regras.** O banco tem tipos, chave primária
   e `CHECK` (tipo só pode ser `fixa` ou `nominal`; uma linha tem no máximo um padrão).
   Uma planilha aceita qualquer coisa em qualquer célula. O custo: editar exige um
   programa como o DB Browser for SQLite.
10. **Sem pandas no núcleo.** openpyxl lê a planilha linha a linha e o resto é Python
    puro. Menos dependências, instalação mais leve no PC da fábrica. pandas continua
    ótimo para **analisar** os dados depois (módulo 10).

> ⚠️ **Erro comum:** tomar a decisão certa e não escrever o porquê. O próximo que mexer
> (talvez você) "simplifica" e reintroduz o bug que a decisão evitava.

## 4. Os dados de exemplo

Tudo o que você precisa para construir e testar está em `dados/`. São dados
**fictícios**, mas com os casos difíceis da vida real.

```text
dados/
  gerar_planilha.py      cria planilha_valores.xlsx (4 abas, 16 OPs)
  gerar_banco_regras.py  cria regras.db a partir de schema_regras.sql
  schema_regras.sql      as tabelas linha, especificacao e tolerancia
  planilha_valores.xlsx
  regras.db
  emails/                8 e-mails da expedição (.txt), um deles em cp1252
```

Para recriar os arquivos (Windows, na pasta `curso-python`):

```text
python 14-projeto-final\dados\gerar_planilha.py
python 14-projeto-final\dados\gerar_banco_regras.py
```

No Linux/macOS, troque `\` por `/`.

**A planilha.** Uma aba por linha, cabeçalho na linha 1, uma OP por linha:

```text
OP | Data | Linha | Produto | Especificação | Espessura nominal (µm) | Espessura (µm) |
Gramatura nominal (g/m²) | Gramatura (g/m²) | COF | Tração (MPa) | Selagem (N/15mm) |
Observação
```

**O banco.** Padrões de linha têm a coluna `linha` preenchida; especificações de
cliente deixam `linha` vazia e listam só o que muda:

```sql
CREATE TABLE IF NOT EXISTS tolerancia (
    titulo         TEXT NOT NULL REFERENCES especificacao (titulo),
    caracteristica TEXT NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('fixa', 'nominal')),
    minimo         REAL,
    maximo         REAL,
    percentual     REAL,
    PRIMARY KEY (titulo, caracteristica)
);
```

```text
python exemplos/05_consultar_regras.py
Padrões de linha:
  linha A: PADRAO-A
  linha B: PADRAO-B
  linha C: PADRAO-C
  linha D: PADRAO-D

ESP-0412: Torrefação Serra - embalagem de café 250 g. COF interno de 0,18 a 0,25; selagem mínima 12 N/15mm.
  cof        fixa     mín=0.18 máx=0.25 %=None
  selagem    fixa     mín=12.0 máx=None %=None
```

**Os e-mails.** Cada um demonstra um caso:

| Arquivo | OP | O que demonstra | Resultado esperado |
|---|---|---|---|
| `email_01_op24518.txt` | 24518 | pedido limpo, linha A | emitir |
| `email_02_op24519.txt` | 24519 | espessura 44,8 em 40 ± 10% | bloqueado (reprovada) |
| `email_03_op24527.txt` | 24527 | "COF: aguardando 24h" | bloqueado (sem liberação) |
| `email_04_op24541.txt` | 24541 | ESP-0412, "NF-e nº 123.789" | emitir |
| `email_05_op24546.txt` | 24546 | especificação ESP-9999 | bloqueado (pendência) |
| `email_06_op24533.txt` | 24533 | aba B, linha digitada C, arquivo cp1252 | bloqueado (pendência) |
| `email_07_sem_nf.txt` | 24555 | "a NF sai amanhã" | fora do padrão |
| `email_08_duas_ops.txt` | 24520 e 24521 | duas OPs no mesmo e-mail | fora do padrão |

> 💡 **Dica:** quando for usar no trabalho, monte primeiro um conjunto de exemplo como
> este, com um caso de cada tipo. Ele vira a base dos seus testes e da sua confiança.

## 5. Roteiro de construção

A ordem das etapas não é aleatória: é **de dentro para fora**. Primeiro o núcleo
(fácil de testar, sem arquivo), depois as bordas, por último a orquestração. Cada
etapa é um exercício com testes.

| Fase | Etapas | Por que nesta ordem |
|---|---|---|
| 1. Domínio | 1 modelos | todo o resto troca essas "fichas" |
| 2. Regras | 2 banco, 3 fixa, 4 nominal, 5 validar OP, 6 liberação | o coração do sistema; puro e testável |
| 3. Entradas | 7 planilha, 8 linha, 9 especificação, 10 e-mails | traduzem o mundo para os modelos |
| 4. Saídas | 11 fila, 12 emissor, 13 relatório, 14 CLI | juntam tudo e entregam o resultado |

**Como trabalhar cada etapa:**

1. Leia o enunciado (docstring do topo) inteiro. Duas vezes.
2. Olhe as **peças prontas** no arquivo: são as etapas anteriores, já resolvidas,
   para cada etapa funcionar sozinha. Você pode fazer a etapa 11 antes da 7, e um erro
   na etapa 3 não quebra a 5.
3. Experimente no REPL antes de escrever a função (`python`, cole a peça, teste).
4. Escreva, rode `python curso.py testar 14 exNN`, leia a falha, corrija.
5. Compare com `solucoes/` só depois de passar. Os comentários de lá explicam o porquê.

> ⚠️ **Erro comum:** querer fazer as 14 etapas num dia só. Faça uma ou duas por sessão.
> Cada uma tem uma ideia nova; dê tempo para ela assentar.

## 6. Domínio e regras (etapas 1 a 6)

### 6.1 Modelos que se defendem (etapa 1)

Uma dataclass com `__post_init__` valida os dados no nascimento. Um objeto inválido
nunca chega a existir, então ninguém lá na frente precisa desconfiar dele.

#### Exemplo resolvido: a ficha da bobina

Quero uma ficha de bobina que recuse lote vazio, largura ou peso zerados. Primeiro
penso nos campos (lote, largura, peso). Depois, nas regras: "o que tornaria esta ficha
um absurdo?". Por fim, `frozen=True`, porque uma bobina pesada não muda de peso.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Bobina:
    lote: str
    largura_mm: float
    peso_kg: float

    def __post_init__(self) -> None:
        if not self.lote.strip():
            raise ValueError("bobina sem lote")
        if self.largura_mm <= 0 or self.peso_kg <= 0:
            raise ValueError(f"bobina {self.lote}: largura e peso devem ser > 0")


print(Bobina("L2026-118", 640, 412.5))
try:
    Bobina("L2026-119", 640, 0)
except ValueError as erro:
    print("recusada:", erro)
```

```text
Bobina(lote='L2026-118', largura_mm=640, peso_kg=412.5)
recusada: bobina L2026-119: largura e peso devem ser > 0
```

Na etapa 1 você faz o mesmo para `Tolerancia` e `Pedido`, e escreve a propriedade
`ResultadoValidacao.aprovado`. Por que propriedade, e não um campo `aprovado: bool`?
Porque um campo pode contradizer os motivos (`aprovado=True` com `motivos=["cof
alto"]`). Calculado a partir dos motivos, ele nunca mente.

O exemplo `exemplos/02_modelos_com_dataclasses.py` mostra ainda `frozen`, `replace` e
a junção de dicionários que você vai usar adiante.

### 6.2 O banco de regras (etapa 2)

A etapa 2 lê as tabelas `especificacao` e `tolerancia` e devolve
`{titulo: Especificacao}`. O resto do sistema nunca vê SQL.

#### Exemplo resolvido: as linhas de produção

Mesmo raciocínio, numa tabela mais simples. Quero `{codigo: descricao}`. Uma consulta,
um laço que desempacota cada linha, e fecho a conexão. (Rode na pasta
`14-projeto-final`: o caminho do banco é relativo a ela.)

```python
import sqlite3

conexao = sqlite3.connect("dados/regras.db")
consulta = "SELECT codigo, descricao FROM linha ORDER BY codigo"
linhas = {codigo: descricao for codigo, descricao in conexao.execute(consulta)}
conexao.close()
print(linhas)
```

```text
{'A': 'Extrusora 1 - filmes PE monocamada', 'B': 'Extrusora 2 - filmes PE finos', 'C': 'Coextrusora 3 camadas', 'D': 'Laminadora - PET/PE e BOPP/PE'}
```

Para as especificações são duas consultas: uma cria as fichas, a outra pendura cada
tolerância na ficha do seu título. Repare que `linha` NULL chega como `None` e precisa
virar `""`.

> ⚠️ **Erro comum:** `sqlite3.connect("regras_errado.db")` não dá erro: **cria** um
> banco vazio. O erro só aparece depois, como `no such table`. No projeto completo, o
> banco é aberto com `?mode=ro` (somente leitura), e um caminho errado vira erro na
> hora, com a mensagem certa.

### 6.3 Tolerância fixa e nominal (etapas 3 e 4)

Duas regras, mesma convenção: devolvem `None` ou o motivo. A fixa compara com mínimo
e máximo (um deles pode faltar: tração só tem mínimo). A nominal calcula a faixa a
partir do valor nominal da OP: 40 µm ± 10% vira 36 a 44.

Os números do motivo usam o formato `:g`, que corta zeros inúteis:

```python
print(f"{0.30:g} | {8.0:g} | {44.8:g} | {65.565:g}")
```

```text
0.3 | 8 | 44.8 | 65.565
```

> 🔮 **Preveja antes de rodar:** a gramatura nominal é 37,0 g/m² com ± 10%. A medida
> foi 33,3, exatamente o limite. Passa?
>
> ```python
> minimo = 37.0 * (1 - 10 / 100)
> print(minimo)
> print(minimo <= 33.3)
> ```

<details><summary>Resposta</summary>

```text
33.300000000000004
False
```

Reprovaria uma bobina boa. É o mesmo problema do `0.1 + 0.2` do módulo 01: o float não
representa 0,9 exatamente. A correção da etapa 4 é arredondar os limites com
`round(..., 4)`. Veja `exemplos/03_float_nos_limites.py`.

</details>

### 6.4 Validar a OP inteira (etapa 5)

Quem manda é a **especificação**: o laço percorre as tolerâncias que ela exige, não os
valores medidos. Assim, "faltou medir a selagem" vira motivo, e uma medição extra que
ninguém pediu é ignorada. E o laço não para no primeiro problema: junta todos, porque
o técnico quer corrigir tudo de uma vez.

```text
para cada tolerância da especificação:
    sem valor medido?          -> motivo "<car> sem valor medido"
    tipo fixa?                 -> verificar_fixa
    tipo nominal sem nominal?  -> motivo "<car> sem valor nominal"
    tipo nominal?              -> verificar_nominal
    a regra devolveu texto?    -> entra nos motivos
```

### 6.5 A observação de liberação (etapa 6)

A etapa 6 é de **leitura de código**. Você recebe a versão que um estagiário escreveu:

```python
def esta_liberado_v1(observacao):
    return "liberado" in observacao.lower()
```

Antes de consertar, você prevê o que ela faz em quatro casos reais. Depois escreve a
versão correta: normalizar o texto (minúsculas, sem acento, espaços simples) e
procurar a marca "cof" seguida de "liberado" com uma regex.

> 🔮 **Preveja antes de rodar:** qual destes casa com o padrão?
>
> ```python
> import re
>
> padrao = r"\bcof\s*[:-]?\s*liberad[oa]\b"
> for texto in ["cof: nao liberado", "cof - liberada", "cof liberado? nao"]:
>     print(texto, "->", re.search(padrao, texto) is not None)
> ```

<details><summary>Resposta</summary>

```text
cof: nao liberado -> False
cof - liberada -> True
cof liberado? nao -> True
```

No primeiro, depois de `cof:` e do espaço vem `nao`, e o padrão exige `liberad` ali.
O terceiro mostra um limite: regex não entende frase. "COF liberado? não" é raro o
bastante para aceitarmos o risco, mas vale um teste documentando o comportamento.

</details>

> 🔧 **Modifique:** a qualidade decidiu que "COF: OK" também libera. Mude o padrão para
> `liberad[oa]|ok` dentro de um grupo e escreva um teste para "COF: ok" e outro para
> "COF: ok?" antes de mudar o código.

## 7. Entradas (etapas 7 a 10)

### 7.1 Ler a planilha (etapa 7)

Regra de ouro das entradas: **olhe o arquivo real antes de escrever o leitor**.

```text
python exemplos/04_espiar_planilha.py
abas: ['Linha A', 'Linha B', 'Linha C', 'Linha D']
cabeçalho: ('OP', 'Data', 'Linha', 'Produto', 'Especificação') ...
  'OP'                         -> 24518 (int)
  'Data'                       -> datetime.datetime(2026, 10, 20, 0, 0) (datetime)
  'Linha'                      -> 'A' (str)
  'Produto'                    -> 'Filme PE 40 µm transparente' (str)
  'Especificação'              -> None (NoneType)
  'Espessura nominal (µm)'     -> 40 (int)
  'Espessura (µm)'             -> 41.2 (float)
Linha A: 5 OPs [24518, 24519, 24520, 24521, 24522]
Linha B: 4 OPs [24527, 24528, 24533, 24534]
Linha C: 4 OPs [24541, 24542, 24546, 24547]
Linha D: 3 OPs [24555, 24556, 24560]
```

Três descobertas que mudam o código: a OP vem como `int` (o pedido do e-mail traz
`str`); célula vazia vem `None`; o cabeçalho tem acento e unidade entre parênteses.

#### Exemplo resolvido: OP e COF da aba Linha C, pelo nome da coluna

Primeiro penso: "não quero depender da posição da coluna; alguém pode inserir uma
coluna nova amanhã". Então monto um dicionário `{nome normalizado: índice}` a partir do
cabeçalho. Depois percorro as linhas com `enumerate(..., start=2)`, porque o cabeçalho
é a linha 1 do Excel. (Também na pasta `14-projeto-final`.)

```python
import unicodedata

from openpyxl import load_workbook


def normalizar(texto):
    decomposto = unicodedata.normalize("NFKD", str(texto or ""))
    sem_acento = "".join(c for c in decomposto if not unicodedata.combining(c))
    return " ".join(sem_acento.lower().split())


pasta_trabalho = load_workbook("dados/planilha_valores.xlsx", read_only=True, data_only=True)
aba = pasta_trabalho["Linha C"]
linhas = aba.iter_rows(values_only=True)
colunas = {normalizar(nome): i for i, nome in enumerate(next(linhas))}
for numero, linha in enumerate(linhas, start=2):
    print(numero, linha[colunas["op"]], linha[colunas["especificacao"]], linha[colunas["cof"]])
pasta_trabalho.close()
```

```text
2 24541 ESP-0412 0.21
3 24542 ESP-0412 0.27
4 24546 ESP-9999 0.2
5 24547 ESP-0618 0.16
```

A etapa 7 vai além: tira a unidade do cabeçalho (`"Espessura (µm)"` vira
`"espessura"`), converte número digitado como texto (`"41,2"`), pula linhas vazias,
recusa planilha sem coluna obrigatória (`PlanilhaInvalida`) e **fecha** o arquivo
num `finally`.

> ⚠️ **Erro comum:** esquecer o `close()` com `read_only=True`. No Windows, o arquivo
> fica preso: o laboratório não consegue salvar a planilha enquanto o programa roda.

### 7.2 A linha bate com a aba? (etapa 8)

Cada aba é de uma linha, mas cada OP também tem a coluna "Linha". Se divergem, alguém
copiou a OP para a aba errada. O sistema não escolhe: o padrão da linha muda as
tolerâncias. Vira pendência: `linha informada C diferente da aba Linha B`.

### 7.3 Escolher a especificação (etapa 9)

Título vazio, padrão da linha. Título conhecido, padrão **mais** as tolerâncias do
cliente por cima. Título desconhecido, `EspecificacaoDesconhecida`. A junção usa
`{**padrao, **cliente}`.

> 🔮 **Preveja antes de rodar:**
>
> ```python
> padrao = {"cof": 0.35, "selagem": 8}
> cliente = {"cof": 0.25}
> print({**padrao, **cliente})
> print({**cliente, **padrao})
> ```

<details><summary>Resposta</summary>

```text
{'cof': 0.25, 'selagem': 8}
{'cof': 0.35, 'selagem': 8}
```

Quem vem depois vence. Na ordem errada, o padrão da linha apagaria a exigência do
cliente, e a OP 24542 (COF 0,27; cliente pede no máximo 0,25) seria aprovada.

</details>

### 7.4 Os e-mails da expedição (etapa 10)

Os padrões de regex já vêm prontos do módulo 05. O trabalho da etapa é **decidir**:
tirar repetições, juntar todos os problemas e nunca escolher entre duas OPs.

> 🔮 **Preveja antes de rodar:** o assunto e o corpo citam a OP.
>
> ```python
> import re
>
> RE_OP = re.compile(r"\bOP\b\s*(?:n[º°o]\.?\s*)?[:#-]?\s*(\d{4,6})\b", re.IGNORECASE)
> texto = "Assunto: Certificado - OP 24518\n\nOP: 24518\nNF: 123456"
> achados = RE_OP.findall(texto)
> print(achados)
> print(sorted(set(achados)))
> ```

<details><summary>Resposta</summary>

```text
['24518', '24518']
['24518']
```

`findall` devolve todas as ocorrências. O `set` junta as iguais: a mesma OP duas vezes
é uma OP só. Duas OPs **diferentes** continuam duas, e o e-mail fica fora do padrão.

</details>

Rodando os padrões sobre os 8 e-mails de exemplo:

```text
python exemplos/06_emails_da_expedicao.py
email_01_op24518.txt     OP=['24518'] NF=['123456'] peso=['1.250,5']
email_02_op24519.txt     OP=['24519'] NF=['123457'] peso=['980,0']
email_03_op24527.txt     OP=['24527'] NF=['123460'] peso=['2.040']
email_04_op24541.txt     OP=['24541'] NF=['123789'] peso=['2.310,75']
email_05_op24546.txt     OP=['24546'] NF=['123790'] peso=['1.100']
  (email_06_op24533.txt não é UTF-8: lendo como cp1252)
email_06_op24533.txt     OP=['24533'] NF=['123801'] peso=['860,4']
email_07_sem_nf.txt      OP=['24555'] NF=[] peso=[]
email_08_duas_ops.txt    OP=['24520', '24521'] NF=['123805'] peso=['3.200']
```

O e-mail 06 foi salvo no Windows em cp1252. Ler com plano B (`UnicodeDecodeError` →
tenta cp1252) é a lição do módulo 05 aplicada. E o e-mail 07 mostra por que a regex de
peso exige a palavra "peso": "(1.500 kg)" no meio da frase não é um campo confiável.

## 8. Saídas e orquestração (etapas 11 a 14)

### 8.1 A triagem (etapa 11)

É a camada de serviço: não lê arquivo, só chama as peças na ordem certa.

```text
pedido ─> OP existe? uma vez só? ──não──> bloqueado ("OP não encontrada" / "aparece 2 vezes")
            │sim
            ▼
          linha bate com a aba? ───não──> bloqueado (linha divergente)
            │sim
            ▼
          especificação conhecida? ─não─> bloqueado (especificação não cadastrada)
            │sim
            ▼
          valida tolerâncias + liberação (junta TODOS os motivos)
            │
            ├── nenhum motivo ──> fila ("emitir")
            └── algum motivo ──> bloqueado (com os motivos)
```

As três primeiras checagens **param** no primeiro problema: sem saber qual OP ou qual
especificação, não há o que validar. A última junta tudo. Uma função auxiliar com
**retornos antecipados** deixa cada caso em uma linha.

> 💡 **Dica:** antes do laço, monte um índice `{op: [medições]}`. Cada pedido acha a
> sua OP direto, sem varrer a planilha inteira. E o caso "OP repetida" aparece de graça:
> é a lista com dois itens.

### 8.2 O emissor e o modo ensaio (etapa 12)

O sistema não sabe o que é TOTVS. Ele conhece uma interface:

```python
class Emissor:
    """Interface: todo emissor tem `ensaio` e `emitir(item) -> comprovante`."""

    ensaio: bool = False

    def emitir(self, item: ItemFila) -> str:
        raise NotImplementedError
```

O `EmissorTotvs` de hoje só tem o modo ensaio: registra o que faria e devolve
`"ENSAIO-24518-123456"`. A função `emitir_fila` cuida do resto: idempotência por
(OP, NF), falha de uma OP vira "falha" e a série segue, bug sobe. O exemplo
`exemplos/07_logging_e_modo_ensaio.py` mostra o padrão em miniatura:

```text
python exemplos/07_logging_e_modo_ensaio.py
INFO     ENSAIO: emitiria certificado da OP 24518 / NF 123456
INFO     ENSAIO: emitiria certificado da OP 24541 / NF 123789
WARNING  OP 24518 / NF 123456 repetida: ignorada
```

> 🔮 **Preveja antes de rodar:** `replace` copia o item trocando a situação. Depois
> mexemos na lista do ORIGINAL.
>
> ```python
> from dataclasses import dataclass, field, replace
>
>
> @dataclass
> class ItemFila:
>     op: str
>     situacao: str
>     motivos: list[str] = field(default_factory=list)
>
>
> original = ItemFila("24518", "emitir")
> copia = replace(original, situacao="falha")
> original.motivos.append("tela não respondeu")
> print(copia.situacao, copia.motivos)
> ```

<details><summary>Resposta</summary>

```text
falha ['tela não respondeu']
```

`replace` faz cópia **rasa**: a cópia aponta para a mesma lista. Por isso a etapa 12
monta uma lista nova (`item.motivos + ["..."]`) em vez de dar `append` no item
recebido. Mexer no que você recebeu é efeito colateral escondido.

</details>

### 8.3 O relatório da série (etapa 13)

CSV para o Excel brasileiro: separador `;`, vírgula decimal (`f"{1250.5:.2f}".replace(".", ",")`
dá `1250,50`) e encoding `utf-8-sig`. Sem o BOM do `-sig`, o Excel mostra
"EspecificaÃ§Ã£o" no cabeçalho. E `newline=""` no `open`, senão aparece uma linha em
branco entre os registros no Windows.

O projeto completo grava também um Excel formatado, com três abas (Série, E-mails fora
do padrão, Resumo) e um gráfico de barras nativo na aba Resumo.

### 8.4 A CLI (etapa 14)

A CLI é fina: lê argumentos, confere se os arquivos existem, chama quem faz o trabalho
e mostra o resumo. Quem faz o trabalho chega por parâmetro (`executar`). Nos testes,
entra um dublê que só anota a chamada; no projeto completo, a série real. Isso se chama
**injeção de dependência**, e é o que deixa a CLI testável sem planilha, banco ou
TOTVS.

O **código de saída** (`return 0` ou `return 1`) é a forma de um programa avisar outro
programa. O Agendador de Tarefas do Windows e o GitHub Actions leem esse número:
diferente de zero significa "precisa de gente".

> 🔧 **Modifique:** depois de passar na etapa 14, acrescente a opção `--quieto`, que
> não imprime o resumo (útil no agendador). Escreva o teste primeiro.

## 9. Montagem final: o projeto-completo

A pasta `projeto-completo/` é o sistema montado como um projeto independente: copie a
pasta para fora do curso e ela funciona sozinha.

```text
projeto-completo/
  pyproject.toml          metadados, dependências, comando "validador", pytest e ruff
  README.md               o que é, como instalar e usar (a vitrine do repositório)
  .gitignore              saida/, .venv/, .env e bancos que não são de exemplo
  .github/workflows/      testes.yml: lint + testes + série de exemplo a cada push
  sql/schema.sql          schema do banco de regras
  dados/                  planilha, banco e e-mails de exemplo (fictícios)
  src/validador_certificados/
    modelos.py  texto.py  regras.py              <- núcleo puro
    banco.py  planilha.py  expedicao.py          <- bordas de entrada
    fila.py  serie.py                            <- serviço
    emissao.py  robo_playwright.py  historico.py  relatorio.py   <- bordas de saída
    cli.py  __main__.py                          <- entrada
  tests/                  77 testes: unidade e ponta a ponta sobre dados/
```

**Por que `src/`?** Com o pacote dentro de `src`, os testes só enxergam o código depois
de instalado. Parece burocracia, mas garante que o que você testa é o que o usuário
instala, e não um arquivo solto que por acaso estava na pasta.

Os trechos principais do `pyproject.toml`:

```toml
[project]
name = "validador-certificados"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["openpyxl>=3.1"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.6"]
robo = ["playwright>=1.40"]

[project.scripts]
validador = "validador_certificados.cli:main"
```

`[project.scripts]` cria o comando `validador` no ambiente virtual. Os extras separam o
que é obrigatório (openpyxl) do que é só para desenvolver (`dev`) ou para o robô
(`robo`): o PC da expedição não precisa de pytest.

**Instalar e rodar** (PowerShell, dentro de `projeto-completo`):

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
validador --planilha dados/planilha_valores.xlsx --regras dados/regras.db --emails dados/emails
```

No Linux/macOS, ative com `source .venv/bin/activate`. A saída abaixo é do Linux (no
Windows, os caminhos aparecem com `\`), e o carimbo de data e hora muda a cada
execução:

```text
INFO     série iniciada em modo ENSAIO
INFO     regras: 7 especificações carregadas de dados/regras.db
INFO     planilha: 16 OPs lidas de dados/planilha_valores.xlsx
INFO     expedição: 8 e-mails lidos de dados/emails
WARNING  e-mail fora do padrão: email_07_sem_nf.txt (NF não encontrada; peso não encontrado)
WARNING  e-mail fora do padrão: email_08_duas_ops.txt (mais de uma OP no e-mail (24520, 24521))
INFO     triagem: 2 para emitir, 4 bloqueados
WARNING  OP 24519 bloqueada: espessura 44.8 fora de 40 ± 10% (36 a 44)
WARNING  OP 24527 bloqueada: COF sem liberação na observação
WARNING  OP 24546 bloqueada: especificação 'ESP-9999' não cadastrada
WARNING  OP 24533 bloqueada: linha informada C diferente da aba Linha B
INFO     ENSAIO: emitiria certificado: OP 24518 | NF 123456 | 1250.50 kg | PADRAO-A
INFO     ENSAIO: emitiria certificado: OP 24541 | NF 123789 | 2310.75 kg | ESP-0412
INFO     relatórios gravados: relatorio_2026-10-29_024641.xlsx e relatorio_2026-10-29_024641.csv
Série processada em modo ENSAIO (nada foi enviado ao TOTVS)
  bloqueado                 4
  ensaio                    2
  e-mails fora do padrão    2
Relatório: saida/relatorio_2026-10-29_024641.xlsx
```

Sem instalar nada, `python exemplos/08_serie_de_ponta_a_ponta.py` (na pasta
`14-projeto-final`) roda a mesma série sobre os dados do módulo.

**Logging em dois destinos.** O terminal mostra INFO (ou DEBUG com `-v`); o arquivo
`saida/validador.log` guarda sempre DEBUG, com data e hora. Quando alguém perguntar
"por que a OP 24527 não saiu na terça?", a resposta está no log. Cada módulo cria o
seu `logger = logging.getLogger(__name__)`, e só a CLI configura os destinos.

**Testes e qualidade** (dentro de `projeto-completo`, com o ambiente ativado):

```text
python -m pytest
ruff check .
ruff format --check .
```

```text
........................................................................ [ 93%]
.....                                                                    [100%]
77 passed in 0.44s
```

O teste mais valioso é o de ponta a ponta (`tests/test_cli.py`): roda a CLI sobre
`dados/` numa pasta temporária e confere o resumo, os arquivos gerados e que o ensaio
não gravou histórico. Se ele passa, o sistema inteiro funciona.

## 10. O robô do TOTVS, isolado

O robô é a parte mais frágil: depende de uma tela que muda sem aviso. Por isso ele fica
**atrás da interface** `Emissor`, e o resto do sistema nem sabe que ele existe.

O arquivo `src/validador_certificados/robo_playwright.py` é um **esqueleto** comentado
(não testado automaticamente): a classe `EmissorTotvsPlaywright` com login, emissão,
print de tela e tradução de erro. O coração dele:

```python
def emitir(self, item: ItemFila) -> str:
    from playwright.sync_api import TimeoutError as TempoEsgotado

    pagina = self._pagina
    try:
        # AJUSTE: caminho até a rotina de certificado de qualidade
        pagina.get_by_role("menuitem", name="Certificado de Qualidade").click()
        pagina.get_by_label("Ordem de Produção").fill(item.op)
        pagina.get_by_label("Nota Fiscal").fill(item.nf)
        pagina.get_by_label("Peso").fill(f"{item.peso_kg:.2f}".replace(".", ","))
        pagina.get_by_role("button", name="Confirmar").click()
        comprovante = pagina.get_by_test_id("numero-certificado").inner_text()
    except TempoEsgotado as erro:
        self._print_de_tela(f"falha_{item.op}_{item.nf}")
        raise ErroEmissao(f"tela não respondeu: {erro}") from erro
    self._print_de_tela(f"ok_{item.op}_{item.nf}")
    return comprovante
```

**Roteiro para implementar quando tiver acesso à tela:**

1. `python -m pip install -e ".[robo]"`. O Edge já vem no Windows; o Playwright o usa
   com `channel="msedge"`.
2. Grave seus cliques uma vez: `playwright codegen --channel msedge <endereço do TOTVS>`.
   O codegen mostra os seletores de cada campo.
3. Troque os seletores marcados com `AJUSTE`. Prefira `get_by_role`, `get_by_label` e
   `get_by_text`. Se a tela estiver dentro de um iframe, use `frame_locator`.
4. Usuário e senha em variáveis de ambiente (`TOTVS_USUARIO`, `TOTVS_SENHA`) ou num
   `.env` lido com python-dotenv. **Nunca** no código, nunca no Git.
5. Rode em **homologação** (base de teste) com o navegador visível. Só depois em
   produção, e por algumas semanas comparando com a emissão manual.
6. Na CLI, troque `EmissorTotvs(ensaio=False)` pelo novo emissor quando `--emitir` for
   passado. Nada mais no sistema muda: esse é o prêmio da interface.

> ⚠️ **Erro comum:** usar `time.sleep(5)` para "esperar a tela". Ora é pouco (falha),
> ora é demais (lento). O Playwright espera sozinho o elemento ficar pronto; ajuste só
> o tempo máximo (`set_default_timeout`).

## 11. Do curso para o trabalho

1. **Troque os dados.** Copie a planilha real para uma pasta local e rode com `-v`. Se
   faltar coluna, a mensagem diz qual. Se o cabeçalho tiver outro nome, ajuste
   `chave_coluna` ou a planilha (combine com o laboratório).
2. **Cadastre as regras.** Abra `regras.db` no DB Browser for SQLite e cadastre os
   padrões das 4 linhas e as especificações de cliente. Comece pelos clientes com mais
   pedidos.
3. **Rode em paralelo.** Por duas semanas, faça a emissão manual como sempre e rode o
   sistema em ensaio. Compare o relatório com o que você decidiu. Cada diferença é um
   bug ou uma regra que faltou.
4. **Agende.** Um arquivo `rodar_serie.bat` e o Agendador de Tarefas do Windows
   (módulo 12) rodam a série toda manhã:

   ```text
   @echo off
   cd /d C:\automacoes\validador
   call .venv\Scripts\activate
   validador --planilha "\\servidor\qualidade\valores.xlsx" --regras dados\regras.db --emails C:\automacoes\emails --saida saida
   ```

5. **Guarde o histórico.** A pasta `saida/` acumula relatórios e log. Faça backup dela
   junto com o `regras.db`.

> 💡 **Dica:** mostre o relatório de ensaio para o seu gestor antes de pedir acesso ao
> TOTVS para o robô. Um relatório certo por duas semanas é o melhor argumento.

## 12. Portfólio no GitHub

O `projeto-completo/` foi feito para virar o seu repositório. Passo a passo:

1. **Repositório próprio.** Copie a pasta para fora do curso (ex.:
   `C:\projetos\validador-certificados`) e, dentro dela:

   ```text
   git init
   git add .
   git commit -m "Versão inicial do Validador de Certificados"
   ```

   Crie o repositório vazio no site do GitHub (sem README) e siga as instruções de
   `git remote add origin ...` e `git push -u origin main` que ele mostra.

2. **README com prints.** Rode a série, tire prints (Windows: `Win+Shift+S`) do terminal
   e da aba "Série" do relatório, salve em `docs/img/` e cite no README:
   `![Relatório da série](docs/img/relatorio.png)`. Um recrutador decide em 30
   segundos; a imagem faz isso por você.
3. **Testes no GitHub Actions.** O arquivo `.github/workflows/testes.yml` já roda lint,
   testes e a série de exemplo no Windows e no Ubuntu a cada push. Depois do primeiro
   push, veja a aba **Actions**. Acrescente o selo no topo do README:
   `![testes](https://github.com/SEU_USUARIO/validador-certificados/actions/workflows/testes.yml/badge.svg)`.
4. **Só dados fictícios.** Nunca suba a planilha real, clientes, OPs ou o banco de
   produção. O `.gitignore` já barra `saida/` e `.env`. Na dúvida, não suba.
5. **Commits que contam a história.** Um commit por etapa ("Regra de tolerância
   nominal com limites arredondados") mostra como você pensa. Use branches para as
   extensões (módulo 09).
6. **Divulgue.** Fixe o repositório no seu perfil e escreva um post curto no LinkedIn:
   o problema, a solução, um print, o link.

## 13. Extensões

**13.1 Robô Playwright no TOTVS.** Seção 10. É a extensão que mais economiza tempo e a
que exige mais cuidado.

**13.2 Ler os e-mails direto do Outlook.** Hoje a série lê `.txt`. No Outlook clássico
do Windows, dá para ler uma pasta da caixa com `pywin32` (módulo 12, só Windows):

```python
import win32com.client  # python -m pip install pywin32

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
caixa = outlook.GetDefaultFolder(6)  # 6 = Caixa de Entrada
pasta = caixa.Folders.Item("Certificados")
emails = {}
for mensagem in pasta.Items:
    if mensagem.UnRead:
        emails[f"{mensagem.EntryID[-12:]}.txt"] = f"{mensagem.Subject}\n{mensagem.Body}"
```

O dicionário `{nome: texto}` é exatamente o que `separar_emails` recebe. Só a borda
muda; a regra de e-mail continua a mesma. (No Outlook novo e no Microsoft 365, o
caminho é a API Microsoft Graph, que pede autorização da TI.)

**13.3 API com FastAPI.** É o desafio deste módulo: outra porta de entrada para o mesmo
núcleo, para o PCP consultar se uma OP pode ter certificado.

**13.4 Outras ideias.** Aviso por e-mail ao supervisor quando houver bloqueio; um
gráfico de controle das espessuras por linha com matplotlib (módulo 10); guardar cada
série num banco para medir o tempo entre o pedido e a emissão.

## Lendo mensagens de erro deste módulo

**Pacote não encontrado.** Você rodou os testes ou o comando sem instalar o projeto, ou
com o ambiente virtual errado ativado.

```text
    from validador_certificados.cli import main
ModuleNotFoundError: No module named 'validador_certificados'
```

Correção: ative o `.venv` e rode `python -m pip install -e ".[dev]"` na pasta do
projeto.

**Banco errado.** O caminho do banco estava errado e o `sqlite3.connect` criou um
banco vazio.

```text
    conexao.execute("SELECT titulo FROM especificacao")
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: especificacao
```

Correção: confira o caminho; apague o `.db` vazio criado por engano; abra com
`?mode=ro`.

**Formato de planilha.** openpyxl só lê `.xlsx` (e parentes). Um `.xls` antigo ou um
`.csv` dão:

```text
openpyxl.utils.exceptions.InvalidFileException: openpyxl does not support .csv file format, please check you can open it with Excel first. Supported formats are: .xlsx,.xlsm,.xltx,.xltm
```

Correção: abra no Excel e salve como `.xlsx`.

**Coluna faltando.** O erro é nosso, de propósito, e diz a aba e as colunas:

```text
validador_certificados.modelos.PlanilhaInvalida: aba 'Linha B': faltam colunas: cof, observacao
```

Correção: alguém renomeou ou apagou a coluna. Repare que o cabeçalho "Obs" não vale
como "Observação".

**Regra quebrada no banco.** A `Tolerancia` recusa nascer:

```text
    raise ValueError(f"{self.caracteristica}: mínimo maior que o máximo")
ValueError: cof: mínimo maior que o máximo
```

Correção: o cadastro inverteu mínimo e máximo. O sistema para em vez de validar com
regra errada.

**Argumento faltando.** O argparse explica sozinho e sai com código 2:

```text
usage: validador [-h] --planilha PLANILHA --regras REGRAS --emails EMAILS
                 [--saida SAIDA] [--emitir] [-v] [--version]
validador: error: the following arguments are required: --regras, --emails
```

**Arquivo aberto no Excel (Windows).** Gravar um relatório com o mesmo nome de um que
está aberto no Excel dá `PermissionError: [Errno 13] Permission denied`. A CLI trata
como erro esperado (código 1). Correção: feche o arquivo; por isso cada série grava um
relatório com data e hora no nome.

## Boas práticas

- **Núcleo puro, bordas finas.** Se uma regra precisa de `open()`, ela está no lugar
  errado.
- **Nunca chutar.** Dado ambíguo vira pendência com motivo legível.
- **Modo seguro por padrão.** Ação perigosa exige pedido explícito (`--emitir`).
- **Idempotência.** Rodar duas vezes dá o mesmo resultado que rodar uma.
- **Capture só o erro esperado.** `except ErroEmissao`, nunca `except Exception` para
  esconder.
- **Log com contexto.** "OP 24527 bloqueada: COF sem liberação" ajuda; "erro" não.
- **Dados de exemplo versionados**, gerados por script, com um caso de cada tipo.
- **Teste de ponta a ponta** sobre esses dados, rodando no CI a cada push.
- **Segredos fora do código**: variável de ambiente ou `.env` no `.gitignore`.
- **Decisões escritas**: o porquê vale tanto quanto o como.

## No mundo real

**Sexta-feira, 16h, expedição cheia.** Chegaram 8 e-mails pedindo certificado. Você
roda:

```text
validador --planilha dados/planilha_valores.xlsx --regras dados/regras.db --emails dados/emails
```

Em um segundo, o resumo: 2 para emitir, 4 bloqueados, 2 e-mails fora do padrão. Você
abre o relatório e decide, linha a linha:

| Item | O sistema disse | O que você faz |
|---|---|---|
| OP 24518 e 24541 | ensaio (seria emitido) | emite no TOTVS (ou deixa o robô emitir, no futuro) |
| OP 24519 | espessura 44,8 fora de 40 ± 10% | avisa a produção; não há certificado para OP reprovada |
| OP 24527 | COF sem liberação | pergunta ao laboratório quando sai o ensaio de 24 h |
| OP 24546 | especificação ESP-9999 não cadastrada | confere o pedido do cliente e cadastra (ou corrige a planilha) |
| OP 24533 | linha C digitada na aba B | corrige a planilha com quem lançou |
| e-mail 07 | NF e peso não encontrados | responde à expedição pedindo a NF |
| e-mail 08 | duas OPs no mesmo e-mail | pede um e-mail por OP (ou implementa a extensão) |

O que levava uma hora de conferência virou dez minutos de **decisão**. Repare: o
sistema não decidiu nada que não devia. Tudo o que era ambíguo voltou para uma pessoa,
com o motivo escrito.

É essa história que você conta na entrevista.

## Resumo

| Tema | Essência |
|---|---|
| Camadas | núcleo puro (modelos, regras) ← serviço (fila) ← bordas (banco, planilha, e-mail, TOTVS, relatório) ← CLI |
| Modelo que se defende | `@dataclass` + `__post_init__` levantando `ValueError` |
| Regra | devolve `None` (passou) ou o motivo (`str`) |
| Tolerância nominal | `round(nominal ∓ nominal * pct / 100, 4)`, limites inclusivos |
| Especificação | vazio → padrão; conhecida → `{**padrao, **cliente}`; desconhecida → exceção |
| Liberação | normalizar + `re.search(r"\bcof\s*[:-]?\s*liberad[oa]\b", texto)` |
| Planilha | `load_workbook(..., read_only=True, data_only=True)`, cabeçalho → dict, `close()` |
| E-mails | `findall` + `set` + `sorted`; dois valores diferentes = fora do padrão |
| Emissão | interface `Emissor`; ensaio por padrão; chave `(OP, NF)`; `except ErroEmissao` |
| Relatório | CSV `;` + `utf-8-sig` + `newline=""`; Excel com openpyxl |
| CLI | argparse, `executar` injetado, código de saída 0/1 |
| Projeto | src layout, `pip install -e ".[dev]"`, pytest, ruff, GitHub Actions |

## Você domina este módulo se...

- [ ] Desenho as camadas do Validador de memória e explico a regra de dependência.
- [ ] Explico, sem consultar, por que as regras devolvem motivo em vez de booleano.
- [ ] Mostro com um exemplo por que os limites da tolerância nominal são arredondados.
- [ ] Explico a diferença entre `{**padrao, **cliente}` e `{**cliente, **padrao}` e qual
      a consequência de trocar.
- [ ] Dou três exemplos de "nunca chutar" no sistema e digo o que acontece em cada um.
- [ ] Explico por que a chave de idempotência é (OP, NF) e por que capturo só
      `ErroEmissao`.
- [ ] Instalo o projeto-completo num ambiente virtual novo, rodo os testes e a série de
      exemplo sem olhar o README.
- [ ] Sei o que mudar (e o que NÃO mudar) para trocar o emissor de ensaio pelo robô.

## Exercícios

Cada exercício é uma etapa do sistema, em ordem de construção. Juntos, eles já são a
revisão integrada do curso: cada etapa usa assuntos de vários módulos anteriores.

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_modelos` | ★☆☆ | dataclasses, `__post_init__`, `@property` (módulo 08) |
| 02 | `ex02_carregar_regras` | ★★☆ | sqlite3, consultas, montar objetos (módulos 08 e 11) |
| 03 | `ex03_tolerancia_fixa` | ★☆☆ | regra pura, `None` × motivo, `:g` (módulos 01, 02 e 04) |
| 04 | `ex04_tolerancia_nominal` | ★☆☆ | float no limite, `round`, tupla (módulos 01 e 03) |
| 05 | `ex05_validar_op` | ★★☆ | laço sobre a especificação, juntar motivos (módulos 02 a 04) |
| 06 | `ex06_liberacao` | ★★☆ | leitura de código: prever e consertar; unicodedata, regex (módulo 05) |
| 07 | `ex07_ler_planilha` | ★★★ | openpyxl, cabeçalho → dict, conversões, `finally` (módulos 06 e 10) |
| 08 | `ex08_conferir_linha` | ★☆☆ | `re.fullmatch`, mensagens de pendência (módulo 05) |
| 09 | `ex09_escolher_especificacao` | ★★☆ | `{**a, **b}`, exceção personalizada, "nunca chutar" (módulos 03 e 06) |
| 10 | `ex10_emails_expedicao` | ★★☆ | regex, número BR, juntar problemas (módulos 05 e 06) |
| 11 | `ex11_fila_emissao` | ★★★ | camada de serviço, índice, retornos antecipados (módulos 03, 04 e 06) |
| 12 | `ex12_emissor_ensaio` | ★★★ | interface, herança, idempotência, `replace` (módulos 08 e 12) |
| 13 | `ex13_relatorio_serie` | ★☆☆ | `Counter`, CSV no padrão Excel BR (módulos 06 e 07) |
| 14 | `ex14_cli` | ★★☆ | argparse, injeção de dependência, código de saída (módulos 07 e 09) |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError` e rode, na pasta `curso-python`:

```text
python curso.py testar 14 ex01
```

Para testar o módulo inteiro: `python curso.py testar 14`.

## Desafio do módulo

**A API do Validador (extensão FastAPI).** Uma API com `/saude`, `/especificacoes`,
`/especificacoes/{titulo}` e `POST /validar`, que importa o núcleo do
`projeto-completo` sem reescrever regra nenhuma, com testes no `TestClient`.
Enunciado completo em [desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou: [quiz.md](quiz.md).

## Para ir além

- dataclasses: https://docs.python.org/pt-br/3/library/dataclasses.html
- argparse (tutorial): https://docs.python.org/pt-br/3/howto/argparse.html
- logging (tutorial): https://docs.python.org/pt-br/3/howto/logging.html
- sqlite3: https://docs.python.org/pt-br/3/library/sqlite3.html
- Empacotamento com pyproject.toml (guia oficial, em inglês):
  https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- Playwright para Python, gerador de código (em inglês):
  https://playwright.dev/python/docs/codegen
- GitHub Actions para Python (em inglês):
  https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python
- Leitura extra: "Arquitetura Hexagonal" (Ports and Adapters), de Alistair Cockburn: o
  nome formal da ideia "núcleo puro e bordas" deste módulo.
