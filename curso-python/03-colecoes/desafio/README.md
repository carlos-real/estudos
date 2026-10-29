# Desafio do módulo 03 — Painel de conferência do lote

## Contexto

Fim de turno no laboratório. A planilha do dia tem 10 amostras das linhas A a D. A expedição mandou por e-mail os pedidos de amanhã (OP, NF e peso). Antes de emitir os certificados, o supervisor quer um painel no terminal com:

- cada amostra conferida contra as tolerâncias da linha;
- um resumo por linha;
- as maiores não conformidades de espessura;
- a fila de certificados, com o que está bloqueado e o que nem tem resultado.

Você vai montar esse painel usando só coleções (e funções simples com `def` e `return`, como no "molde" dos exercícios).

## Dados de entrada

Crie o arquivo `desafio/painel.py` e cole estes dados no topo. No projeto final, eles virão da planilha (openpyxl) e do e-mail; por enquanto, estão no código.

```python
TOLERANCIAS = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "B": {
        "espessura": {"nominal": 20.0, "tol_pct": 8.0},
        "gramatura": {"nominal": 18.5, "tol_pct": 5.0},
        "cof": {"min": 0.20, "max": 0.40},
    },
    "C": {
        "espessura": {"nominal": 35.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 32.0, "tol_pct": 6.0},
        "cof": {"min": 0.15, "max": 0.30},
    },
    "D": {
        "espessura": {"nominal": 70.0, "tol_pct": 7.0},
        "gramatura": {"nominal": 65.0, "tol_pct": 5.0},
        "cof": {"min": 0.10, "max": 0.25},
    },
}

COLUNAS = ("op", "linha", "espessura", "gramatura", "cof", "obs")
PLANILHA = [
    ("OP-5101", "A", 50.4, 46.3, 0.22, ""),
    ("OP-5102", "A", 55.8, 46.9, 0.24, ""),
    ("OP-5103", "B", 20.6, 18.9, 0.42, "COF: liberado"),
    ("OP-5104", "B", 19.1, None, 0.30, ""),
    ("OP-5105", "C", 35.9, 32.4, 0.19, ""),
    ("OP-5106", "C", 31.0, 29.5, 0.33, ""),
    ("OP-5107", "D", 71.2, 66.0, 0.12, ""),
    ("OP-5108", "D", 70.4, 64.1, 0.26, "cof: liberado pela supervisão"),
    ("OP-5109", "A", 47.9, 44.0, 0.16, ""),
    ("OP-5110", "D", 64.9, 61.5, 0.11, ""),
]
AMOSTRAS = [dict(zip(COLUNAS, linha, strict=True)) for linha in PLANILHA]

PEDIDOS = [
    {"op": "OP-5101", "nf": "004501", "peso_kg": 1250.5},
    {"op": "OP-5103", "nf": "004502", "peso_kg": 830.0},
    {"op": "OP-5106", "nf": "004503", "peso_kg": 640.2},
    {"op": "OP-5108", "nf": "004504", "peso_kg": 1105.8},
    {"op": "OP-5104", "nf": "004505", "peso_kg": 412.0},
    {"op": "OP-5120", "nf": "004506", "peso_kg": 300.0},
]
```

Regras de tolerância:

- **espessura** e **gramatura**: nominal ± `tol_pct` %. Limites arredondados em 2 casas, e os limites contam como dentro.
- **cof**: faixa fixa `min` a `max`.

## Requisitos obrigatórios

1. **Conferir cada amostra** e produzir uma tabela **nova** (sem alterar `AMOSTRAS`) com duas colunas a mais:
   - `falhas`: lista das propriedades fora da faixa;
   - `status`:
     - `INCOMPLETA` se alguma propriedade da linha está vazia (`None`);
     - `APROVADA` se não há falhas;
     - `LIBERADA` se a **única** falha é o COF e a observação contém "cof: liberado" (sem diferenciar maiúsculas);
     - `REPROVADA` nos demais casos.
2. **Imprimir a tabela** alinhada: OP, linha, espessura, gramatura, COF, status e falhas. Célula vazia aparece como `-`.
3. **Resumo por linha** (em ordem alfabética): quantidade de amostras, quantas podem ser emitidas (APROVADA ou LIBERADA), percentual e espessura média.
4. **Os 3 maiores desvios de espessura**, em módulo, em relação ao nominal da linha, mostrando o sinal (`+11.6%`, `-7.3%`).
5. **Expedição**:
   - pedidos que podem ganhar certificado, com NF, peso e status, e o peso total;
   - pedidos bloqueados (com o motivo);
   - OPs pedidas que não têm resultado no laboratório (use conjuntos).

