# Desafio do módulo 02 — Inspetor de série no terminal

## Contexto

No fim de cada bobina, o operador mede a espessura em vários pontos e anota numa folha. O laboratório quer trocar a folha por um programa simples de terminal: o operador informa a linha e o nominal, digita as leituras uma a uma e o programa responde na hora se cada leitura está boa. Se o processo sair de controle, o programa manda parar a linha. No fim, emite o veredito da série.

É o primeiro programa **interativo e que decide** do curso: junta validação, `while`, `match-case`, contadores, acumuladores, máximo e mínimo, `break` e `continue`.

## Requisitos obrigatórios

1. Crie o arquivo `inspetor.py` (pode ser dentro de `desafio/`).
2. **Linha de produção:** pergunte a linha (A, B, C ou D), aceitando minúsculas e espaços. Use `match-case` para obter a tolerância (A e B: 5%, C: 8%, D: 10%). Linha desconhecida: avise e **pergunte de novo** (laço de validação).
3. **Nominal:** pergunte a espessura nominal em µm, aceitando vírgula. Se não for um número maior que zero, avise e pergunte de novo. Não use `try/except` (é do módulo 06): valide o texto antes de converter.
4. Mostre a faixa aceita (nominal ± tolerância), com 2 casas.
5. **Leituras:** leia as medições uma a uma até o operador digitar `fim`:
   - Enter vazio é ignorado sem aviso;
   - texto que não é número gera um aviso e não conta;
   - cada leitura válida é classificada na hora: `OK`, `FORA (abaixo)` ou `FORA (acima)` (limites inclusivos);
   - **regra de parada:** 3 leituras válidas **seguidas** fora da faixa encerram a leitura com o alerta `PARE A LINHA`.
6. **Relatório final:** quantidade de leituras válidas, média, mínima, máxima, amplitude (máxima - mínima), quantidade e porcentagem fora da faixa. Sem `sum()`, `min()` ou `max()`: use os padrões da aula.
7. **Veredito:**
   - `REPROVADO (processo fora de controle)` se a regra de parada disparou;
   - senão, `REPROVADO (muitas leituras fora)` se mais de 20% das leituras ficaram fora;
   - senão, `CONDICIONAL` se houve alguma fora;
   - senão, `APROVADO`.
   Sem nenhuma leitura válida, diga isso em vez de dividir por zero.
8. **Modo demonstração:** o programa precisa conseguir rodar **sem ninguém digitar nada**, usando respostas de exemplo, para você (e o professor) testarem rápido. Uma constante `MODO_DEMO = True` no topo liga esse modo. Dica de implementação na seção "Dicas".
9. Roda sem erro e passa no `ruff check`.

## Extras opcionais

- **Limite de segurança:** pare depois de 50 leituras válidas, mesmo sem `fim`.
- **Maior sequência:** informe no relatório a maior sequência de leituras seguidas fora.
- **Gramatura também:** pergunte no início qual ensaio será feito (espessura ou gramatura, com `match-case`) e ajuste a unidade das mensagens.
- **Formato brasileiro:** mostre os números com vírgula decimal no relatório (técnica do exercício 01.12).
- **Volte ao desafio do módulo 01:** acrescente à ficha da bobina o veredito automático (dentro ou fora da faixa).

## Exemplo de execução

Modo demonstração (as respostas aparecem depois de cada pergunta, como se alguém tivesse digitado):

