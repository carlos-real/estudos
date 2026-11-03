# Desafio do módulo 04 — Fila de emissão de certificados

## Contexto

Fim do dia. A expedição mandou os pedidos de amanhã (OP, NF e peso), alguns com erro de digitação. O laboratório tem os resultados de quase todas as OPs. Algumas OPs têm **especificação própria** (título + regras); as outras seguem o **padrão da linha**. E a qualidade pode liberar um COF fora da faixa com a observação "COF: liberado".

Seu programa monta a **fila de emissão**: o texto de cada certificado que pode sair e a lista de pendências, com o motivo de cada uma. É o núcleo do projeto final, só que com os dados no código (planilha, banco e e-mail entram nos próximos módulos).

O objetivo principal não é só "funcionar": é **decompor** o problema em funções pequenas e puras, com uma casca fina que imprime.

## Dados de entrada

Crie `desafio/fila.py` e cole os dados no topo:

```python
PADROES_DA_LINHA = {
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
}

ESPECIFICACOES = {
    "OP-6101": {
        "titulo": "Filme PE 50 µm alta selagem",
        "regras": {"espessura": {"nominal": 50.0, "tol_pct": 5.0}},
    },
    "OP-6104": {
        "titulo": "Filme BOPP 20 µm baixo atrito",
        "regras": {"cof": {"min": 0.10, "max": 0.25}},
    },
}

PEDIDOS = [
    {"op": "OP-6101", "nf": "000501", "peso_kg": 1250.5},
    {"op": " op-6102", "nf": "000502", "peso_kg": 830.0},
    {"op": "OP-6103", "nf": "000503", "peso_kg": 640.2},
    {"op": "OP-6104", "nf": "000504", "peso_kg": 910.0},
    {"op": "OP-61", "nf": "5O5", "peso_kg": 0},
    {"op": "OP-6106", "nf": "000506", "peso_kg": 300.0},
    {"op": "OP-6107", "nf": "000507", "peso_kg": 455.5},
]

RESULTADOS = {
    "OP-6101": {
        "linha": "A",
        "obs": "",
        "medidas": {"espessura": 51.2, "gramatura": 46.3, "cof": 0.22},
    },
    "OP-6102": {
        "linha": "A",
        "obs": "COF: liberado",
        "medidas": {"espessura": 49.1, "gramatura": 45.8, "cof": 0.33},
    },
    "OP-6103": {
        "linha": "B",
        "obs": "",
        "medidas": {"espessura": 22.4, "gramatura": 18.9, "cof": 0.31},
    },
    "OP-6104": {
        "linha": "B",
        "obs": "",
        "medidas": {"espessura": 20.3, "gramatura": 18.2, "cof": 0.18},
    },
    "OP-6107": {"linha": "A", "obs": "", "medidas": {"espessura": 50.6, "cof": 0.19}},
}
```

## Regras de negócio

1. **Pedido inválido** (não vai adiante): OP limpa (strip + upper) precisa ser `"OP-"` + 4 a 6 dígitos; NF limpa precisa ser só dígitos; peso precisa existir e ser maior que zero. Mostre **todos** os problemas do pedido, não só o primeiro.
2. **Aguardando**: pedido válido cuja OP não tem resultado no laboratório.
3. **Regras da OP**: `padrão da linha | regras da especificação` (a especificação vence nas propriedades que define). O título é o da especificação ou "Padrão da linha X".
4. **Conferência**: `nominal ± tol_pct %` (limites com 2 casas) ou faixa `min`–`max`, limites inclusive. Propriedade sem medição conta como falha.
5. **Parecer**: sem falhas → `APROVADO`; a única falha é o COF e a observação contém "cof: liberado" (sem diferenciar maiúsculas) → `APROVADO COM RESSALVA (COF: liberado)`; senão → `REPROVADO` (o pedido fica **bloqueado**).
6. **Certificado** (só para aprovados): OP, NF, peso, título da especificação, cada propriedade com resultado e faixa, e o parecer.

## Requisitos obrigatórios

- [ ] Pelo menos **6 funções** no núcleo, cada uma com uma tarefa, docstring e no máximo ~20 linhas.
- [ ] **Nenhuma função do núcleo usa `print`** nem altera os dados recebidos. Só a `main` imprime.
- [ ] Nenhuma variável global é alterada (constantes em MAIÚSCULAS só são lidas).
- [ ] Nenhum valor padrão mutável.
- [ ] A função que decide o destino de **um** pedido devolve um dicionário (por exemplo `{"op": ..., "destino": "emitir", ...}`), e outra função monta a fila aplicando-a a todos.
- [ ] Ao menos **5 `assert`** no fim do arquivo testando funções do núcleo isoladamente.
- [ ] A saída mostra os certificados, as pendências com o motivo e uma linha de resumo com a contagem por destino e o peso total a emitir.

