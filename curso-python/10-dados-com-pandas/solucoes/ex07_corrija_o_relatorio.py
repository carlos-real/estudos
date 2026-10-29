"""
Exercício 10.07 — Corrija o relatório (SOLUÇÃO)

Os quatro defeitos do código original:

1. df[df["cof"] > cof_max]["status"] = "ALTO" é ATRIBUIÇÃO ENCADEADA: o
   primeiro [...] devolve uma tabela que se comporta como CÓPIA, e o valor é
   gravado nessa cópia, que é jogada fora. No pandas 3 isso nunca funciona (aviso
   ChainedAssignmentError); no 2.2 também não funciona aqui (SettingWithCopyWarning).
   Correção: uma operação só, com .loc[mascara, "coluna"] = valor.

2. contagem / total: linhas sem nenhuma bobina alta NÃO aparecem em 'contagem'.
   Na divisão, o pandas alinha pelos índices e o que falta de um lado vira NaN.

3. sort_values() é crescente por padrão: as melhores linhas vinham primeiro.

4. df["status"] = "OK" cria uma coluna no DataFrame de quem chamou a função
   (efeito colateral, módulo 04).

A versão abaixo resolve os quatro de uma vez: não cria coluna nenhuma (nada de
efeito colateral nem de atribuição encadeada) e usa a média de uma máscara
booleana, que já dá 0.0 para quem não tem True.
"""

import pandas as pd


def percentual_cof_alto(df: pd.DataFrame, cof_max: float) -> pd.Series:
    """% de bobinas com COF acima do máximo, por linha (piores primeiro)."""
    # Máscara True/False do tamanho da tabela. É uma Series NOVA: df não muda.
    alto = df["cof"] > cof_max

    # Agrupamos a máscara pela coluna "linha" do df. A média de True/False é a
    # proporção de True; linha sem nenhum True dá 0.0 (e não some, como antes).
    percentual = (alto.groupby(df["linha"]).mean() * 100).round(1)
    percentual.name = "pct_cof_alto"

    # groupby já devolve as linhas em ordem alfabética. Uma ordenação "estável"
    # (kind="stable") mantém essa ordem entre os empates.
    return percentual.sort_values(ascending=False, kind="stable")

    # Alternativa mais próxima do código original, corrigida:
    #   copia = df.copy()                                        # defeito 4
    #   copia["status"] = "OK"
    #   copia.loc[copia["cof"] > cof_max, "status"] = "ALTO"      # defeito 1
    #   contagem = copia[copia["status"] == "ALTO"].groupby("linha")["bobina"].count()
    #   total = copia.groupby("linha")["bobina"].count()
    #   contagem = contagem.reindex(total.index, fill_value=0)   # defeito 2
    #   ... e sort_values(ascending=False, kind="stable")         # defeito 3