## Extras opcionais

- Perguntar ao usuário (com `input()`) uma linha (A–D) e mostrar só as amostras dela. Deixe também um jeito de rodar sem perguntar.
- Mostrar os números no formato brasileiro (`1.250,5 kg`). Dica: formate com `:,.1f` e troque os separadores com `replace`.
- Avisar se a mesma OP aparece duas vezes na planilha.
- Ordenar a tabela pela coluna que o usuário escolher.
- Mostrar, para cada falha, o valor medido e a faixa (`espessura 55.8 fora de 45.0 a 55.0`).

## Exemplo de execução

```text
python desafio\painel.py
```

(No Linux/macOS: `python3 desafio/painel.py`.) Saída esperada, para os dados acima:

```text
============================================================
PAINEL DE CONFERÊNCIA DO LOTE
============================================================
OP       Linha   Esp.  Gram.   COF  Status     Fora
OP-5101  A       50.4   46.3  0.22  APROVADA   -
OP-5102  A       55.8   46.9  0.24  REPROVADA  espessura
OP-5103  B       20.6   18.9  0.42  LIBERADA   cof
OP-5104  B       19.1      -  0.30  INCOMPLETA gramatura
OP-5105  C       35.9   32.4  0.19  APROVADA   -
OP-5106  C       31.0   29.5  0.33  REPROVADA  espessura, gramatura, cof
OP-5107  D       71.2   66.0  0.12  APROVADA   -
OP-5108  D       70.4   64.1  0.26  LIBERADA   cof
OP-5109  A       47.9   44.0  0.16  APROVADA   -
OP-5110  D       64.9   61.5  0.11  REPROVADA  espessura, gramatura

--- Resumo por linha ---
Linha  Amostras Liberadas      %  Esp. média
A             3         2  66.7%       51.37
B             2         1  50.0%       19.85
C             2         1  50.0%       33.45
D             3         2  66.7%       68.83

--- 3 maiores desvios de espessura ---
OP-5102 (linha A): +11.6% do nominal
OP-5106 (linha C): -11.4% do nominal
OP-5110 (linha D): -7.3% do nominal

--- Expedição ---
Emitir certificado (3 OPs, 3186.3 kg):
  OP-5101  NF 004501  1250.5 kg  [APROVADA]
  OP-5103  NF 004502  830.0 kg  [LIBERADA]
  OP-5108  NF 004504  1105.8 kg  [LIBERADA]
Bloqueadas:
  OP-5106  REPROVADA: espessura, gramatura, cof
  OP-5104  INCOMPLETA: gramatura
Sem resultado no laboratório: ['OP-5120']
```

O layout pode ser diferente; os números e os status, não.

## Critérios de aceite

- [ ] O programa roda do começo ao fim sem erro e sem pedir nada ao usuário (nos requisitos obrigatórios).
- [ ] Os status das 10 amostras batem com a saída de exemplo (inclusive `OP-5108`, cuja observação está em minúsculas).
- [ ] `AMOSTRAS` e `PEDIDOS` não são alterados (teste: no fim do programa, `"status" not in AMOSTRAS[0]`).
- [ ] O resumo por linha sai em ordem alfabética, com os percentuais corretos.
- [ ] Os 3 maiores desvios são `OP-5102`, `OP-5106` e `OP-5110`, nessa ordem.
- [ ] O peso total a emitir é 3186.3 kg e `OP-5120` aparece como sem resultado.
- [ ] Nenhuma lista é modificada enquanto é percorrida.
- [ ] O código passa no `ruff check` (rode `ruff check desafio` na pasta do módulo).

## Dicas de como começar

1. **Comece pelos dados, não pelo `print`.** Primeiro escreva `faixa(regra)`, que transforma uma regra em `(mínimo, máximo)`. Teste no REPL com `faixa(TOLERANCIAS["A"]["gramatura"])`: deve dar `(43.7, 48.3)`.
2. Depois escreva `conferir(amostra)`, que devolve um dicionário **novo** (`{**amostra, "falhas": ..., "status": ...}`). Teste com uma amostra de cada status.
3. Monte a tabela conferida com uma compreensão: `[conferir(a) for a in AMOSTRAS]`.
4. Só então faça as partes do painel, uma de cada vez, conferindo com a saída de exemplo.
5. Para o resumo por linha, use o padrão "agrupar, depois resumir" da seção 12 da aula.
6. Para a expedição, monte um índice `{op: amostra_conferida}` (o "PROCV" da seção 12).

Travou? A solução de referência está em [solucao_referencia.py](solucao_referencia.py). Tente por pelo menos 30 minutos antes de abrir; depois compare as duas versões e anote o que você faria diferente.
