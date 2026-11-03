# Módulo 11 — Bancos de dados e SQL (SQLite)

> **Tempo estimado:** 10 a 14 horas · **Pré-requisitos:** módulos 00 a 10 · **Nível:** intermediário

## O que você vai aprender

- Explicar tabela, linha, coluna, chave primária e chave estrangeira com exemplos do
  laboratório.
- Conectar num banco SQLite com `sqlite3`, executar comandos e ler resultados
  (`fetchone`, `fetchall`, `for`).
- Criar tabelas com tipos e restrições (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`,
  `REFERENCES`) e entender o `IntegrityError`.
- Inserir dados **sempre** com parâmetros (`?` e `:nome`), um por vez ou com
  `executemany`.
- Escrever `SELECT` com `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, `LIKE`, `IS NULL` e
  `CASE`.
- Resumir com `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY` e `HAVING`.
- Juntar tabelas com `INNER JOIN` e `LEFT JOIN` e achar "quem não tem par".
- Usar subconsultas (`IN`, `EXISTS`, escalar) e CTEs (`WITH`).
- Alterar e apagar com `UPDATE`/`DELETE` sem desastre, e agrupar alterações numa
  transação (`commit`, `rollback`, `with`).
- Demonstrar um ataque de SQL injection e escrever a versão segura.
- Modelar o banco de regras do projeto final (linhas, especificações, tolerâncias).
- Levar o resultado de uma consulta para o pandas com `read_sql`.

## Por que isso importa

Planilha é ótima para uma pessoa. Quando vários programas e várias pessoas precisam dos
mesmos dados, com regras que não podem ser quebradas, entra o **banco de dados**. O ERP
TOTVS Protheus que você usa todo dia é, por baixo, um banco de dados relacional enorme.

SQL é a habilidade técnica mais pedida em vagas de dados: analista, engenheiro, BI,
analytics engineering. Ela aparece até em vagas de automação e backend. E é uma das
mais estáveis: o SQL que você aprende hoje é praticamente o mesmo de 30 anos atrás e
vale em SQLite, PostgreSQL, SQL Server, Oracle e BigQuery.

No projeto final (módulo 14), as regras de conferência (padrão de cada linha,
especificações de cliente e tolerâncias) ficam num banco SQLite. Na seção 15 você vai
entender cada decisão daquele banco.

## 1. O que é um banco de dados relacional

Um banco relacional guarda dados em **tabelas**. Cada tabela é parecida com uma aba do
Excel, com uma diferença importante: as colunas têm **tipo** e **regras**, e o banco
obriga todo mundo a respeitá-las.

```text
tabela op                                         tabela cliente
┌────────┬───────┬────────────┬──────────┐        ┌────┬────────────────────────┐
│ numero │ linha │ cliente_id │ status   │        │ id │ nome                   │
├────────┼───────┼────────────┼──────────┤        ├────┼────────────────────────┤
│ 24518  │ A     │ 1 ─────────┼──────────┼──────► │ 1  │ Torrefação Serra Ltda  │
│ 24520  │ A     │ 2 ─────────┼──────────┼──────► │ 2  │ Agro Campo S.A.        │
└────────┴───────┴────────────┴──────────┘        └────┴────────────────────────┘
   ▲ chave primária    ▲ chave estrangeira           ▲ chave primária
```

- **Linha** (registro): uma OP, um cliente, um ensaio.
- **Coluna** (campo): uma informação de todas as linhas, com um tipo.
- **Chave primária** (*primary key*, PK): a coluna que identifica cada linha sem
  ambiguidade. Não repete e não fica vazia. Na `op`, é o `numero`.
- **Chave estrangeira** (*foreign key*, FK): uma coluna que aponta para a PK de outra
  tabela. O `cliente_id` da OP aponta para o `id` do cliente. O banco recusa uma OP de
  um cliente que não existe.

Por que não guardar o **nome** do cliente direto na OP? Porque, se a Torrefação Serra
mudar de razão social, você teria que corrigir em 500 OPs (e uma ia escapar). Com a FK,
o nome mora num lugar só. Essa ideia (cada informação num lugar, ligada por chaves) se
chama **normalização**, e é o "relacional" do nome.

**SQL** (*Structured Query Language*) é a linguagem para conversar com o banco. Você
diz **o que** quer ("as OPs da linha A com mais de 4 t"), e o banco descobre **como**
buscar.

**SQLite** é um banco inteiro num arquivo só (`.db`), sem servidor para instalar, e já
vem com o Python (módulo `sqlite3`). Está dentro do seu celular, do navegador e de
milhares de programas. Para olhar um `.db` com mouse, instale o **DB Browser for
SQLite** (gratuito). Bancos "de servidor", como PostgreSQL e SQL Server, usam o mesmo
SQL; muda a forma de conectar.

## 2. Primeira conexão com sqlite3

O ciclo é sempre: **conectar → executar → (commit) → fechar**. De
`exemplos/01_primeira_conexao.py`:

```python
import sqlite3

conexao = sqlite3.connect(":memory:")  # banco só na memória; para arquivo: "lab.db"
conexao.execute("CREATE TABLE bobina (id INTEGER PRIMARY KEY, op INTEGER, peso_kg REAL)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24518, 1250.5)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24518, 980.0)")
conexao.execute("INSERT INTO bobina (op, peso_kg) VALUES (24519, 1100.0)")
conexao.commit()  # grava de verdade

cursor = conexao.execute("SELECT id, op, peso_kg FROM bobina")
print(cursor.fetchall())
conexao.close()
```

```text
[(1, 24518, 1250.5), (2, 24518, 980.0), (3, 24519, 1100.0)]
```

- `sqlite3.connect(caminho)` abre o arquivo (e **cria** um vazio se ele não existir).
  `":memory:"` é um banco temporário, ótimo para testar.
- `conexao.execute(sql)` roda um comando e devolve um **cursor**: um "marcador" que
  percorre o resultado.
- Cada linha do resultado chega como **tupla**, na ordem das colunas do `SELECT`.
- `commit()` confirma as alterações. Sem ele, outro programa não enxerga os dados, e
  eles se perdem se o programa terminar.
- O `id INTEGER PRIMARY KEY` foi numerado sozinho: 1, 2, 3.

> 🔮 **Preveja antes de rodar:** o resultado tem duas linhas da OP 24518. O que os três
> `print` mostram?

```python
cursor = conexao.execute("SELECT op, peso_kg FROM bobina WHERE op = 24518")
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())
```

<details><summary>Resposta</summary>

```text
(24518, 1250.5)
(24518, 980.0)
None
```

`fetchone()` devolve a **próxima** linha e avança o marcador. Quando as linhas acabam,
devolve `None`. Por isso `fetchone()` é o jeito de perguntar "existe?" (se veio `None`,
não existe).
</details>

O cursor também pode ser percorrido com `for`, sem carregar tudo na memória de uma vez:

```python
for op, peso in conexao.execute("SELECT op, peso_kg FROM bobina"):
    print(op, peso)
```

> 💡 **Dica:** no Windows, `sqlite3.connect("lab.db")` cria o arquivo na pasta **de onde
> você rodou o comando**, não na pasta do script. Use caminhos com `pathlib` a partir de
> `Path(__file__)`, como no módulo 06.

## 3. Criando tabelas: tipos e restrições

```sql
CREATE TABLE nome_da_tabela (
    coluna1 TIPO RESTRIÇÕES,
    coluna2 TIPO RESTRIÇÕES,
    ...
);
```

Tipos do SQLite: `INTEGER` (inteiro), `REAL` (decimal), `TEXT` (texto), `BLOB` (bytes) e
o valor especial `NULL` (ausente). Não há tipo de data: guarde datas como `TEXT` no
formato ISO `'AAAA-MM-DD'`, que ordena e compara certo.

As **restrições** são regras de negócio que o banco passa a garantir, venha o dado de
onde vier (do seu script, de outro programa, de alguém no DB Browser). De
`exemplos/02_criar_tabelas_e_restricoes.py`:

```python
conexao.execute("PRAGMA foreign_keys = ON")  # no SQLite, FK só vale com isto!
conexao.executescript(
    """
    CREATE TABLE cliente (
        id   INTEGER PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE
    );
    CREATE TABLE op (
        numero        INTEGER PRIMARY KEY,
        cliente_id    INTEGER NOT NULL REFERENCES cliente (id),
        quantidade_kg REAL    NOT NULL CHECK (quantidade_kg > 0),
        status        TEXT    NOT NULL DEFAULT 'ABERTA'
    );
    """
)
```

| Restrição | Significa |
|---|---|
| `PRIMARY KEY` | identifica a linha: não repete |
| `NOT NULL` | obrigatório |
| `UNIQUE` | não repete (ex.: dois clientes com o mesmo nome) |
| `CHECK (condição)` | a condição precisa ser verdadeira |
| `DEFAULT valor` | valor usado quando o INSERT não informa a coluna |
| `REFERENCES tabela (coluna)` | chave estrangeira: o valor precisa existir lá |

Tentando quebrar cada regra, o banco responde com `sqlite3.IntegrityError`:

```text
NOT NULL     -> IntegrityError: NOT NULL constraint failed: cliente.nome
UNIQUE       -> IntegrityError: UNIQUE constraint failed: cliente.nome
CHECK        -> IntegrityError: CHECK constraint failed: quantidade_kg > 0
FOREIGN KEY  -> IntegrityError: FOREIGN KEY constraint failed
PRIMARY KEY  -> IntegrityError: UNIQUE constraint failed: op.numero
```

`executescript` roda vários comandos separados por `;` (o `execute` só aceita um).
`CREATE TABLE IF NOT EXISTS` não dá erro se a tabela já existir, e `DROP TABLE IF EXISTS
nome` apaga a tabela. Para ver as colunas de uma tabela: `PRAGMA table_info(op)`.

> ⚠️ **Erro comum:** esquecer o `PRAGMA foreign_keys = ON`. Por compatibilidade antiga, o
> SQLite vem com as chaves estrangeiras **desligadas**, e a FK vira enfeite. Ligue em
> **toda** conexão (ele não fica salvo no arquivo). Nossos scripts `.sql` já começam com
> ele.

> 🔮 **Preveja antes de rodar:** a coluna é `REAL`. O que o SQLite faz com `'12abc'`?

```python
conexao.execute("CREATE TABLE teste (valor REAL)")
conexao.execute("INSERT INTO teste VALUES ('12abc'), ('38.5'), (40)")
print(conexao.execute("SELECT valor, typeof(valor) FROM teste").fetchall())
```

<details><summary>Resposta</summary>

```text
[('12abc', 'text'), (38.5, 'real'), (40.0, 'real')]
```

Ele **aceita** e guarda como texto! O SQLite tem tipagem flexível: o tipo da coluna é
uma "preferência" (ele converte `'38.5'` e `40` para real), não uma regra. Para o tipo
ser regra de verdade, crie a tabela com `STRICT` no fim (SQLite 3.37+):
`CREATE TABLE teste (valor REAL) STRICT` recusa o `'12abc'` com
`IntegrityError: cannot store TEXT value in REAL column teste_estrito.valor`. Outra
opção é um `CHECK`. Bancos como PostgreSQL já são rígidos por padrão.
</details>

## 4. Inserindo dados com parâmetros

```sql
INSERT INTO tabela (coluna1, coluna2) VALUES (valor1, valor2);
```

No Python, os valores **nunca** são colados no texto do SQL. Eles vão separados, como
**parâmetros**. O `sqlite3` aceita dois estilos (`exemplos/03_inserir_com_parametros.py`):

```python
# Posicional: "?" e uma tupla, na mesma ordem
cursor = conexao.execute(
    "INSERT INTO expedicao (op, nf, peso_kg) VALUES (?, ?, ?)", (24518, "123456", 1250.5)
)
print("id gerado:", cursor.lastrowid)

# Nomeado: ":nome" e um dicionário
pedido = {"op": 24541, "nf": "123465", "peso": 2000.25}
conexao.execute("INSERT INTO expedicao (op, nf, peso_kg) VALUES (:op, :nf, :peso)", pedido)

# Muitas linhas: executemany com uma lista de tuplas
cargas = [(24520, "123458", 2400.0), (24521, "123459", 2950.0), (24518, "123470", 1830.0)]
cursor = conexao.executemany("INSERT INTO expedicao (op, nf, peso_kg) VALUES (?, ?, ?)", cargas)
print("linhas inseridas:", cursor.rowcount)
conexao.commit()
```

```text
id gerado: 1
linhas inseridas: 3
```

Por que parâmetros? Três motivos, do menos ao mais importante:

1. **Comodidade:** o `sqlite3` cuida das aspas, dos números, do `None` (vira `NULL`).
2. **Texto com apóstrofo:** `"Plásticos D'Ávila"` colado no SQL quebra o comando; como
   parâmetro, funciona.
3. **Segurança:** sem parâmetros, o texto do usuário vira **código** SQL. Isso é o SQL
   injection, que a seção 13 mostra na prática.

> ⚠️ **Erro comum:** um parâmetro só, sem vírgula. `conexao.execute(sql, 24518)` dá
> `ProgrammingError: parameters are of unsupported type`, e `(24518)` sem vírgula é só um
> número entre parênteses. O certo é `(24518,)`. Quantidade errada de valores dá
> `Incorrect number of bindings supplied. The current statement uses 2, and there are 1
> supplied.`

`cursor.lastrowid` é o id que acabou de ser gerado (útil para inserir os "filhos" logo
em seguida). `cursor.rowcount` é quantas linhas o comando afetou.

## 5. O banco do laboratório

A partir daqui, os exemplos usam um banco com cara de laboratório (dados fictícios),
definido em `dados/laboratorio.sql`:

```text
linha (codigo PK, descricao)
  ▲
  │ linha
op (numero PK, linha FK, cliente_id FK, produto, especificacao, emissao,
  │  quantidade_kg, status)             │
  │                                     ▼
  │                              cliente (id PK, nome, cidade, uf)
  ├──── ensaio (id PK, op FK, bobina, caracteristica, valor, resultado, data)
  └──── expedicao (id PK, op FK, nf, peso_kg, data)
```

São 4 linhas, 6 clientes, 12 OPs (outubro/2026), 60 ensaios (espessura, gramatura e COF
de 2 bobinas por OP; um ainda sem valor) e 8 cargas expedidas. O `status` da OP é
`ABERTA`, `LIBERADA`, `BLOQUEADA` ou `CERTIFICADA`; o `resultado` do ensaio é `OK` ou
`FORA`.

Para abrir no DB Browser, gere os arquivos `.db` (na pasta `curso-python`):

```text
python 11-banco-de-dados-e-sql/dados/montar_banco.py
```

Os exemplos montam o banco na memória com `abrir_banco_exemplo()` (cada exemplo começa
do zero) e imprimem os resultados como tabela com `mostrar(conexao, sql)`, ambas em
`exemplos/utilitarios.py`. Leia esse arquivo: ele usa `cursor.description`, que traz os
nomes das colunas do resultado.

> 💡 **Dica:** escreva as palavras do SQL em MAIÚSCULAS (`SELECT`, `WHERE`) e os nomes
> em minúsculas. O banco não liga, mas fica muito mais fácil de ler.

## 6. SELECT: escolher, filtrar, ordenar

A forma geral, na ordem em que se **escreve**:

```sql
SELECT colunas
FROM tabela
WHERE condição
ORDER BY colunas
LIMIT n;
```

De `exemplos/04_select_where_order.py`:

```sql
SELECT numero, produto, quantidade_kg / 1000 AS toneladas
FROM op
WHERE linha = 'A' AND quantidade_kg >= 4500
ORDER BY quantidade_kg DESC
```

```text
numero | produto                     | toneladas
-------+-----------------------------+----------
24521  | Filme PE 60 µm sacaria      | 6
24520  | Filme PE 50 µm branco       | 5.2
24518  | Filme PE 40 µm transparente | 4.5
(3 linhas)
```

- No `SELECT` cabem contas e **apelidos** (`AS toneladas`). `SELECT *` traz todas as
  colunas (bom para explorar, ruim em programa: se a tabela ganhar uma coluna, seu
  código quebra).
- Texto vai entre **aspas simples** (`'A'`). Aspas duplas, no SQL, são para nomes.
- `ORDER BY coluna DESC` ordena decrescente (`ASC`, o padrão, é crescente). Várias
  colunas: `ORDER BY emissao, numero`.
- `LIMIT 3` pega só as 3 primeiras linhas.

Os operadores do `WHERE`:

| Operador | Exemplo |
|---|---|
| `=`, `<>` (diferente), `<`, `<=`, `>`, `>=` | `status <> 'CERTIFICADA'` |
| `AND`, `OR`, `NOT` | `linha = 'A' AND quantidade_kg > 4000` |
| `BETWEEN a AND b` (inclui as pontas) | `emissao BETWEEN '2026-10-21' AND '2026-10-22'` |
| `IN (lista)` | `status IN ('LIBERADA', 'CERTIFICADA')` |
| `LIKE` (`%` = qualquer coisa, `_` = um caractere) | `produto LIKE '%PE 35%'` |
| `IS NULL`, `IS NOT NULL` | `valor IS NULL` |

```sql
SELECT numero, emissao, status
FROM op
WHERE emissao BETWEEN '2026-10-21' AND '2026-10-22'
  AND status IN ('LIBERADA', 'CERTIFICADA')
ORDER BY emissao, numero
```

```text
numero | emissao    | status
-------+------------+------------
24520  | 2026-10-21 | LIBERADA
24521  | 2026-10-21 | LIBERADA
24528  | 2026-10-22 | CERTIFICADA
(3 linhas)
```

`SELECT DISTINCT status FROM op` mostra cada status uma vez só. E `LIKE` no SQLite não
diferencia maiúsculas de minúsculas (para letras sem acento).

> 🔮 **Preveja antes de rodar:** existe um ensaio com `valor` NULL (o COF da bobina 2 da
> OP 24534). Quantas linhas esta consulta devolve?

```sql
SELECT op, bobina FROM ensaio WHERE valor = NULL
```

<details><summary>Resposta</summary>

```text
op | bobina
---+-------
(0 linhas)
```

**Nenhuma.** `NULL` significa "desconhecido", e "desconhecido = desconhecido" também é
desconhecido, nunca verdadeiro. Para testar ausência, use `valor IS NULL` (que acha o
ensaio pendente da OP 24534). Esse erro roda sem mensagem nenhuma: o resultado
simplesmente vem vazio.
</details>

> ⚠️ **Erro comum:** `AND` vem antes de `OR`. `uf = 'SP' OR uf = 'MG' AND cidade =
> 'Varginha'` significa `uf = 'SP' OR (uf = 'MG' AND cidade = 'Varginha')`. Na dúvida,
> **parênteses**.

**CASE** é o `if` do SQL, dentro do `SELECT`:

```sql
SELECT numero, especificacao,
       CASE WHEN especificacao IS NULL THEN 'padrão da linha'
            ELSE 'especificação do cliente' END AS regra
FROM op
WHERE linha = 'A'
```

```text
numero | especificacao | regra
-------+---------------+-------------------------
24518  | NULL          | padrão da linha
24519  | NULL          | padrão da linha
24520  | NULL          | padrão da linha
24521  | ESP-0533      | especificação do cliente
(4 linhas)
```

## 7. Agregação: GROUP BY e HAVING

Funções de agregação transformam muitas linhas em um número: `COUNT`, `SUM`, `AVG`,
`MIN`, `MAX` (`exemplos/05_agregacao_group_by.py`):

```sql
SELECT COUNT(*) AS ops, SUM(quantidade_kg) AS total_kg,
       ROUND(AVG(quantidade_kg), 1) AS media_kg,
       MIN(emissao) AS primeira, MAX(emissao) AS ultima
FROM op
```

```text
ops | total_kg | media_kg | primeira   | ultima
----+----------+----------+------------+-----------
12  | 45200    | 3766.7   | 2026-10-20 | 2026-10-27
(1 linha)
```

> 🔮 **Preveja antes de rodar:** há 20 ensaios de COF, e um deles está sem valor. O que
> sai?

```sql
SELECT COUNT(*) AS linhas, COUNT(valor) AS medidos
FROM ensaio
WHERE caracteristica = 'cof'
```

<details><summary>Resposta</summary>

```text
linhas | medidos
-------+--------
20     | 19
(1 linha)
```

`COUNT(*)` conta **linhas**; `COUNT(coluna)` conta valores **não nulos**. O mesmo vale
para `AVG`, `SUM`, `MIN` e `MAX`: todos ignoram NULL. (É a mesma ideia do `size()` x
`count()` do pandas.)
</details>

**GROUP BY** faz uma conta por grupo, como o `groupby` do pandas:

```sql
SELECT linha, COUNT(*) AS ops, SUM(quantidade_kg) AS total_kg
FROM op
GROUP BY linha
ORDER BY total_kg DESC
```

```text
linha | ops | total_kg
------+-----+---------
A     | 4   | 18700
D     | 3   | 11900
B     | 3   | 7900
C     | 2   | 6700
(4 linhas)
```

Regra prática: no `SELECT` de uma consulta agrupada, só entram as colunas do
`GROUP BY` e funções de agregação. Um truque útil: `SUM(CASE WHEN resultado = 'FORA'
THEN 1 ELSE 0 END)` conta quantas linhas atendem à condição (no SQLite, até
`SUM(resultado = 'FORA')` funciona, porque comparação vale 1 ou 0).

**WHERE x HAVING.** O `WHERE` filtra **linhas** antes de agrupar; o `HAVING` filtra
**grupos** depois:

```sql
SELECT op, COUNT(*) AS cargas, SUM(peso_kg) AS peso_total
FROM expedicao
WHERE data >= '2026-10-26'
GROUP BY op
HAVING COUNT(*) >= 2
ORDER BY op
```

```text
op    | cargas | peso_total
------+--------+-----------
24518 | 2      | 3080.5
24541 | 2      | 3750.25
(2 linhas)
```

Para entender o porquê, veja a ordem em que o banco **executa** (diferente da ordem em
que escrevemos):

```text
1. FROM / JOIN    de onde vêm as linhas
2. WHERE          filtra linhas
3. GROUP BY       forma os grupos
4. HAVING         filtra grupos
5. SELECT         calcula as colunas e apelidos
6. ORDER BY       ordena
7. LIMIT          corta
```

Por isso `WHERE COUNT(*) >= 2` dá erro (`misuse of aggregate function COUNT()`): no
passo 2, os grupos ainda não existem.

## 8. JOINs: juntando tabelas

A OP tem o `cliente_id`; o nome do cliente está em `cliente`. O `JOIN` junta as duas
pela condição do `ON` (`exemplos/06_joins.py`):

```sql
SELECT o.numero, c.nome AS cliente, o.produto
FROM op AS o
JOIN cliente AS c ON c.id = o.cliente_id
WHERE o.linha = 'D'
ORDER BY o.numero
```

```text
numero | cliente               | produto
-------+-----------------------+-----------------------
24541  | Torrefação Serra Ltda | Laminado PET/PE 62 µm
24546  | Laticínios Serra Azul | Laminado BOPP/PE 55 µm
24551  | Agro Campo S.A.       | Laminado PET/PE 62 µm
(3 linhas)
```

`op AS o` dá um apelido curto à tabela; `o.numero` diz de qual tabela vem a coluna
(obrigatório quando o nome existe nas duas, senão dá `ambiguous column name`).

```text
INNER JOIN (ou só JOIN)     LEFT JOIN
 cliente     op              cliente     op
  ┌───┐    ┌───┐              ┌───┐    ┌───┐
  │ ░░│████│░░ │              │███│████│░░ │
  └───┘    └───┘              └───┘    └───┘
 só o que casa              todos da esquerda; sem par,
 dos dois lados             colunas da direita = NULL
```

O mesmo `merge` do pandas (módulo 10): `how="inner"` e `how="left"`. Com `LEFT JOIN`, os
clientes de MG aparecem todos, mesmo o Café do Vale, que não tem OP:

```sql
SELECT c.nome, o.numero
FROM cliente AS c
LEFT JOIN op AS o ON o.cliente_id = c.id
WHERE c.uf = 'MG'
ORDER BY c.nome, o.numero
```

```text
nome                  | numero
----------------------+-------
Café do Vale          | NULL
Laticínios Serra Azul | 24527
Laticínios Serra Azul | 24546
(3 linhas)
```

**"Quem não tem"** é uma pergunta muito comum (OP sem ensaio, cliente sem pedido). A
receita é `LEFT JOIN` + `IS NULL` numa coluna da direita (o "anti-join"):

```sql
SELECT o.numero, o.status
FROM op AS o
LEFT JOIN ensaio AS e ON e.op = o.numero
WHERE e.id IS NULL
```

```text
numero | status
-------+-------
24550  | ABERTA
24551  | ABERTA
(2 linhas)
```

Dá para encadear vários JOINs e agregar no fim. Peso expedido por cliente (expedição →
OP → cliente):

```sql
SELECT c.nome AS cliente, COUNT(x.id) AS cargas, SUM(x.peso_kg) AS peso_kg
FROM expedicao AS x
JOIN op AS o ON o.numero = x.op
JOIN cliente AS c ON c.id = o.cliente_id
GROUP BY c.nome
ORDER BY peso_kg DESC
```

```text
cliente                | cargas | peso_kg
-----------------------+--------+--------
Torrefação Serra Ltda  | 4      | 6830.75
Agro Campo S.A.        | 2      | 5350
Higiene Bem-Estar S.A. | 2      | 2750.5
(3 linhas)
```

> 🔮 **Preveja antes de rodar:** queremos os clientes de MG e, ao lado, as OPs deles da
> linha B (ou NULL). O Café do Vale aparece?

```sql
SELECT c.nome, o.numero
FROM cliente AS c
LEFT JOIN op AS o ON o.cliente_id = c.id
WHERE c.uf = 'MG' AND o.linha = 'B'
```

<details><summary>Resposta</summary>

```text
nome                  | numero
----------------------+-------
Laticínios Serra Azul | 24527
(1 linha)
```

**Não aparece.** O `WHERE` roda **depois** do `LEFT JOIN`: na linha do Café do Vale,
`o.linha` é NULL, e `NULL = 'B'` não é verdadeiro. O `WHERE` jogou fora justamente quem
o `LEFT JOIN` tinha guardado. A condição sobre a tabela da direita vai no `ON`:

```sql
LEFT JOIN op AS o ON o.cliente_id = c.id AND o.linha = 'B'
WHERE c.uf = 'MG'
```

Agora sai `Laticínios Serra Azul | 24527` e `Café do Vale | NULL`. É um dos defeitos do
exercício 10.
</details>

## 9. Subconsultas e CTEs

Uma **subconsulta** é um `SELECT` dentro de outro. Leia de dentro para fora
(`exemplos/07_subconsultas_e_cte.py`).

**Escalar** (devolve um valor): OPs acima da média.

```sql
SELECT numero, quantidade_kg
FROM op
WHERE quantidade_kg > (SELECT AVG(quantidade_kg) FROM op)
ORDER BY quantidade_kg DESC
```

```text
numero | quantidade_kg
-------+--------------
24521  | 6000
24520  | 5200
24518  | 4500
24551  | 4100
24541  | 4000
24546  | 3800
(6 linhas)
```

**Com IN** (devolve uma lista): OPs com algum ensaio FORA.

```sql
SELECT numero, status
FROM op
WHERE numero IN (SELECT op FROM ensaio WHERE resultado = 'FORA')
```

```text
numero | status
-------+----------
24519  | BLOQUEADA
24527  | BLOQUEADA
24533  | BLOQUEADA
24546  | BLOQUEADA
(4 linhas)
```

**Com EXISTS / NOT EXISTS** (correlacionada: usa a linha de fora). Clientes sem OP:

```sql
SELECT nome
FROM cliente AS c
WHERE NOT EXISTS (SELECT 1 FROM op AS o WHERE o.cliente_id = c.id)
```

Resultado: só o `Café do Vale`.

> ⚠️ **Erro comum:** `WHERE id NOT IN (SELECT cliente_id FROM op)` parece igual, mas se
> a subconsulta trouxer **um** NULL, o `NOT IN` não devolve **nada** (de novo o
> "desconhecido"). Prefira `NOT EXISTS`.

**CTE** (`WITH`) dá nome a um passo intermediário. Consultas grandes ficam legíveis, de
cima para baixo, como funções pequenas em Python:

```sql
WITH situacao AS (
    SELECT op,
           SUM(resultado = 'FORA') AS fora,
           SUM(valor IS NULL) AS pendentes
    FROM ensaio
    GROUP BY op
)
SELECT o.numero, o.status, s.fora, s.pendentes
FROM op AS o
JOIN situacao AS s ON s.op = o.numero
WHERE s.fora > 0 OR s.pendentes > 0
ORDER BY o.numero
```

```text
numero | status    | fora | pendentes
-------+-----------+------+----------
24519  | BLOQUEADA | 1    | 0
24527  | BLOQUEADA | 1    | 0
24533  | BLOQUEADA | 2    | 0
24534  | ABERTA    | 0    | 1
24546  | BLOQUEADA | 2    | 0
(5 linhas)
```

CTEs aparecem em praticamente todo teste técnico de SQL para vagas de dados. Treine.

> 🔧 **Modifique:** na CTE acima, acrescente `COUNT(*) AS ensaios` e mostre também as OPs
> sem problema nenhum (tire o `WHERE`). Depois troque o `JOIN situacao` por `LEFT JOIN`:
> quais OPs aparecem a mais, e com que valores?

## 10. UPDATE e DELETE

```sql
UPDATE tabela SET coluna = valor WHERE condição;
DELETE FROM tabela WHERE condição;
```

São os comandos mais perigosos do SQL: **sem `WHERE`, valem para a tabela inteira.**
`DELETE FROM ensaio` apaga todos os ensaios, sem perguntar.

O hábito que evita desastre: rode antes um `SELECT` com o **mesmo** `WHERE` e confira o
que vai mudar (`exemplos/08_update_delete_transacoes.py`):

```python
alvo = "WHERE status = 'ABERTA' AND numero IN (SELECT op FROM ensaio)"
print(banco.execute(f"SELECT numero FROM op {alvo}").fetchall())
cursor = banco.execute(f"UPDATE op SET status = 'LIBERADA' {alvo}")
print("UPDATE alterou", cursor.rowcount, "linha(s)")
```

```text
[(24534,)]
UPDATE alterou 1 linha(s)
```

(O f-string aqui é aceitável porque `alvo` é texto **nosso**, fixo no código, nunca vindo
do usuário. Valores do usuário vão como parâmetro, sempre.)

`cursor.rowcount` diz quantas linhas o `UPDATE`/`DELETE` afetou. Se você esperava 1 e
veio 500, ainda dá para desistir com `rollback()`, antes do `commit()`.

## 11. Transações: commit, rollback e with

Uma **transação** agrupa comandos que só fazem sentido juntos: ou todos acontecem, ou
nenhum. Exemplo do laboratório: certificar uma carga é **gravar a expedição E mudar o
status da OP**. Metade disso no banco é um problema real (OP certificada sem carga, ou o
contrário).

- `conexao.commit()` confirma tudo desde o último commit.
- `conexao.rollback()` desfaz tudo desde o último commit.
- `with conexao:` faz os dois por você: **commit** se o bloco terminar sem erro,
  **rollback** se der exceção (e a exceção continua subindo).

> 🔮 **Preveja antes de rodar:** o terceiro comando falha no `CHECK (peso_kg > 0)`.
> Depois do `except`, qual é o status da OP 24541 (era `LIBERADA`) e quantas cargas com
> NF `123480` existem?

```python
try:
    with banco:
        banco.execute(
            "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)",
            (24541, "123480", 250.0, "2026-10-30"),
        )
        banco.execute("UPDATE op SET status = 'CERTIFICADA' WHERE numero = ?", (24541,))
        banco.execute(
            "INSERT INTO expedicao (op, nf, peso_kg, data) VALUES (?, ?, ?, ?)",
            (24541, "123481", -1, "2026-10-30"),
        )
except sqlite3.IntegrityError as erro:
    print("Erro, nada foi gravado:", erro)
print(banco.execute("SELECT status FROM op WHERE numero = 24541").fetchone())
print(banco.execute("SELECT COUNT(*) FROM expedicao WHERE nf = '123480'").fetchone())
```

<details><summary>Resposta</summary>

```text
Erro, nada foi gravado: CHECK constraint failed: peso_kg > 0
('LIBERADA',)
(0,)
```

O `with` desfez **também** os dois comandos que tinham dado certo. É exatamente o "tudo
ou nada" que queremos.
</details>

> ⚠️ **Erro comum:** achar que `with conexao:` fecha a conexão, como o `with open(...)`
> fecha o arquivo. **Não fecha.** Ele só controla a transação. Para fechar
> automaticamente, use `contextlib.closing`:
>
> ```python
> from contextlib import closing
> with closing(sqlite3.connect("lab.db")) as conexao:
>     with conexao:
>         ...
> ```

> 💡 **Dica:** no Python 3.12+ existe o parâmetro `autocommit` em `sqlite3.connect`, que
> deixa o controle de transações mais explícito. O comportamento padrão (o usado aqui)
> continua igual e funciona em todas as versões do curso.

**Transação também é desempenho.** Mil `INSERT` com um `commit` cada são lentos (cada
commit grava no disco). Mil `INSERT` num `executemany` dentro de um `with` são quase
instantâneos.

## 12. Linhas com nome: row_factory

Tuplas obrigam a lembrar a posição de cada coluna (`linha[3]` é o quê?). Com
`row_factory = sqlite3.Row`, cada linha aceita acesso por **nome**
(`exemplos/10_row_factory_e_with.py`):

```python
conexao.row_factory = sqlite3.Row
linha = conexao.execute("SELECT numero, produto FROM op WHERE numero = 24541").fetchone()
print(linha["produto"], "|", linha[0], "|", linha.keys())
ops = [dict(r) for r in conexao.execute("SELECT numero, status FROM op LIMIT 2")]
print(ops)
```

```text
Laminado PET/PE 62 µm | 24541 | ['numero', 'produto']
[{'numero': 24518, 'status': 'LIBERADA'}, {'numero': 24519, 'status': 'BLOQUEADA'}]
```

`dict(linha)` vira um dicionário: ótimo para montar dataclasses (módulo 08), JSON ou
DataFrames. A `row_factory` vale para a conexão inteira; numa função que recebe a
conexão de outra pessoa, prefira não mudá-la (use `cursor.description` para pegar os
nomes, como no `utilitarios.py`).

## 13. SQL injection na prática

Esta é a falha de segurança mais famosa da web, e ainda derruba sistemas todo ano. Ela
acontece quando o programa **cola** o texto do usuário dentro do SQL. Veja
`exemplos/09_sql_injection.py`:

```python
def buscar_cliente_inseguro(conexao, nome):
    """NUNCA faça assim: o texto do usuário vira parte do comando SQL."""
    sql = f"SELECT id, nome, cidade FROM cliente WHERE nome = '{nome}'"
    return conexao.execute(sql).fetchall()
```

Com um nome normal, funciona. Agora veja o que o programa monta com outras entradas:

```text
2) Um nome com apóstrofo já quebra a versão insegura:
  SQL montado: SELECT id, nome, cidade FROM cliente WHERE nome = 'Plásticos D'Ávila'
  OperationalError: near "Ávila": syntax error
3) Ataque: ' OR '1'='1  -> devolve TODOS os clientes
  SQL montado: SELECT id, nome, cidade FROM cliente WHERE nome = 'x' OR '1'='1'
  6 clientes vazaram
4) Ataque com UNION: lê outra tabela inteira
  SQL montado: SELECT id, nome, cidade FROM cliente WHERE nome = 'x' UNION SELECT numero, produto, status FROM op --'
  12 linhas de OUTRA tabela
```

Leia o ataque 3 devagar: o apóstrofo do usuário **fechou** o texto, e o resto virou
código: `OR '1'='1'` é sempre verdadeiro. No ataque 4, o `UNION` grudou uma consulta à
tabela `op` e o `--` transformou o apóstrofo final em comentário. Numa tela de login, o
ataque 3 entra sem senha; com `UNION`, dá para ler a tabela de usuários.

A correção é a mesma da seção 4: **parâmetros**.

```python
def buscar_cliente_seguro(conexao, nome):
    sql = "SELECT id, nome, cidade FROM cliente WHERE nome = ?"
    return conexao.execute(sql, (nome,)).fetchall()
```

```text
5) Versão segura com os mesmos textos:
  'Biscoitos Aurora'                                      -> [(3, 'Biscoitos Aurora', 'Marília')]
  "Plásticos D'Ávila"                                     -> []
  "x' OR '1'='1"                                          -> []
  "x' UNION SELECT numero, produto, status FROM op --"    -> []
```

Com parâmetro, o banco recebe o comando e o valor **separados**: o valor nunca é
interpretado como SQL, por mais aspas e palavras-chave que tenha. Ele só procura um
cliente com aquele nome estranho (e não acha).

**E nomes de coluna?** Parâmetros substituem **valores**, nunca nomes de tabela ou
coluna. Se o usuário escolhe a ordenação, confira o nome numa **lista permitida** antes
de montar o texto:

```python
COLUNAS_PERMITIDAS = {"numero", "emissao", "quantidade_kg"}

def ops_ordenadas(conexao, coluna):
    if coluna not in COLUNAS_PERMITIDAS:
        raise ValueError(f"ordenação não permitida: {coluna!r}")
    sql = f"SELECT numero FROM op ORDER BY {coluna} LIMIT 3"  # seguro: coluna conferida
    return [numero for (numero,) in conexao.execute(sql)]
```

```text
  [24527, 24550, 24528]
  ValueError: ordenação não permitida: 'numero; DROP TABLE op'
```

> 💡 **Dica:** o `execute` do `sqlite3` recusa dois comandos de uma vez
> (`ProgrammingError: You can only execute one statement at a time.`), o que barra o
> clássico `'; DROP TABLE op; --`. Mas não conte com isso: o `executescript` aceita
> vários, outros bancos aceitam, e os ataques 3 e 4 funcionam com um comando só. A
> defesa é **sempre** parâmetro.

## 14. Índices

Buscar a OP 24518 numa tabela sem índice obriga o banco a ler **todas** as linhas (um
*scan*). Um **índice** é como o sumário de um livro: uma estrutura ordenada que leva
direto às linhas certas. A chave primária já tem índice; para outras colunas muito
usadas em `WHERE` e `JOIN`, crie você (`exemplos/11_indices.py`, com 300 mil ensaios):

```python
conexao.execute("CREATE INDEX idx_ensaio_op ON ensaio (op)")
```

```text
Plano sem índice: [(3, 0, 0, 'SCAN ensaio')]
200 buscas sem índice: 2914 ms
Plano com índice: [(3, 0, 0, 'SEARCH ensaio USING COVERING INDEX idx_ensaio_op (op=?)')]
200 buscas com índice: 0.5 ms
```

`EXPLAIN QUERY PLAN` antes de uma consulta mostra o plano: `SCAN` (lê tudo) ou
`SEARCH ... USING INDEX` (vai direto). Os tempos variam por máquina, mas a diferença de
milhares de vezes é real. O preço: o índice ocupa espaço e deixa `INSERT`/`UPDATE` um
pouco mais lentos. Crie índices para as colunas que você **consulta** muito, não para
todas.

## 15. Modelando o banco de regras do projeto final

Hora de projetar o banco do Validador de Certificados. Os requisitos, do mundo real:

1. Cada linha (A, B, C, D) tem um **padrão**: tolerâncias que valem para toda OP dela.
2. Alguns clientes têm **especificação própria** (título + texto que vai no certificado),
   que muda **algumas** tolerâncias. O resto continua vindo do padrão da linha.
3. Tolerância pode ser **fixa** (mínimo e/ou máximo: COF de 0,15 a 0,35; tração mínima
   20 MPa) ou **nominal ± %** (espessura e gramatura, sobre o nominal que vem da
   planilha de cada OP).

**Exemplo resolvido: do requisito às tabelas.** Primeiro eu listo os "substantivos":
linha, especificação, tolerância. Cada um vira uma tabela. Depois penso nas relações:
uma especificação tem várias tolerâncias (uma por característica), então a tolerância
aponta para a especificação. E o padrão da linha? Em vez de uma tabela a mais, ele é
**uma especificação como as outras**, só que com a coluna `linha` preenchida. Assim a
tabela de tolerâncias serve para os dois casos. O resultado, idêntico ao do projeto
final (`dados/regras.sql`):

```sql
CREATE TABLE linha (
    codigo    TEXT PRIMARY KEY CHECK (codigo IN ('A', 'B', 'C', 'D')),
    descricao TEXT NOT NULL
);

CREATE TABLE especificacao (
    titulo TEXT PRIMARY KEY,               -- 'PADRAO-A', 'ESP-0533'
    texto  TEXT NOT NULL DEFAULT '',       -- vai no certificado
    linha  TEXT REFERENCES linha (codigo)  -- preenchida = PADRÃO da linha
);

-- Cada linha tem no máximo UM padrão
CREATE UNIQUE INDEX um_padrao_por_linha
    ON especificacao (linha) WHERE linha IS NOT NULL;

CREATE TABLE tolerancia (
    titulo         TEXT NOT NULL REFERENCES especificacao (titulo),
    caracteristica TEXT NOT NULL,          -- espessura, gramatura, cof, tracao, selagem
    tipo           TEXT NOT NULL CHECK (tipo IN ('fixa', 'nominal')),
    minimo         REAL,                   -- tipo 'fixa'
    maximo         REAL,                   -- tipo 'fixa'
    percentual     REAL,                   -- tipo 'nominal'
    PRIMARY KEY (titulo, caracteristica)
);
```

```text
linha (codigo PK) ◄──── especificacao (titulo PK, texto, linha FK ou NULL)
                                 ▲
                                 │ titulo
                        tolerancia (titulo FK + caracteristica = PK composta,
                                    tipo, minimo, maximo, percentual)
```

Cada decisão, com o porquê:

- **`PRIMARY KEY (titulo, caracteristica)`** (chave composta): uma especificação não pode
  ter duas regras de COF.
- **Índice único parcial** (`WHERE linha IS NOT NULL`): no máximo um padrão por linha,
  mas quantas especificações de cliente quiser (essas têm `linha` NULL).
- **`CHECK (tipo IN (...))`**: um erro de digitação (`'nomial'`) é recusado na hora.
- **Não guardamos o nominal**: ele muda a cada OP e vem da planilha. O banco guarda só o
  percentual. Guardar o que muda junto com o que não muda é a origem de muita
  inconsistência.

As restrições funcionando (`exemplos/12_banco_de_regras.py`):

```text
Segundo padrão para a linha A -> UNIQUE constraint failed: especificacao.linha
Tipo inválido -> CHECK constraint failed: tipo IN ('fixa', 'nominal')
```

**A consulta que importa:** quais tolerâncias valem para uma OP da linha A com a
especificação ESP-0533? As da especificação, mais as do padrão que a especificação
**não** redefine:

```sql
SELECT caracteristica, tipo, minimo, maximo, percentual, titulo AS origem
FROM tolerancia
WHERE titulo = :titulo
UNION ALL
SELECT t.caracteristica, t.tipo, t.minimo, t.maximo, t.percentual, t.titulo
FROM tolerancia AS t
JOIN especificacao AS e ON e.titulo = t.titulo
WHERE e.linha = :linha
  AND t.caracteristica NOT IN (
      SELECT caracteristica FROM tolerancia WHERE titulo = :titulo
  )
ORDER BY caracteristica
```

```text
caracteristica | tipo    | minimo | maximo | percentual | origem
---------------+---------+--------+--------+------------+---------
cof            | fixa    | 0.15   | 0.35   | NULL       | PADRAO-A
espessura      | nominal | NULL   | NULL   | 5          | ESP-0533
gramatura      | nominal | NULL   | NULL   | 10         | PADRAO-A
selagem        | fixa    | 8      | NULL   | NULL       | PADRAO-A
tracao         | fixa    | 28     | NULL   | NULL       | ESP-0533
(5 linhas)
```

`UNION ALL` empilha os resultados de duas consultas com as mesmas colunas (como o
`pd.concat`). Os parâmetros nomeados (`:titulo`, `:linha`) deixam reaproveitar o mesmo
valor em vários lugares, passando um dicionário: `{"linha": "A", "titulo": "ESP-0533"}`.

Por fim, a tolerância nominal vira uma faixa no Python, com o nominal da planilha (60 µm
± 5% = 57 a 63 µm). Essa parte é uma função pura, sem banco: fácil de testar. É o
exercício 12, e o coração das regras do módulo 14.

> 🔧 **Modifique:** rode a consulta acima para a linha D com a ESP-0412 (o laminado de
> café). Quais características vêm da especificação e quais do padrão?

## 16. SQL e pandas: read_sql e to_sql

O trabalho de dados real costuma ser: **SQL** filtra, junta e agrega no banco (onde os
dados estão), e o **pandas** recebe a tabela pronta para análise, gráficos e Excel
(`exemplos/13_pandas_read_sql.py`):

```python
import pandas as pd

consulta = """
    SELECT o.linha, e.caracteristica, e.valor
    FROM ensaio AS e
    JOIN op AS o ON o.numero = e.op
    WHERE e.caracteristica = ? AND e.valor IS NOT NULL
"""
df = pd.read_sql(consulta, banco, params=("espessura",))
print(df.groupby("linha")["valor"].agg(["count", "mean"]).round(2))
```

```text
       count   mean
linha
A          8  48.60
B          4  34.40
C          4  70.62
D          4  58.05
```

Os parâmetros continuam valendo (`params=`). O caminho inverso, `df.to_sql("meta",
banco, index=False, if_exists="replace")`, grava um DataFrame como tabela (útil para
carregar uma planilha no banco). Para outros bancos (PostgreSQL, SQL Server), o pandas
usa a biblioteca SQLAlchemy para conectar; o SQL é o mesmo.

## Lendo mensagens de erro deste módulo

| Mensagem | O que significa e como corrigir |
|---|---|
| `sqlite3.OperationalError: no such table: ensaios` | Nome da tabela errado, ou o banco aberto não é o que você pensa (o `connect` criou um vazio num caminho errado). Confira o caminho e `SELECT name FROM sqlite_master`. |
| `sqlite3.OperationalError: no such column: numro` | Coluna com nome errado (ou de outra tabela sem o `JOIN`). Veja `PRAGMA table_info(tabela)`. |
| `sqlite3.OperationalError: near "Ávila": syntax error` | SQL montado com f-string e um apóstrofo no meio. Use parâmetros. |
| `sqlite3.OperationalError: misuse of aggregate function COUNT()` | Agregação no `WHERE`. Use `HAVING` (depois do `GROUP BY`). |
| `sqlite3.OperationalError: ambiguous column name: id` | A coluna existe nas duas tabelas do JOIN. Use o apelido: `o.id`. |
| `sqlite3.IntegrityError: UNIQUE constraint failed: op.numero` | Chave repetida. Confira se o registro já existe (ou use `UPDATE`). |
| `sqlite3.IntegrityError: FOREIGN KEY constraint failed` | O valor da FK não existe na tabela de origem (ex.: cliente 99). |
| `sqlite3.IntegrityError: CHECK constraint failed: peso_kg > 0` | O dado quebra uma regra do banco. Corrija o dado, não a regra. |
| `sqlite3.ProgrammingError: Incorrect number of bindings supplied` | Quantidade de `?` diferente da de valores. Um valor só: `(valor,)`. |
| `sqlite3.ProgrammingError: You can only execute one statement at a time.` | Dois comandos num `execute`. Use dois `execute` (ou `executescript`, só com SQL seu). |
| `sqlite3.ProgrammingError: Cannot operate on a closed database.` | A conexão já foi fechada. Abra de novo, ou reorganize o `with closing(...)`. |
| `sqlite3.OperationalError: database is locked` | Outro programa (ou o DB Browser com alterações não gravadas) está escrevendo no arquivo. Grave/feche o outro e tente de novo. |

Lembre: a última linha do traceback diz o tipo do erro; suba até a primeira linha que
aponta para um arquivo **seu**.

## Boas práticas

- **Valores sempre como parâmetros** (`?` ou `:nome`). Nomes de coluna, só de lista
  permitida.
- **`PRAGMA foreign_keys = ON`** em toda conexão SQLite.
- **Regras no banco:** `NOT NULL`, `UNIQUE`, `CHECK`, FK. O banco é a última linha de
  defesa contra dado ruim.
- **Datas em texto ISO** (`'AAAA-MM-DD'`), que ordenam e comparam certo.
- **`SELECT` antes de `UPDATE`/`DELETE`**, com o mesmo `WHERE`; confira o `rowcount`.
- **Operações relacionadas numa transação** (`with conexao:`) e conexão fechada no fim
  (`closing`).
- **Nada de `SELECT *` em programa:** liste as colunas.
- **`ORDER BY` sempre que a ordem importar.** Sem ele, a ordem não é garantida.
- **Scripts `.sql` versionados no Git** para criar o banco (como `dados/regras.sql`): o
  banco vira algo reprodutível.
- **Funções pequenas que recebem a conexão** (como nos exercícios): fáceis de testar com
  `sqlite3.connect(":memory:")`.

## No mundo real

Toda manhã a expedição pergunta: "quais cargas já podem receber certificado, e por que
as outras não?". Com SQL, a resposta é **uma consulta** (`exemplos/14_fila_de_certificados.py`),
que junta quatro tabelas, resume os ensaios numa CTE e explica a situação de cada carga
com `CASE`:

```sql
WITH situacao_op AS (                       -- passo 1: um resumo por OP
    SELECT op,
           COUNT(*)                 AS ensaios,
           SUM(resultado = 'FORA')  AS fora,
           SUM(valor IS NULL)       AS pendentes
    FROM ensaio
    GROUP BY op
)
SELECT x.op, x.nf, x.peso_kg, c.nome AS cliente,     -- passo 2: cada carga
       CASE
           WHEN o.status = 'CERTIFICADA'      THEN 'já certificada'
           WHEN s.ensaios IS NULL             THEN 'sem ensaios'
           WHEN s.fora > 0                    THEN 'ensaio fora'
           WHEN s.pendentes > 0               THEN 'ensaio pendente'
           WHEN o.status <> 'LIBERADA'        THEN 'OP ' || LOWER(o.status)
           ELSE 'EMITIR'
       END AS situacao
FROM expedicao AS x
JOIN op AS o ON o.numero = x.op
JOIN cliente AS c ON c.id = o.cliente_id
LEFT JOIN situacao_op AS s ON s.op = x.op
WHERE x.data BETWEEN :inicio AND :fim
ORDER BY situacao = 'EMITIR' DESC, x.op, x.nf
```

O exemplo acrescenta duas cargas pedidas por e-mail (OPs 24533 e 24534) e roda a semana
de 25 a 31/10:

```text
op    | nf     | peso_kg | cliente                | situacao
------+--------+---------+------------------------+----------------
24518 | 123456 | 1250.5  | Torrefação Serra Ltda  | EMITIR
24518 | 123470 | 1830    | Torrefação Serra Ltda  | EMITIR
24520 | 123458 | 2400    | Agro Campo S.A.        | EMITIR
24521 | 123459 | 2950    | Agro Campo S.A.        | EMITIR
24541 | 123465 | 2000.25 | Torrefação Serra Ltda  | EMITIR
24541 | 123466 | 1750    | Torrefação Serra Ltda  | EMITIR
24528 | 123452 | 1300    | Higiene Bem-Estar S.A. | já certificada
24528 | 123453 | 1450.5  | Higiene Bem-Estar S.A. | já certificada
24533 | 123490 | 1500    | Biscoitos Aurora       | ensaio fora
24534 | 123491 | 800     | Torrefação Serra Ltda  | ensaio pendente
(10 linhas)
```

Repare no `LEFT JOIN` com a CTE (para não perder carga de OP sem ensaio), no `||` (junta
textos no SQL) e no `ORDER BY` com uma comparação (as cargas a emitir primeiro). No
exercício 14 você faz o passo seguinte: emitir os certificados dessa fila, numerados,
numa transação.

## Resumo

| Tarefa | Sintaxe |
|---|---|
| Conectar / fechar | `con = sqlite3.connect("lab.db")`, `con.close()`, `closing(...)` |
| Executar | `cur = con.execute(sql, params)`, `con.executemany(sql, lista)` |
| Ler | `cur.fetchone()`, `cur.fetchall()`, `for linha in cur:` |
| Gravar / desfazer | `con.commit()`, `con.rollback()`, `with con:` |
| Parâmetros | `"... WHERE op = ?", (op,)` ou `"... WHERE op = :op", {"op": op}` |
| Criar tabela | `CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, c TEXT NOT NULL, ...)` |
| Restrições | `NOT NULL`, `UNIQUE`, `CHECK (...)`, `DEFAULT`, `REFERENCES t (c)` |
| Inserir | `INSERT INTO t (a, b) VALUES (?, ?)`; `cur.lastrowid` |
| Consultar | `SELECT a, b FROM t WHERE ... ORDER BY a DESC LIMIT 10` |
| Filtros | `=`, `<>`, `BETWEEN`, `IN (...)`, `LIKE '%x%'`, `IS NULL`, `AND`/`OR` |
| Agregar | `COUNT(*)`, `COUNT(c)`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING` |
| Juntar | `FROM a JOIN b ON b.x = a.y`, `LEFT JOIN`, anti-join com `IS NULL` |
| Subconsultas | `WHERE x > (SELECT AVG...)`, `IN (SELECT ...)`, `NOT EXISTS (...)` |
| CTE | `WITH nome AS (SELECT ...) SELECT ... FROM nome` |
| Alterar / apagar | `UPDATE t SET c = ? WHERE ...`, `DELETE FROM t WHERE ...`; `cur.rowcount` |
| Condicional | `CASE WHEN ... THEN ... ELSE ... END` |
| Índice | `CREATE INDEX idx ON t (c)`; `EXPLAIN QUERY PLAN ...` |
| Linhas com nome | `con.row_factory = sqlite3.Row`; `dict(linha)` |
| pandas | `pd.read_sql(sql, con, params=(...))`, `df.to_sql("t", con, index=False)` |

## Você domina este módulo se...

- [ ] Consigo explicar chave primária e chave estrangeira com um exemplo do laboratório,
      sem consultar.
- [ ] Consigo criar uma tabela com `NOT NULL`, `UNIQUE`, `CHECK` e FK, e dizer qual erro
      cada uma provoca.
- [ ] Consigo explicar por que `WHERE valor = NULL` não acha nada e qual a forma certa.
- [ ] Consigo explicar a diferença entre `WHERE` e `HAVING` pela ordem de execução.
- [ ] Consigo escrever um `LEFT JOIN` que acha "quem não tem" e explicar por que uma
      condição no `WHERE` pode desfazer o `LEFT`.
- [ ] Consigo demonstrar um SQL injection com `' OR '1'='1` e corrigir com parâmetros.
- [ ] Consigo agrupar comandos numa transação com `with conexao:` e sei que ele não fecha
      a conexão.
- [ ] Consigo desenhar o banco de regras do projeto final e justificar cada tabela.

## Exercícios

| Nº | Exercício | Nível | O que pratica |
|---|---|---|---|
| 01 | `ex01_criar_tabela_bobinas` | ★☆☆ | `CREATE TABLE` com PK, `NOT NULL`, `CHECK`, `UNIQUE` |
| 02 | `ex02_inserir_bobina` | ★☆☆ | `INSERT` com `?`, `lastrowid`, `commit` |
| 03 | `ex03_inserir_varias` | ★☆☆ | `executemany` numa transação (tudo ou nada) |
| 04 | `ex04_buscar_por_op` | ★☆☆ | `SELECT` com `WHERE` e `ORDER BY`, `fetchone` |
| 05 | `ex05_filtros_where` | ★☆☆ | `BETWEEN`, `IS NULL`, `LIKE`, `DISTINCT` |
| 06 | `ex06_agregacoes` | ★★☆ | `COUNT`, `AVG`, `MIN`, `MAX`, `COALESCE`, filtro opcional |
| 07 | `ex07_group_by_having` | ★★☆ | `GROUP BY`, `HAVING`, ordenação com empate |
| 08 | `ex08_joins` | ★★☆ | `JOIN`, `LEFT JOIN`, anti-join, JOIN encadeado |
| 09 | `ex09_subconsulta` | ★★☆ | subconsulta escalar, `IN`, `NOT EXISTS` |
| 10 | `ex10_corrija_as_consultas` | ★★☆ | **leitura de código e depuração**: 3 armadilhas clássicas |
| 11 | `ex11_busca_segura` | ★★★ | filtros dinâmicos sem SQL injection, lista permitida |
| 12 | `ex12_banco_de_regras` | ★★★ | banco de regras do projeto: padrão + especificação, nominal ± % |
| 13 | `ex13_revisao_importar_csv` | ★★☆ | **revisão**: CSV (mód. 06), números BR (mód. 05), datas (mód. 07) + INSERT |
| 14 | `ex14_revisao_emitir_certificados` | ★★★ | **revisão**: dataclass (mód. 08), datas (mód. 07) + transação |

Como fazer: abra `exercicios/exNN_...py`, leia o enunciado, escreva o código no lugar de
`raise NotImplementedError`, e rode, na pasta `curso-python`:

```text
python curso.py testar 11 ex01
```

Cada teste cria um banco novo **na memória** (`sqlite3.connect(":memory:")`), monta as
tabelas (a partir de `dados/laboratorio.sql` ou `dados/regras.sql`, quando o enunciado
diz "banco do laboratório" ou "banco de regras") e passa a conexão para a sua função. Não
altere os arquivos `.sql` da pasta `dados/`: os testes dependem deles.

## Desafio do módulo

**Ferramenta do banco de regras:** um programa de linha de comando com subcomandos para
criar o banco de regras, listar as especificações, mostrar as tolerâncias efetivas de
uma OP (com as faixas calculadas a partir do nominal) e conferir valores medidos,
devolvendo APROVADA ou REPROVADA com os motivos. Enunciado completo em
[desafio/README.md](desafio/README.md).

## Quiz

Teste o que ficou com o [quiz do módulo](quiz.md) (14 perguntas, gabarito no final).

## Para ir além

- Documentação oficial do `sqlite3` em português:
  <https://docs.python.org/pt-br/3/library/sqlite3.html>
- SQL do SQLite, comando por comando: <https://www.sqlite.org/lang.html>
- Tipagem flexível e tabelas STRICT no SQLite: <https://www.sqlite.org/stricttables.html>
- SQL injection explicado pela OWASP: <https://owasp.org/www-community/attacks/SQL_Injection>
- DB Browser for SQLite (para ver e editar os `.db`): <https://sqlitebrowser.org>
- Para treinar SQL com exercícios corrigidos na hora: SQLBolt (<https://sqlbolt.com>) e,
  depois, funções de janela (`ROW_NUMBER`, `LAG`), o próximo passo pedido em vagas de
  dados: <https://www.sqlite.org/windowfunctions.html>
