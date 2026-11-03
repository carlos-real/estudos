# Desafio do módulo 06 — Conferência de laudos em lote

## Contexto

Toda manhã, cada linha de produção (A, B, C e D) deixa um CSV exportado do Excel na
pasta de laudos. O analista abre um por um, confere as medições contra a especificação
e monta à mão a lista do que pode ser liberado. Quando um arquivo vem com problema, a
conferência inteira atrasa.

Sua missão: escrever `conferir_laudos.py`, que faz essa conferência sozinho e **não
para no primeiro problema**.

```text
dados/
  regras_tolerancia.json      regras por linha: espessura e gramatura (nominal ± %), COF (mín/máx)
  laudos/
    laudos_linha_A.csv        "CSV UTF-8" (com BOM)
    laudos_linha_B.csv        "CSV (separado por vírgulas)" em cp1252, coluna "Observação"
    laudos_linha_C.csv        alguém digitou "2O,1" (letra O) no lugar de "20,1"
    laudos_linha_D.csv        exportado sem a coluna "cof"
    leia-me.txt               não é laudo: deve ser ignorado
```

As colunas dos laudos são `lote;linha;espessura;gramatura;cof;observacao` (com variações
de maiúsculas e acentos no cabeçalho). A observação pode liberar um ensaio que ficou
fora da faixa: `COF: liberado`, `espessura: liberada`.

## Requisitos obrigatórios

1. Carregar as regras de `dados/regras_tolerancia.json`. Se o JSON estiver quebrado,
   **parar** com uma exceção `ArquivoInvalido` dizendo o arquivo e a linha do erro.
2. Processar todos os `.csv` de `dados/laudos/` em ordem alfabética, ignorando os
   outros arquivos.
3. Ler cada CSV com o encoding certo (UTF-8 com BOM ou cp1252) usando o módulo `csv`,
   com os nomes de coluna normalizados (sem espaços, minúsculos, sem acento).
4. Validar cada arquivo: colunas obrigatórias (`lote`, `linha`, `espessura`,
   `gramatura`, `cof`) e números no formato brasileiro. Qualquer problema levanta
   `ArquivoInvalido` com uma mensagem que diga a linha e a coluna.
5. Arquivo inválido é recusado **inteiro** (nenhum lote dele entra no resultado), o erro
   é mostrado na tela e o programa segue com os próximos arquivos.
6. Conferir cada lote contra a regra da sua linha de produção:
   - `APROVADO`: os três ensaios dentro da faixa (limites inclusive);
   - `APROVADO COM LIBERAÇÃO`: algum ensaio fora, mas todos os que estão fora foram
     liberados na observação;
   - `REPROVADO`: algum ensaio fora e não liberado.
   O motivo (ensaios fora e a faixa) acompanha o status.
7. Gravar em `desafio/saida/`:
   - `resultado.csv` no padrão do Excel brasileiro (`;`, vírgula decimal, `utf-8-sig`,
     `newline=""`), com `arquivo;lote;linha;espessura;gramatura;cof;status;motivo`;
   - `resumo.json` (legível, com acentos) com arquivos lidos, arquivos recusados e o
     motivo, total de lotes e a contagem por status, gravado de forma **atômica**
     (temporário + `replace`);
   - `erros.log`, acrescentando (modo `"a"`) uma linha por arquivo recusado.
8. Usar uma família de exceções própria (`ErroDeQualidade` como mãe de
   `ArquivoInvalido` e de pelo menos mais uma).
9. Se o `resultado.csv` estiver aberto no Excel (`PermissionError`), mostrar uma
   mensagem clara ("feche o arquivo no Excel") em vez de só o traceback.

## Extras opcionais

- Receber a pasta dos laudos como argumento (`sys.argv`, prévia do módulo 07).
- Gravar também um CSV só com os lotes que podem seguir para emissão de certificado.
- Avisar quando o mesmo lote aparece em dois arquivos.
- Validar também o JSON de regras (toda linha precisa dos três ensaios, e cada regra
  precisa de `nominal` e `tolerancia_pct` ou de `min` e `max`), com `RegraAusente`.
- Calcular a média de cada ensaio por linha de produção e incluir no `resumo.json`.

## Exemplo de execução

Na pasta `curso-python`:

```text
python 06-arquivos-e-erros/desafio/conferir_laudos.py
```

