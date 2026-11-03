# Desafio do módulo 10 — Relatório mensal da qualidade

## Contexto

Todo começo de mês, alguém do laboratório passa uma manhã montando o mesmo relatório:
filtra as medições do mês na planilha, confere bobina por bobina contra as
especificações, conta aprovadas e reprovadas por linha, pinta de vermelho o que está
fora e cola um gráfico. Você vai transformar essa manhã em **um comando**.

## O que o programa faz

Lê três arquivos de `10-dados-com-pandas/dados/`:

- `medicoes.csv` (CSV brasileiro, UTF-8 com BOM);
- `ops_protheus.csv` (exportação do ERP, `cp1252`), para saber o cliente de cada OP;
- `especificacoes.csv`, com nominal, tolerância (%) e COF máximo de cada produto.

Filtra um mês, confere cada bobina e gera, na pasta `saida/`, um Excel formatado e dois
gráficos em PNG.

## Requisitos obrigatórios

1. Linha de comando com `argparse` (módulo 07):
   - `--mes AAAA-MM` (opcional; sem ele, use o último mês que aparece nos dados);
   - `--produto` (produto do gráfico de controle; padrão `LAM-62`);
   - `--dados` e `--saida` (pastas; padrões: `dados/` e `saida/` do módulo).
2. Leitura correta dos três arquivos (separador, decimal, milhar, encoding, OP como texto).
3. Conferência de cada bobina:
   - espessura e gramatura dentro de nominal ± tolerância (%), limites inclusivos;
   - COF até o máximo, **exceto** se a observação disser "COF: liberado" (em qualquer
     combinação de maiúsculas);
   - status `APROVADA`, `REPROVADA` ou `PENDENTE`, e uma coluna `motivo`
     (ex.: `"espessura; gramatura"`);
   - produto sem especificação ou OP sem cadastro no ERP é `PENDENTE`, nunca aprovado.
4. Excel `relatorio_qualidade_AAAA-MM.xlsx` com três abas:
   - **Resumo**: por linha de produção, bobinas, aprovadas, reprovadas, pendentes, peso
     total (kg) e % de aprovadas, com uma linha de **Total** no fim;
   - **Não conformidades**: só as bobinas reprovadas ou pendentes;
   - **Medições**: todas as bobinas do mês, com status e motivo.
   - Em todas: cabeçalho destacado, largura de coluna ajustada, painel congelado. Linhas
     reprovadas em vermelho claro (`FFC7CE`) e pendentes em amarelo (`FFEB9C`).
5. `aprovacao_AAAA-MM.png`: barras com o % de aprovadas por linha, com título e rótulos.
6. `controle_AAAA-MM.png`: gráfico de controle da espessura do `--produto` no mês, com
   média e limites ± 3σ calculados nos **meses anteriores** (referência). Se não houver
   histórico, calcule no próprio mês e avise.
7. Mês sem medições ou arquivo inexistente: mensagem clara em português e código de
   saída 1 (sem traceback).

## Extras opcionais

- Aba "Por cliente" com bobinas e peso por cliente (use o `cliente` do ERP).
- Inserir os PNG dentro do Excel (`openpyxl.drawing.image.Image`).
- Opção `--todas` para gerar um relatório por mês, de uma vez.
- Testes com pytest para `conferir` e `resumir`, usando DataFrames pequenos.
- Repetir a análise com a planilha `planilha_linhas.xlsx` (4 abas) em vez do CSV.

## Exemplo de execução

```text
> python 10-dados-com-pandas/desafio/solucao_referencia.py --mes 2026-08
Relatório de 2026-08: 19 bobinas
linha  bobinas  aprovadas  reprovadas  pendentes  peso_total_kg  pct_aprovadas
    A        3          3           0          0         3376.1          100.0
    B        3          2           1          0         3353.2           66.7
    C        4          3           1          0         4843.0           75.0
    D        9          6           3          0        10585.7           66.7
Total       19         14           5          0        22158.0           73.7
LAM-62: média 61.17 µm, LIC 50.68, LSC 71.66, 0 ponto(s) fora de controle
Arquivos em ...\10-dados-com-pandas\saida: relatorio_qualidade_2026-08.xlsx, aprovacao_2026-08.png, controle_2026-08.png
```

```text
> python 10-dados-com-pandas/desafio/solucao_referencia.py --mes 2025-01
Erro: não há medições em 2025-01. Meses disponíveis: 2026-07, 2026-08, 2026-09
```

## Critérios de aceite

- [ ] Roda sem argumentos e gera os três arquivos em `saida/`.
- [ ] `--mes 2026-08` mostra 19 bobinas: 14 aprovadas e 5 reprovadas.
- [ ] `--mes 2026-09` mostra 10 pendentes na linha A (produto PE-90 sem especificação e
      OP 024499 sem cadastro no ERP).
- [ ] A bobina 024430-03 (COF 0,38, "COF: liberado") aparece como aprovada em julho.
- [ ] O Excel abre sem aviso de reparo, com as três abas formatadas e cores corretas.
- [ ] Os gráficos têm título e rótulos nos dois eixos.
- [ ] Mês inexistente dá mensagem amigável e código de saída 1.
- [ ] `ruff check` e `ruff format --check` passam no seu arquivo.

## Dicas de como começar

1. Comece pela **leitura**: uma função `ler_dados(pasta)` que devolve uma tabela só
   (medições + cliente + especificação, com dois `merge` `how="left"`). Imprima
   `df.dtypes` e `df.shape` para conferir.
2. Escreva `conferir(df)` como no "No mundo real" da aula: máscaras para cada regra,
   coluna `motivo` montada com `.loc`, e as pendências por último.
3. `pd.crosstab(df["linha"], df["status"])` dá quase o resumo inteiro de graça.
4. Só depois cuide do Excel e dos gráficos. Reaproveite o exemplo 12 (formatação) e o
   exemplo 14 (gráfico de controle).
5. Deixe o `main()` curto: ler argumentos, chamar as funções, imprimir o resumo.

A solução de referência está em `solucao_referencia.py`. Tente antes de abrir!
