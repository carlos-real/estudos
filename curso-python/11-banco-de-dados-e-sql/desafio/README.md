# Desafio do módulo 11 — Ferramenta do banco de regras

## Contexto

No projeto final, as regras de conferência (padrão de cada linha, especificações de
cliente e tolerâncias) moram num banco SQLite. Hoje, quem quer saber "qual é a faixa de
espessura da OP da linha A com a ESP-0533?" abre o DB Browser e escreve SQL na mão. Você
vai criar uma ferramenta de linha de comando que responde isso, e confere valores
medidos, em um comando.

## Requisitos obrigatórios

1. Linha de comando com `argparse` e subcomandos (`add_subparsers`, módulo 07), com a
   opção geral `--banco` (padrão: `11-banco-de-dados-e-sql/saida/regras.db`).
2. `criar`: cria o banco a partir de `dados/regras.sql`. Se o arquivo já existir, recusa,
   a não ser que venha `--forcar`.
3. `listar`: mostra cada especificação, a linha (ou `-` para especificação de cliente) e
   quantas tolerâncias ela tem. Padrões primeiro.
4. `regras --linha X [--especificacao TITULO] [--nominal carac=valor ...]`: mostra as
   tolerâncias **efetivas** (padrão da linha + especificação do cliente por cima), com a
   origem de cada uma. Para as do tipo nominal, calcula a faixa se o nominal for
   informado; senão mostra "nominal ± N%".
5. `conferir --linha X [--especificacao TITULO] --valor carac=valor ... [--nominal ...]`:
   imprime `APROVADA` ou `REPROVADA` com os motivos. Código de saída 0 se aprovada e 2 se
   reprovada (útil para outros scripts).
6. Todo valor vindo do usuário entra nas consultas como **parâmetro** (`?` ou `:nome`).
7. Título da especificação sem diferenciar maiúsculas e sem espaços nas pontas.
8. Erros (banco inexistente, especificação desconhecida, `nome=valor` mal escrito):
   mensagem clara em português e código de saída 1, sem traceback. Atenção:
   `sqlite3.connect("caminho_errado.db")` **cria** um banco vazio sem avisar; confira se
   o arquivo existe antes.
9. Sem argumentos, roda uma demonstração num banco na memória.

## Extras opcionais

- `adicionar-especificacao --titulo ESP-0700 --texto "..."` e
  `adicionar-tolerancia --titulo ESP-0700 --caracteristica cof --tipo fixa --minimo 0.1
  --maximo 0.2`, com as restrições do banco protegendo os dados (trate o
  `IntegrityError`).
- `exportar --saida regras.xlsx`: todas as tolerâncias numa planilha (pandas `read_sql` +
  `to_excel`).
- Aceitar números com vírgula (`cof=0,28`).
- Testes com pytest para `tolerancias_efetivas` e `conferir`, usando um banco
  `:memory:`.

## Exemplo de execução

```text
> python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py criar
Banco criado: ...\11-banco-de-dados-e-sql\saida\regras.db

> python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py regras --linha A --especificacao esp-0533 --nominal espessura=60 --nominal gramatura=55,5
Linha A, especificação ESP-0533
característica  tipo       mínimo   máximo  origem
cof             fixa         0,15     0,35  PADRAO-A
espessura       nominal        57       63  ESP-0533
gramatura       nominal     49,95    61,05  PADRAO-A
selagem         fixa            8        -  PADRAO-A
tracao          fixa           28        -  ESP-0533

> python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py conferir --linha D --valor cof=0.31 --valor espessura=60 --nominal espessura=62
REPROVADA
  - cof 0.31 acima do máximo 0.3

> python 11-banco-de-dados-e-sql/desafio/solucao_referencia.py regras --linha B --especificacao ESP-9
Erro: especificação 'ESP-9' não cadastrada
```

## Critérios de aceite

- [ ] `criar` gera o banco; rodar de novo sem `--forcar` dá erro amigável.
- [ ] `listar` mostra as 7 especificações (4 padrões e 3 de cliente).
- [ ] `regras --linha A --especificacao ESP-0533 --nominal espessura=60` mostra a
      espessura de 57 a 63 vinda da ESP-0533 e o COF de 0,15 a 0,35 vindo do PADRAO-A.
- [ ] `conferir` devolve código de saída 0 (aprovada) ou 2 (reprovada).
- [ ] Nenhuma consulta monta SQL com f-string a partir de texto do usuário.
- [ ] Banco inexistente não é criado sem querer.
- [ ] `ruff check` e `ruff format --check` passam no seu arquivo.

## Dicas de como começar

1. Comece pelas funções de banco, sem CLI: `especificacao(conexao, linha, titulo)` e
   `tolerancias_efetivas(conexao, linha, titulo)`. Teste no REPL com
   `sqlite3.connect(":memory:")` e `executescript` do `regras.sql`.
2. A consulta das tolerâncias efetivas está na seção 15 da aula (UNION ALL + NOT IN).
3. `limites(...)` é uma função pura: fácil de testar sem banco.
4. Só depois monte o `argparse`. Use `action="append"` para aceitar `--valor` várias
   vezes.
5. Para fechar a conexão sempre: `with closing(sqlite3.connect(...)) as conexao:`.

A solução de referência está em `solucao_referencia.py`. Tente antes de abrir!
