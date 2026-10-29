"""
Exercício 10.07 — Corrija o relatório (leitura de código e depuração)
Nível: ★★☆

Contexto: um colega escreveu a função abaixo para dizer, por linha de produção,
qual porcentagem das bobinas teve COF acima do máximo. O relatório saiu com
números estranhos e o gerente desconfiou. Leia o código com atenção ANTES de
rodar qualquer coisa:

    def percentual_cof_alto(df, cof_max):
        df["status"] = "OK"
        df[df["cof"] > cof_max]["status"] = "ALTO"               # (1)
        altas = df[df["status"] == "ALTO"]
        contagem = altas.groupby("linha")["bobina"].count()
        total = df.groupby("linha")["bobina"].count()
        percentual = (contagem / total * 100).round(1)            # (2)
        return percentual.sort_values()                           # (3)

Este código tem QUATRO defeitos:
  - um que faz a coluna "status" nunca virar "ALTO";
  - um que deixa linhas sem nenhuma bobina alta com NaN em vez de 0.0;
  - um na ordenação (o gerente quer as piores linhas primeiro);
  - um efeito colateral: a função altera o DataFrame de quem chamou.

Tarefa: escreva a versão correta de percentual_cof_alto(df, cof_max), que
devolve uma Series:
  - índice = as linhas de produção (todas as que aparecem em df), nome "linha";
  - valores = % de bobinas com cof > cof_max (estritamente maior), 1 casa decimal;
    linha sem bobina alta -> 0.0;
  - nome da Series: "pct_cof_alto";
  - ordem: do maior percentual para o menor; empate -> ordem alfabética da linha;
  - sem alterar o df recebido.

Exemplo:
    >>> df
      linha bobina   cof
    0     A     a1  0.38
    1     A     a2  0.30
    2     B     b1  0.25
    >>> percentual_cof_alto(df, 0.35)
    linha
    A    50.0
    B     0.0
    Name: pct_cof_alto, dtype: float64

Dica: para cada defeito, escreva primeiro (num comentário) o que acontece e por
quê. Lembre que a média de uma coluna True/False é a proporção de True.

Teste com:  python curso.py testar 10 ex07
"""

import pandas as pd


def percentual_cof_alto(df: pd.DataFrame, cof_max: float) -> pd.Series:
    """% de bobinas com COF acima do máximo, por linha (piores primeiro)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
