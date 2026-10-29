# Desafio do módulo 01 — Ficha de medição da bobina

## Contexto

Toda bobina amostrada no laboratório gera uma ficha: OP, linha, cliente, as medições de espessura, a gramatura e algumas estimativas que o PCP e a expedição pedem (peso e diâmetro da bobina). Hoje essa ficha é preenchida à mão numa planilha, com contas feitas na calculadora.

Seu desafio é escrever um script que recebe os dados **brutos** (do jeito que chegam: OP mal digitada, números com vírgula, espaços sobrando) e imprime a ficha completa, calculada e alinhada. Ainda sem decidir "aprovado ou reprovado": isso exige `if`, assunto do módulo 02. Lá você vai voltar a este script e acrescentar o veredito.

## Requisitos obrigatórios

1. Crie o arquivo `ficha_bobina.py` (pode ser dentro de `desafio/`).
2. **Entrada no topo do arquivo**, em variáveis, com dados brutos como texto quando for realista:
   - OP digitada de qualquer jeito (ex.: `"  op-48.213 "`);
   - linha (ex.: `" c "`) e cliente (ex.: `"  embalagens sul ltda "`);
   - **cinco** medições de espessura como texto com vírgula (ex.: `"24,8"`);
   - espessura nominal (µm) e tolerância (%);
   - massa do corpo de prova (texto com vírgula, em g) e as dimensões dele (cm);
   - largura (mm) e comprimento (m) da bobina, e diâmetro do tubete (mm).
3. **Limpeza e conversão:** OP no formato `OP48213`; linha e cliente sem espaços nas pontas e em maiúsculas; medições e massa convertidas para `float`.
4. **Cálculos:**
   - média das cinco medições;
   - limites mínimo e máximo da faixa (nominal ± tolerância %);
   - desvio da média em relação ao nominal, em porcentagem e com sinal (`+0.16%`);
   - gramatura (g/m²) do corpo de prova;
   - peso estimado da bobina (kg);
   - diâmetro estimado da bobina (mm), com a fórmula do exercício 13 (use a espessura média).
5. **Saída:** uma ficha com título centralizado, rótulos alinhados à esquerda e valores alinhados à direita, linhas de separação, espessuras com 2 casas, gramatura com 1 casa e diâmetro sem casas.
6. **Pelo menos duas funções** com `def` e `return` (ex.: `texto_para_float(texto)` e `linha_da_ficha(rotulo, valor)`).
7. Código organizado em blocos comentados: entrada, limpeza, cálculos, saída.
8. Roda sem erro com `python ficha_bobina.py` e passa no `ruff check` sem avisos.

## Extras opcionais

- **Formato brasileiro:** mostre todos os números com vírgula decimal e ponto de milhar (`1.234,56`), reaproveitando a técnica do exercício 12.
- **Bobinas da OP:** dada a produção total da OP em metros, mostre quantas bobinas completas saem e quanto sobra (`//` e `%`).
- **Tempo de produção:** dada a velocidade da máquina, mostre quanto tempo falta e o horário previsto de término (exercício 14).
- **Versão interativa:** troque as variáveis de entrada por `input()`. Lembre que `input()` sempre devolve texto.

## Exemplo de execução

Com os dados de exemplo da solução de referência (que implementa também os extras de formato brasileiro e de bobinas da OP):

```text
PS C:\curso-python> python 01-fundamentos\desafio\solucao_referencia.py
============================================
         FICHA DE MEDIÇÃO DA BOBINA
============================================
OP                                   OP48213
Linha                                      C
Cliente                   EMBALAGENS SUL LTDA
--------------------------------------------
Medições (µm):
            24,8 | 25,3 | 25,1 | 24,6 | 25,4
Espessura média (µm)                   25,04
Nominal (µm)                       25,0 ± 8%
Faixa aceita (µm)              23,00 a 27,00
Desvio do nominal                     +0,16%
--------------------------------------------
Gramatura (g/m²)                        47,1
Peso estimado (kg)                    180,86
Diâmetro estimado (mm)                   444
Bobinas na OP               7 + sobra 3500 m
============================================
Veredito automático: fica para o módulo 02 (if/else).
```

Sua ficha não precisa ser idêntica. O importante é estar correta, legível e alinhada.

## Critérios de aceite

- [ ] O script roda do começo ao fim sem erro e sem pedir nada ao usuário (exceto na versão interativa).
- [ ] A OP sai no formato `OP` + número, sem espaços, hífens ou pontos, qualquer que seja a forma digitada.
- [ ] As cinco medições com vírgula são convertidas corretamente (confira a média na calculadora).
- [ ] A faixa de 25 µm ± 8% sai como 23,00 a 27,00 (ou 23.00 a 27.00).
- [ ] A gramatura de 0,4710 g em 10 cm × 10 cm sai como 47,1 g/m².
- [ ] Os valores estão alinhados à direita numa mesma coluna.
- [ ] Nenhum arredondamento no meio das contas: só na exibição.
- [ ] Existem pelo menos duas funções com `return`, e elas são usadas.
- [ ] Os nomes de variáveis dizem o que guardam e incluem a unidade quando há dúvida.
- [ ] `ruff check` e `ruff format --check` não reclamam do arquivo.

## Dicas de como começar

1. **Comece pela entrada e pela saída**, sem cálculo nenhum: crie as variáveis e imprima a ficha com valores fixos (`"???"`). Rode. Ver o "esqueleto" da ficha na tela dá ânimo e mostra o que falta.
2. **Uma conta por vez.** Faça a limpeza da OP e rode. Depois a conversão das medições e rode. Depois a média e rode. Nunca escreva 30 linhas sem rodar.
3. **Confira com um caso que você sabe de cabeça.** Troque as cinco medições por `"25,0"`: a média tem que dar 25 e o desvio, 0%.
4. **Teste fórmulas no REPL** antes de colocar no arquivo, como na seção 15 da aula.
5. Travou no alinhamento? Volte à seção 11 (f-strings) e teste `f"[{'texto':>18}]"` no REPL com larguras diferentes.
6. Só depois de tudo funcionando, pense nos extras.

A solução de referência está em `solucao_referencia.py`. Tente o seu antes de abrir.