```text
PS C:\curso-python> python 02-decisoes-e-repeticoes\desafio\solucao_referencia.py
==============================================
        INSPETOR DE SÉRIE — ESPESSURA
==============================================
Linha (A, B, C ou D): E
  Linha desconhecida. Tente de novo.
Linha (A, B, C ou D): b
Espessura nominal (µm): abc
  Digite um número maior que zero, como 25 ou 25,5.
Espessura nominal (µm): 0
  Digite um número maior que zero, como 25 ou 25,5.
Espessura nominal (µm): 25
Faixa da linha B (±5%): 23.75 a 26.25 µm
Digite as leituras (Enter vazio é ignorado; 'fim' encerra).
  Leitura 1: 25,3
    25.30 µm -> OK
  Leitura 2:
  Leitura 2: 24,9
    24.90 µm -> OK
  Leitura 3: xx
    Leitura inválida, não contada.
  Leitura 3: 26,8
    26.80 µm -> FORA (acima)
  Leitura 4: 25,1
    25.10 µm -> OK
  Leitura 5: 24,6
    24.60 µm -> OK
  Leitura 6: 25,0
    25.00 µm -> OK
  Leitura 7: 25,2
    25.20 µm -> OK
  Leitura 8: fim
----------------------------------------------
Leituras válidas                             7
Média (µm)                               25.27
Mínima / máxima (µm)             24.60 / 26.80
Amplitude (µm)                            2.20
Fora da faixa                          1 (14%)
Veredito: CONDICIONAL (avaliar com o líder)
==============================================
```

Modo interativo, disparando a regra de parada (linha D, nominal 20 µm, faixa 18 a 22):

```text
  Leitura 1: 18,1
    18.10 µm -> OK
  Leitura 2: 17,5
    17.50 µm -> FORA (abaixo)
  Leitura 3: 22,9
    22.90 µm -> FORA (acima)
  Leitura 4: 17
    17.00 µm -> FORA (abaixo)
    !!! 3 seguidas fora: PARE A LINHA.
----------------------------------------------
Leituras válidas                             4
Média (µm)                               18.88
Mínima / máxima (µm)             17.00 / 22.90
Amplitude (µm)                            5.90
Fora da faixa                          3 (75%)
Veredito: REPROVADO (processo fora de controle)
==============================================
```

## Critérios de aceite

- [ ] Com `MODO_DEMO = True`, o programa roda do começo ao fim sem pedir nada.
- [ ] Com `MODO_DEMO = False`, ele pergunta de verdade e funciona com digitação.
- [ ] Linha inválida e nominal inválido (texto, zero, vazio) fazem o programa perguntar de novo, sem quebrar.
- [ ] Nenhuma entrada digitada derruba o programa com `ValueError` (teste `abc`, `25,4,1`, `-3`, `.`).
- [ ] Os limites da faixa contam como dentro (teste uma leitura exatamente igual ao mínimo).
- [ ] Uma leitura boa no meio "zera" a contagem de seguidas fora.
- [ ] Três seguidas fora encerram as leituras com o alerta.
- [ ] O relatório não divide por zero quando não há leituras válidas (digite `fim` logo de cara).
- [ ] O veredito segue a ordem de prioridade dos requisitos.
- [ ] Não há `while` sem uma saída garantida (`break` ou condição que fica falsa).
- [ ] `ruff check` não reclama.

## Dicas de como começar

1. **Comece sem interação.** Escreva primeiro o "miolo" com as leituras numa lista fixa (`for texto in ["25,3", "xx", ...]`), como o exemplo `exemplos/10_inspecao_serie.py`. Só depois troque a lista por perguntas.
2. **Um laço por pergunta.** A linha e o nominal usam o mesmo molde: `while True:` → pergunta → se válido, `break` → senão, avisa. Escreva um, teste, copie o molde para o outro.
3. **Modo demonstração sem índice de lista:** guarde as respostas de exemplo numa lista e escreva uma função `ler(passo, pergunta)`. O programa principal conta as perguntas (`passo += 1` antes de cada uma) e a função percorre a lista com um contador até chegar à resposta número `passo` (é o padrão "buscar posição" da aula). Se `MODO_DEMO` for `False`, a função simplesmente devolve `input(pergunta)`.
4. **Valide o número antes de converter:** reaproveite a ideia do exercício 14 (`eh_numero`).
5. **Teste de mesa** com a sequência `ok, fora, fora, ok, fora, fora, fora`: em que leitura o alerta deve disparar? Confira se o seu programa concorda.
6. Para sair de um programa travado num loop infinito: `Ctrl+C`.

A solução de referência está em `solucao_referencia.py`. Tente o seu antes de abrir.
