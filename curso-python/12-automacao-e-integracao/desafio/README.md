# Desafio do módulo 12 — Robô da expedição (modo ensaio)

## Contexto

Toda manhã chegam pedidos de certificado da expedição por e-mail. Hoje alguém lê um
por um, confere a OP no sistema, vê se ela tem especificação de cliente, emite o
certificado e avisa o supervisor. Você vai automatizar a parte chata **com segurança**:
o robô roda em **modo ensaio** por padrão, não emite nada em dobro e deixa rastro de tudo.

Os e-mails de exemplo estão em `../dados/emails/` (5 arquivos `.eml`, um deles sem NF e
outro com uma OP que não existe no cadastro). O cadastro de OPs é `../dados/ops.csv`
(separado por `;`):

```text
op;linha;produto;especificacao_titulo;especificacao_texto
123456;B;Filme PE 40 µm;Espec. Cliente Alfa;COF 0,20 a 0,30 e espessura 40 µm ± 5%
123789;A;Filme PP 20 µm;;
...
```

Especificação em branco significa "use o padrão da linha".

## Requisitos obrigatórios

1. Programa de linha de comando (`argparse`) com as opções `--emails` (pasta),
   `--ops` (CSV), `--saida` (pasta) e `--confirmar`. Sem `--confirmar`, é **ensaio**.
2. Ler todos os `.eml` da pasta e extrair OP (6 dígitos), NF e peso (formato
   brasileiro). Corpo em texto puro ou só em HTML.
3. E-mail sem algum campo, ou com OP fora do cadastro, vira **pendência** com o motivo.
   Uma pendência nunca derruba o programa.
4. Para cada OP válida: linha, produto e especificação (título + texto, ou
   `Padrão da linha X`).
5. Montar o **plano de ações** do robô de cada pedido. Em ensaio, o plano termina em
   `Cancelar`; com `--confirmar`, em `Confirmar`.
6. Emissão **idempotente**: um registro `emitidos.csv` na pasta de saída. Rodar duas
   vezes com `--confirmar` não emite nada de novo. Em ensaio, nada é registrado.
7. Uma emissão que falha é registrada no log e o robô segue para o próximo pedido.
8. Relatório Excel `fila_AAAA-MM-DD.xlsx` com duas abas, `Fila` e `Pendências`,
   cabeçalho estilizado, larguras ajustadas, filtro, painel congelado e `FALHA` em
   vermelho (formatação condicional).
9. E-mail-resumo `resumo_AAAA-MM-DD.eml` para o supervisor, com a planilha anexada.
   **Não envie**: só salve o arquivo.
10. Log em arquivo (`robo_expedicao.log`) e no terminal.
11. Código de saída: `0` se tudo certo, `1` se algum pedido falhou.

Para a emissão, use um **emissor simulado** (uma função ou classe que devolve
`000001`, `000002`...). Ele tem a mesma "cara" do robô real: recebe um pedido e
devolve o número do certificado.

## Extras opcionais

- Ligar o robô Playwright de verdade (`exemplos/09_robo_certificados.py`) no lugar do
  emissor simulado, rodando contra o simulador `dados/simulador_certificados.html`.
- Mover os `.eml` processados para `processados/` e os com pendência para `revisar/`,
  sem sobrescrever nada.
- Opção `--desde AAAA-MM-DD` que ignora e-mails mais antigos (cabeçalho `Date`).
- Testes com `pytest` para `ler_email`, `montar_fila` e `processar` (use `tmp_path`).
- Agendar no Agendador de Tarefas do Windows com um `.bat` (aula, seção 10).

## Exemplo de execução

```text
> python 12-automacao-e-integracao/desafio/solucao_referencia.py
09:54:24 INFO    Início (ENSAIO)
09:54:24 INFO    3 pedido(s) na fila, 2 pendência(s)
09:54:24 WARNING Pendência em pedido_004.eml: NF não encontrado no e-mail
09:54:24 WARNING Pendência em pedido_005.eml: OP 125310 sem cadastro
09:54:24 INFO    OP 123456: plano com 7 ações, termina em Cancelar
09:54:24 INFO    OP 123789: plano com 7 ações, termina em Cancelar
09:54:24 INFO    OP 124001: plano com 7 ações, termina em Cancelar
09:54:24 INFO    Gerados: fila_2026-10-29.xlsx e resumo_2026-10-29.eml

Olá,

Resumo da fila de certificados de 29/10/2026 (MODO ENSAIO: nada foi emitido).

Pedidos na fila: 3 (4.540,75 kg)
  - OP 123456 / NF 98765: ENSAIO
  - OP 123789 / NF 98766: ENSAIO
  - OP 124001 / NF 98770: ENSAIO

Pendências: 2
  - pedido_004.eml: NF não encontrado no e-mail
  - pedido_005.eml: OP 125310 sem cadastro

Planilha completa em anexo.

Robô da expedição
```

Com `--confirmar`, os pedidos aparecem como `EMITIDO 000001`, `EMITIDO 000002`... Na
segunda execução com `--confirmar`, todos aparecem como `JÁ EMITIDO`.

## Critérios de aceite

- [ ] Roda sem argumentos usando os dados de exemplo e termina com código 0.
- [ ] Os 3 pedidos válidos entram na fila; os 2 problemáticos viram pendências com motivo.
- [ ] Em ensaio, nenhum plano contém `Confirmar` e `emitidos.csv` não é criado.
- [ ] Duas execuções seguidas com `--confirmar` geram 3 linhas no registro, não 6.
- [ ] A planilha abre no Excel com as abas `Fila` e `Pendências` formatadas.
- [ ] O `.eml` abre no Outlook com o texto do resumo e a planilha anexada.
- [ ] O log em arquivo conta a história da execução (início, pendências, emissões, fim).
- [ ] Nenhuma senha, e-mail real ou caminho pessoal está escrito no código.
- [ ] `ruff check` e `ruff format --check` passam.

## Dicas de como começar

1. Comece pelo **núcleo sem efeitos colaterais**: uma função que recebe os bytes de um
   `.eml` e devolve um pedido (você já fez isso no exercício 11).
2. Depois, `montar_fila(pasta, ops)` devolvendo `(fila, pendencias)`. Teste no REPL.
3. O plano de ações é o exercício 12; a fila idempotente é o exercício 13.
4. Só no fim junte as saídas (Excel, e-mail, log) e o `argparse`.
5. Use uma `dataclass Pedido` (módulo 08) para não carregar dicionários soltos por aí.
6. Rode em ensaio dezenas de vezes. Só use `--confirmar` quando o ensaio estiver perfeito.

A solução de referência está em `solucao_referencia.py`. Tente antes de abrir.
