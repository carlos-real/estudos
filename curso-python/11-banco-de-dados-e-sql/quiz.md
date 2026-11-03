# Quiz — Módulo 11: bancos de dados e SQL

Responda sem rodar. Depois confira no gabarito. As perguntas com SQL usam o banco do
laboratório da aula (`dados/laboratorio.sql`): 12 OPs, 6 clientes, 60 ensaios.

**1.** Para que serve a chave estrangeira `cliente_id INTEGER REFERENCES cliente (id)`
na tabela `op`?

- a) Deixa a busca por cliente mais rápida.
- b) Impede gravar uma OP com um cliente que não existe (com `PRAGMA foreign_keys = ON`).
- c) Cria o cliente automaticamente.
- d) Faz o `id` do cliente ser único.

**2.** O que esta consulta devolve?

```sql
SELECT NULL = NULL, NULL IS NULL, 1 + NULL;
```

**3.** Quantos clientes esta consulta conta? (Clientes de SP: Torrefação Serra, em
Franca, e Biscoitos Aurora, em Marília. De MG: Laticínios Serra Azul, em Juiz de Fora, e
Café do Vale, em Varginha.)

```sql
SELECT COUNT(*) FROM cliente WHERE uf = 'SP' OR uf = 'MG' AND cidade = 'Varginha';
```

**4.** Onde está o erro?

```sql
SELECT linha, COUNT(*) FROM op WHERE COUNT(*) > 2 GROUP BY linha;
```

**5.** O que `conexao.execute(sql, 24518)` provoca, e como corrigir?

```python
sql = "SELECT * FROM op WHERE numero = ?"
conexao.execute(sql, 24518)
```

**6.** A tabela `op` tem 12 linhas e só 3 têm `especificacao` preenchida. O que sai?

```sql
SELECT COUNT(*), COUNT(especificacao) FROM op;
```

**7.** Qual a diferença entre `INNER JOIN` e `LEFT JOIN` entre `cliente` (esquerda) e
`op` (direita)?

**8.** Por que este código é perigoso? Mostre um valor de `nome` que vaza todos os
clientes.

```python
sql = f"SELECT * FROM cliente WHERE nome = '{nome}'"
conexao.execute(sql)
```

**9.** Você precisa deixar o usuário escolher a coluna de ordenação. Por que
`conexao.execute("SELECT * FROM op ORDER BY ?", (coluna,))` não resolve, e o que fazer?

**10.** O que acontece com os dados?

```python
with conexao:
    conexao.execute("UPDATE op SET status = 'CERTIFICADA' WHERE numero = 24541")
    conexao.execute("INSERT INTO expedicao (op, nf, peso_kg, data) "
                    "VALUES (24541, '1', -5, '2026-10-30')")  # CHECK (peso_kg > 0)
```

- a) O UPDATE fica gravado e o INSERT não.
- b) Nada fica gravado: o `with` faz rollback e a exceção sobe.
- c) Os dois ficam gravados.
- d) A conexão é fechada.

**11.** Depois de um bloco `with conexao:`, a conexão está fechada?

**12.** O que esta consulta faz e qual "padrão" ela usa?

```sql
SELECT o.numero
FROM op AS o
LEFT JOIN ensaio AS e ON e.op = o.numero
WHERE e.id IS NULL;
```

**13.** No banco de regras do projeto final, por que existe o índice abaixo?

```sql
CREATE UNIQUE INDEX um_padrao_por_linha ON especificacao (linha) WHERE linha IS NOT NULL;
```

**14.** `sqlite3.connect("regras.bd")` (você errou a extensão; o arquivo certo é
`regras.db`). O que acontece?

- a) `FileNotFoundError`.
- b) O SQLite cria um banco novo e vazio com esse nome, sem avisar.
- c) Abre o `regras.db` mesmo assim.
- d) `sqlite3.OperationalError` na hora.

---

## Gabarito

1. **b.** A FK garante a integridade: `cliente_id` precisa existir em `cliente.id`. No
   SQLite, só vale com `PRAGMA foreign_keys = ON` em cada conexão.
2. **`(None, 1, None)`.** Comparar com NULL dá NULL ("desconhecido"); só `IS NULL` dá
   verdadeiro (1). Conta com NULL também dá NULL.
3. **3.** O `AND` vem antes do `OR`, então a condição é `uf = 'SP' OR (uf = 'MG' AND
   cidade = 'Varginha')`: os 2 de SP mais o Café do Vale. Use parênteses para não depender
   da precedência.
4. **Agregação no WHERE.** O WHERE roda antes do GROUP BY e não enxerga `COUNT(*)` (erro
   `misuse of aggregate function COUNT()`). Use `HAVING COUNT(*) > 2` depois do
   `GROUP BY`.
5. **`ProgrammingError: parameters are of unsupported type`.** Os parâmetros vão numa
   sequência: `conexao.execute(sql, (24518,))`, com a vírgula.
6. **`12 | 3`.** `COUNT(*)` conta linhas; `COUNT(coluna)` conta valores não nulos.
7. **INNER** só traz clientes que têm OP (e as OPs). **LEFT** traz todos os clientes; os
   sem OP aparecem uma vez, com as colunas de `op` em NULL (o Café do Vale, por exemplo).
8. **SQL injection.** O texto do usuário vira código SQL. Com `nome = "x' OR '1'='1"` a
   condição fica `nome = 'x' OR '1'='1'`, sempre verdadeira. Correto:
   `conexao.execute("SELECT * FROM cliente WHERE nome = ?", (nome,))`.
9. **Parâmetros só substituem VALORES**, nunca nomes de coluna ou tabela. Com `?`, o
   banco ordena por um texto constante (não pela coluna). Confira o nome numa lista
   permitida (`if coluna not in {"numero", "emissao"}: raise ValueError`) e só então
   monte o texto.
10. **b.** O `with conexao:` é uma transação: erro dentro do bloco desfaz tudo (rollback)
    e a exceção (`IntegrityError`) continua subindo.
11. **Não.** O `with conexao:` controla a transação (commit/rollback), mas não fecha.
    Feche com `conexao.close()` ou use `with contextlib.closing(sqlite3.connect(...))`.
12. **Lista as OPs sem nenhum ensaio** (24550 e 24551). É o "anti-join": LEFT JOIN e
    depois ficar só com quem não achou par (`IS NULL` numa coluna da direita).
13. **Para garantir no máximo UM padrão por linha.** É um índice único *parcial*: vale só
    para as linhas com `linha` preenchida (as especificações de cliente têm `linha` NULL
    e podem ser muitas).
14. **b.** O `connect` cria o arquivo se ele não existe. A primeira consulta depois dá
    `no such table`, longe da causa real. Por isso, confira `Path(caminho).is_file()`
    antes, ou abra em modo somente leitura (`?mode=ro` com `uri=True`).
