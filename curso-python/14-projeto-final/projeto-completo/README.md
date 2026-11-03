# Validador de Certificados

Sistema de linha de comando que confere as OPs da planilha de valores do laboratório
contra as regras de qualidade, lê os pedidos de certificado que a expedição manda por
e-mail e monta a fila de emissão no TOTVS. Hoje roda em **modo ensaio**: faz tudo,
menos clicar no TOTVS, e entrega um relatório dizendo o que seria emitido e o que
ficou bloqueado (com o motivo).

```text
e-mails da expedição ─┐
planilha de valores ──┼─> triagem ─> fila de emissão ─> emissor (ensaio) ─> relatório
banco de regras ──────┘      │                                               (.xlsx/.csv)
                             └─> bloqueados com motivo ─────────────────────────┘
```

## O que ele confere

- **Tolerâncias** de cada característica: fixas (mín/máx: COF, tração, selagem) e
  nominais ± % (espessura e gramatura, sobre o nominal da planilha).
- **Especificação**: título do cliente (herda do padrão da linha e sobrescreve o que
  define) ou padrão da linha. Título desconhecido vira pendência: nunca chuta.
- **Liberação**: a observação precisa ter a marca "COF: liberado" (aceita variações de
  maiúsculas, acento, espaços e pontuação; "COF: não liberado" não passa).
- **Consistência**: OP inexistente ou repetida na planilha, linha digitada diferente da
  aba, e-mail sem OP/NF/peso ou com dois valores para o mesmo campo.
- **Idempotência**: a mesma OP/NF não é emitida duas vezes (histórico em
  `saida/emitidos.csv`, gravado só no modo real).

## Instalação

Requer Python 3.10 ou mais novo. No Windows (PowerShell):

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

No Linux/macOS, troque a ativação por `source .venv/bin/activate`.

O `-e` instala em modo editável: você muda o código e o comando `validador` já usa a
versão nova. O `[dev]` traz pytest e ruff.

## Uso

Rodando sobre os dados de exemplo (fictícios) que vêm no repositório:

```text
validador --planilha dados/planilha_valores.xlsx --regras dados/regras.db --emails dados/emails
```

Saída (o log vai para o terminal e para `saida/validador.log`):

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
INFO     relatórios gravados: relatorio_2026-10-29_101500.xlsx e relatorio_2026-10-29_101500.csv
Série processada em modo ENSAIO (nada foi enviado ao TOTVS)
  bloqueado                 4
  ensaio                    2
  e-mails fora do padrão    2
Relatório: saida/relatorio_2026-10-29_101500.xlsx
```

Sem instalar, de dentro da pasta do projeto, também funciona:

```text
$env:PYTHONPATH = "src"          # Linux/macOS: export PYTHONPATH=src
python -m validador_certificados --planilha dados/planilha_valores.xlsx --regras dados/regras.db --emails dados/emails
```

Opções: `--saida PASTA` (padrão `saida`), `-v` (log detalhado), `--emitir` (modo real,
ainda indisponível), `--version`, `--help`.

Códigos de saída: `0` sucesso, `1` erro esperado (arquivo, planilha, banco) ou falha de
emissão, `2` argumentos inválidos, `3` erro inesperado (detalhes no log).

## Formato das entradas

**Planilha** (`.xlsx`): uma aba por linha de produção (`Linha A` ... `Linha D`), cabeçalho
na linha 1, uma OP por linha. Colunas obrigatórias: OP, Linha, Especificação, Espessura
nominal, Espessura, Gramatura nominal, Gramatura, COF, Tração, Selagem, Observação.
O cabeçalho é comparado sem acento, sem maiúsculas e sem o que estiver entre
parênteses: `Espessura (µm)` e `ESPESSURA (um)` são a mesma coluna. Colunas extras
(Data, Produto...) são ignoradas ou guardadas como informação.

**Banco de regras** (SQLite): schema em `sql/schema.sql`. Padrões de linha têm a coluna
`linha` preenchida; especificações de cliente deixam `linha` vazia e listam só as
tolerâncias que mudam. Para editar, use o [DB Browser for SQLite](https://sqlitebrowser.org/).

**E-mails** (`.txt`, UTF-8 ou cp1252): um pedido por e-mail, com `OP`, `NF` (ou
`NF-e`, `Nota fiscal`) e `Peso` em kg no formato brasileiro (`1.250,5 kg`).

## Estrutura

```text
src/validador_certificados/
  modelos.py         dataclasses do domínio + exceções
  texto.py           normalização, "COF: liberado", números BR
  regras.py          tolerâncias, validação da OP, escolha da especificação (puro)
  banco.py           leitura do banco de regras (SQLite, somente leitura)
  planilha.py        leitura da planilha (openpyxl) e conferência da linha
  expedicao.py       leitura dos e-mails da expedição
  fila.py            triagem: fila de emissão e bloqueados (serviço)
  emissao.py         interface Emissor, EmissorTotvs (ensaio) e emitir_fila
  robo_playwright.py ESQUELETO do robô real no Edge (não testado)
  historico.py       OP/NF já emitidos (idempotência)
  relatorio.py       relatório Excel (3 abas + gráfico) e CSV
  serie.py           orquestra uma série inteira
  cli.py             argparse + logging + códigos de saída
tests/               pytest (unidade + ponta a ponta sobre dados/)
dados/               dados de exemplo fictícios
sql/schema.sql       schema do banco de regras
```

Regra de dependência: `modelos`, `texto` e `regras` não importam openpyxl, sqlite3 nem
nada de I/O. As bordas (planilha, banco, e-mail, TOTVS) dependem do núcleo, nunca o
contrário.

## Desenvolvimento

```text
python -m pytest           # testes
ruff check .               # lint
ruff format .              # formatação
```

O workflow `.github/workflows/testes.yml` roda lint, testes e a série de exemplo no
GitHub Actions (Windows e Ubuntu, Python 3.10 e 3.13) a cada push.

## Próximos passos

- [ ] Robô real no TOTVS: implementar `EmissorTotvsPlaywright` (roteiro no topo de
      `robo_playwright.py`) e usar na CLI quando `--emitir` for passado.
- [ ] Ler os e-mails direto do Outlook (pasta "Certificados") em vez de `.txt`.
- [ ] API FastAPI para consultar especificações e validar uma OP.
- [ ] Agendar a série no Agendador de Tarefas do Windows.

## Licença

MIT. Os dados em `dados/` são fictícios.