Saída da solução de referência:

```text
[OK]       laudos_linha_A.csv: 4 lotes
[OK]       laudos_linha_B.csv: 3 lotes
[RECUSADO] laudos_linha_C.csv: linha 3: valor inválido em espessura: '2O,1'
[RECUSADO] laudos_linha_D.csv: colunas ausentes: cof

Lote    Linha  Status                  Motivo
A-0153  A      APROVADO
A-0154  A      REPROVADO               espessura 27,90 fora de [22,50; 27,50]
A-0155  A      APROVADO COM LIBERAÇÃO  cof 0,33 fora de [0,15; 0,30]
A-0156  A      REPROVADO               gramatura 21,50 fora de [21,85; 24,15]
B-0201  B      APROVADO
B-0202  B      APROVADO COM LIBERAÇÃO  cof 0,27 fora de [0,15; 0,25]
B-0203  B      APROVADO

Lotes conferidos: 7 | APROVADO: 3 | APROVADO COM LIBERAÇÃO: 2 | REPROVADO: 2
Arquivos gravados em: saida/ (resultado.csv, resumo.json, erros.log)
```

E o `resumo.json` gerado:

```json
{
  "arquivos_lidos": 2,
  "arquivos_recusados": {
    "laudos_linha_C.csv": "linha 3: valor inválido em espessura: '2O,1'",
    "laudos_linha_D.csv": "colunas ausentes: cof"
  },
  "lotes": 7,
  "por_status": {
    "APROVADO": 3,
    "APROVADO COM LIBERAÇÃO": 2,
    "REPROVADO": 2
  }
}
```

O seu layout na tela pode ser diferente. Os status, as contagens e os arquivos recusados
devem ser os mesmos.

## Critérios de aceite

- [ ] Roda sem erro e sem pedir nada ao usuário.
- [ ] 7 lotes conferidos: 3 aprovados, 2 aprovados com liberação, 2 reprovados.
- [ ] `laudos_linha_C.csv` recusado com mensagem citando a linha 3 e o valor `'2O,1'`;
      `laudos_linha_D.csv` recusado por falta da coluna `cof`; nenhum lote dos dois no
      resultado.
- [ ] `leia-me.txt` ignorado.
- [ ] `resultado.csv` abre no Excel em colunas, com acentos e vírgula decimal certos.
- [ ] `resumo.json` legível (acentos sem `\u00e7`) e gravado via arquivo temporário.
- [ ] Rodar duas vezes não duplica o `resultado.csv` nem o `resumo.json` (só o
      `erros.log` cresce).
- [ ] Nenhum `except:` sozinho; cada `except` captura um tipo específico.
- [ ] Funções pequenas, cada uma com uma responsabilidade (ler regras, ler laudo,
      conferir lote, gravar saídas).

## Dicas de como começar

1. **Comece pelas regras.** Carregue o JSON e escreva `faixa(regras, linha, ensaio)`,
   que devolve `(mínimo, máximo)` para os dois tipos de regra. Teste no REPL para a
   linha A: espessura de 22,50 a 27,50; COF de 0,15 a 0,30.
2. **Depois, um laudo.** Reaproveite o exercício 13 (`ler_medicoes`): ele já resolve
   encoding, cabeçalho e números. Acrescente a coluna `cof` e a `observacao` opcional.
3. **Liberações.** A observação "COF: liberado; espessura: liberada" vira o conjunto
   `{"cof", "espessura"}`. Normalize (sem acento, minúsculo) e use uma regex por ensaio
   (módulo 05, "No mundo real").
4. **O lote inteiro de uma vez.** Monte as linhas de resultado de um arquivo numa lista
   e só junte ao resultado geral depois que o arquivo inteiro deu certo (exercício 14).
5. **Saídas por último.** `csv.DictWriter` para o resultado, gravação atômica para o
   JSON (exercício 12) e modo `"a"` para o log (exercício 4). Para a data e hora do log,
   `datetime.now().strftime("%Y-%m-%d %H:%M:%S")` (do módulo `datetime`, que você verá no
   módulo 07).
6. **Teste o pior caso.** Abra o `resultado.csv` no Excel e rode de novo: a mensagem do
   `PermissionError` aparece?

A solução de referência está em `solucao_referencia.py`. Abra só depois de tentar.