## Extras opcionais

- Use um **dicionário de funções** para os tipos de regra (`"nominal"`, `"faixa"`) em vez de `if "nominal" in regra` (seção 8 da aula).
- Mostre o peso no formato brasileiro (`1.250,5 kg`).
- Acrescente um tipo de regra "só mínimo" para tração (`{"min": 25.0}`) e uma OP que o use.
- Ordene as pendências por destino e, dentro de cada destino, por OP.
- Escreva `compor(*funcoes)` (exercício 13) e monte a limpeza da OP com ele.

## Exemplo de execução

```text
python desafio\fila.py
```

(No Linux/macOS: `python3 desafio/fila.py`.) Saída esperada para os dados acima:

```text
=== CERTIFICADOS A EMITIR ===

CERTIFICADO DE QUALIDADE - OP-6101
  NF 000501  |  1250.5 kg  |  Filme PE 50 µm alta selagem
  espessura  51.2 µm     47.5 a 52.5
  gramatura  46.3 g/m²   43.7 a 48.3
  cof        0.22        0.15 a 0.30
  Parecer: APROVADO

CERTIFICADO DE QUALIDADE - OP-6102
  NF 000502  |  830.0 kg  |  Padrão da linha A
  espessura  49.1 µm     45.0 a 55.0
  gramatura  45.8 g/m²   43.7 a 48.3
  cof        0.33        0.15 a 0.30
  Parecer: APROVADO COM RESSALVA (COF: liberado)

CERTIFICADO DE QUALIDADE - OP-6104
  NF 000504  |  910.0 kg  |  Filme BOPP 20 µm baixo atrito
  espessura  20.3 µm     18.4 a 21.6
  gramatura  18.2 g/m²   17.6 a 19.4
  cof        0.18        0.10 a 0.25
  Parecer: APROVADO

=== PENDÊNCIAS ===
  OP-6103   bloqueado   fora da especificação: espessura
  OP-61     inválido    OP inválida 'OP-61'; NF inválida '5O5'; peso deve ser maior que zero
  OP-6106   aguardando  sem resultado do laboratório
  OP-6107   bloqueado   fora da especificação: gramatura (sem medição)

Fila: 3 emitir, 2 bloqueado, 1 aguardando, 1 inválido | peso a emitir: 2990.5 kg
```

O layout pode variar; os destinos, os motivos e os números não.

## Critérios de aceite

- [ ] Roda sem erro e sem interação.
- [ ] Emite exatamente `OP-6101`, `OP-6102` (com ressalva) e `OP-6104`, com peso total 2990.5 kg.
- [ ] `OP-6104` usa a faixa de COF **da especificação** (0.10 a 0.25), e não a da linha B (0.20 a 0.40): por isso o COF 0.18 passa.
- [ ] `OP-6101` usa a espessura da especificação (47.5 a 52.5), mas a gramatura e o COF **do padrão** da linha A.
- [ ] O pedido `OP-61` aparece como inválido com os **três** problemas.
- [ ] `OP-6107` fica bloqueada por falta de medição de gramatura (e não quebra o programa).
- [ ] Os `assert` do fim do arquivo passam.
- [ ] `ruff check desafio` não aponta nada.

## Dicas de como começar

1. **Não comece pela `main`.** Escreva o problema numa frase e desenhe a árvore de funções (seção 11 da aula). Uma sugestão:

   ```text
   montar_fila
   +-- processar_pedido
       +-- problemas_do_pedido
       +-- regras_da_op
       +-- falhas_das_medidas
       |   +-- faixa
       +-- parecer
       +-- montar_certificado
   ```

2. Implemente **de baixo para cima**: `faixa` primeiro, testada com `assert faixa({"nominal": 46.0, "tol_pct": 5.0}) == (43.7, 48.3)`.
3. `regras_da_op` é uma linha com o operador `|` de dicionários (módulo 03). Teste com uma OP com especificação e uma sem.
4. `processar_pedido` usa **retorno antecipado**: inválido? devolve. Sem resultado? devolve. Reprovado? devolve. O caminho feliz (emitir) fica no fim.
5. Só depois escreva a `main`, que percorre a fila e imprime.

Travou? A solução de referência está em [solucao_referencia.py](solucao_referencia.py). Tente por pelo menos 40 minutos antes de abrir. Depois, compare as árvores de funções: a sua e a de referência não precisam ser iguais, mas ambas devem ser fáceis de testar.
