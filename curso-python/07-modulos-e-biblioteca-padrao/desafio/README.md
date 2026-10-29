# Desafio do Módulo 07 — Agenda de validade de laudos

## Contexto

Todo laudo de qualidade vence. Hoje alguém do laboratório abre a planilha de laudos,
calcula na mão quanto falta para cada um vencer e avisa a expedição. Esquecer um
laudo vencido significa material parado no cliente.

Seu desafio: um **programa de linha de comando** que lê a lista de laudos e mostra,
numa olhada, o que já venceu e o que vence nos próximos dias. Ele junta quase tudo
do módulo: `datetime`, `collections`, `argparse`, `os`, `sys` e organização em
funções (ou em um pacote, no extra).

Os dados estão em `../dados/laudos.csv` (UTF-8, separador `;`):

```text
op;cliente;produto;emissao;validade_dias
OP244801;Alimentos Bom Sabor;Filme PE 25 µm;02/04/2026;180
OP244930;Café Montanha;Laminado BOPP/PE;10/09/2025;365
...
```

## Requisitos obrigatórios

1. Ler o CSV e calcular o **vencimento** de cada laudo (emissão + validade em dias).
2. Aceitar a **data de referência** com `--hoje dd/mm/aaaa`. Sem a opção, usar a data
   de hoje do computador.
3. Separar os laudos em três grupos:
   - **vencidos**: vencimento antes da data de referência;
   - **a vencer**: vencem em até N dias (`--janela N`, inclusive);
   - **em dia**: o resto.
4. A janela padrão vem da variável de ambiente `LAB_JANELA_DIAS`. Se ela não existir,
   use 30 dias.
5. Mostrar os vencidos e os a vencer **em ordem de vencimento**, com OP, cliente, data
   de vencimento e um texto amigável ("amanhã", "em 7 dias", "há 3 dias"). Para os a
   vencer, mostrar também o dia da semana em português.
6. Mostrar um resumo **por cliente** com quantos vencidos e quantos a vencer (use
   `Counter`).
7. Arquivo inexistente: mensagem no `stderr` e código de saída 2. Data inválida em
   `--hoje`: mensagem amigável do argparse (código 2).
8. Com `--estrito`, terminar com código de saída 1 quando houver laudo vencido (assim
   o Agendador de Tarefas do Windows marca a execução como "falha" e alguém olha).
9. Funções pequenas com docstring, `main(argv=None)` e
   `if __name__ == "__main__": sys.exit(main())` no final.

## Extras opcionais

- `--cliente texto`: filtra pelos clientes cujo nome contém o texto (sem diferenciar
  maiúsculas).
- `--json caminho`: também grava o resultado em JSON (datas como texto `dd/mm/aaaa`).
- Linhas com data ou validade inválidas são ignoradas com um aviso no `stderr`, sem
  derrubar o programa.
- Transformar o programa num **pacote** `agenda_laudos/` com `datas.py`, `leitura.py`,
  `relatorio.py`, `cli.py` e `__main__.py`, e rodar com `python -m agenda_laudos`.
- Avisar quando o vencimento cair num sábado ou domingo (a renovação tem de ser feita
  antes).

## Exemplo de execução

```text
> python 07-modulos-e-biblioteca-padrao/desafio/solucao_referencia.py --hoje 29/10/2026
Agenda de laudos em 29/10/2026 (janela: 30 dias)

VENCIDOS (5)
  OP244930  Café Montanha          venceu em 10/09/2026 (há 49 dias)
  OP244801  Alimentos Bom Sabor    venceu em 29/09/2026 (há 30 dias)
  OP244815  Alimentos Bom Sabor    venceu em 17/10/2026 (há 12 dias)
  OP245066  Pet Nutri              venceu em 26/10/2026 (há 3 dias)
  OP245094  Higiene Total          venceu em 27/10/2026 (há 2 dias)

VENCEM EM ATÉ 30 DIAS (6)
  OP245010  Higiene Total          vence em 30/10/2026, sexta (amanhã)
  OP245041  Laticínios Serra Azul  vence em 30/10/2026, sexta (amanhã)
  OP245058  Alimentos Bom Sabor    vence em 30/10/2026, sexta (amanhã)
  OP244977  Café Montanha          vence em 05/11/2026, quinta (em 7 dias)
  OP245022  Higiene Total          vence em 10/11/2026, terça (em 12 dias)
  OP244902  Laticínios Serra Azul  vence em 11/11/2026, quarta (em 13 dias)

Em dia: 3 laudo(s)

Por cliente (vencidos / a vencer):
  Alimentos Bom Sabor    2 / 1
  Café Montanha          1 / 1
  Higiene Total          1 / 2
  Laticínios Serra Azul  0 / 2
  Pet Nutri              1 / 0
```

Com filtro e janela menor:

```text
> python 07-modulos-e-biblioteca-padrao/desafio/solucao_referencia.py --hoje 29/10/2026 --janela 7 --cliente café
Agenda de laudos em 29/10/2026 (janela: 7 dias)

VENCIDOS (1)
  OP244930  Café Montanha          venceu em 10/09/2026 (há 49 dias)

VENCEM EM ATÉ 7 DIAS (1)
  OP244977  Café Montanha          vence em 05/11/2026, quinta (em 7 dias)

Em dia: 1 laudo(s)

Por cliente (vencidos / a vencer):
  Café Montanha          1 / 1
```

Para ver o código de saída no PowerShell, rode o programa e depois `$LASTEXITCODE`
(no Linux/macOS: `echo $?`).

## Critérios de aceite

- [ ] Roda sem argumentos (usa `dados/laudos.csv` e a data de hoje).
- [ ] Com `--hoje 29/10/2026`, mostra 5 vencidos, 6 a vencer e 3 em dia.
- [ ] Os grupos aparecem em ordem de vencimento.
- [ ] `--janela 7` muda a lista "a vencer"; sem `--janela`, vale `LAB_JANELA_DIAS` ou 30.
- [ ] `--hoje 2026-10-29` mostra a mensagem de uso e termina com código 2.
- [ ] Arquivo inexistente: mensagem no `stderr` e código 2, sem traceback.
- [ ] `--estrito` devolve 1 quando há vencidos e 0 quando não há.
- [ ] O código tem `main(argv=None)` e o bloco `if __name__ == "__main__":`.
- [ ] `ruff check` e `ruff format --check` passam.

## Dicas para começar

1. **Decomponha antes de digitar.** Escreva no papel as etapas: ler → calcular
   vencimento → classificar → imprimir. Cada etapa vira uma função.
2. Comece pela função mais simples e teste no REPL:
   `classificar([...], date(2026, 10, 29), 30)` com dois ou três dicionários feitos à
   mão.
3. Só depois de as funções funcionarem, escreva o `argparse`. Teste o parser com
   `criar_parser().parse_args(["--hoje", "29/10/2026"])`, sem precisar do terminal.
4. Para a variável de ambiente, no PowerShell: `$env:LAB_JANELA_DIAS = "15"`; no
   Linux/macOS: `export LAB_JANELA_DIAS=15`.
5. Travou? Compare com a `solucao_referencia.py` **depois** de tentar. Ela tem um
   jeito de fazer, não o único.
