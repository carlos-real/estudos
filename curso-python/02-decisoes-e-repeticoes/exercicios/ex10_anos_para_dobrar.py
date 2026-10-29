"""
Exercício 02.10 — Quanto tempo até a meta?
Nível: ★★☆

Contexto: Você decidiu guardar dinheiro para um notebook melhor e um curso de dados.
Perguntas do tipo "quantas vezes até chegar lá?" são o território do while: você não
sabe de antemão quantas repetições serão necessárias.

Tarefa:
1. `anos_para_dobrar(taxa_anual_pct)` devolve quantos anos inteiros um capital leva
   para dobrar (ficar maior ou igual ao dobro) com juros compostos de
   `taxa_anual_pct`% ao ano. A cada ano, o capital é multiplicado por
   (1 + taxa_anual_pct / 100).
   Se a taxa for menor ou igual a zero, o capital nunca dobra: devolva -1 (sem isso,
   seu while vira um loop infinito!).
2. `meses_para_meta(saldo_inicial, deposito_mensal, meta)` devolve quantos depósitos
   mensais são necessários para o saldo ficar maior ou igual à meta (sem juros).
   - Se o saldo inicial já atinge a meta, devolva 0.
   - Se o depósito for menor ou igual a zero (e a meta ainda não foi atingida),
     devolva -1.

Exemplos:
    >>> anos_para_dobrar(10)
    8
    >>> anos_para_dobrar(0)
    -1
    >>> meses_para_meta(0, 500, 3000)
    6
    >>> meses_para_meta(5000, 100, 3000)
    0

Dica: comece com capital = 1.0 (o valor inicial não importa para "dobrar") e conte
as voltas do while.

Teste com:  python curso.py testar 02 ex10
"""


def anos_para_dobrar(taxa_anual_pct: float) -> int:
    """Devolve os anos para o capital dobrar, ou -1 se a taxa for <= 0."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def meses_para_meta(saldo_inicial: float, deposito_mensal: float, meta: float) -> int:
    """Devolve quantos depósitos faltam para atingir a meta (0 ou -1 nos casos especiais)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
