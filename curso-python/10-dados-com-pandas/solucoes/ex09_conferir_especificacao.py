"""
Exercício 10.09 — Conferir medições contra a especificação (SOLUÇÃO)

Plano em quatro passos (escreva o plano antes do código!):
1. Juntar cada medição com a especificação do seu produto (merge LEFT: nenhuma
   medição pode sumir, mesmo sem especificação).
2. Calcular mínimo e máximo, de uma vez, para todas as linhas.
3. Decidir o status: padrão + exceções, com .loc.
4. Tirar as colunas auxiliares e devolver.
"""

import pandas as pd


def conferir_espessura(medicoes: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    """Junta medições e especificações e classifica cada bobina."""
    # 1. how="left": todas as medições ficam, na ordem original.
    #    validate="many_to_one": várias medições por produto, mas no máximo UMA
    #    especificação por produto. Se houver duplicata, o pandas levanta
    #    MergeError, que é um tipo de ValueError.
    df = medicoes.merge(
        specs[["produto", "nominal_um", "tolerancia_pct"]],
        on="produto",
        how="left",
        validate="many_to_one",
    )

    # 2. Produto sem especificação tem nominal NaN, e conta com NaN dá NaN:
    #    minimo e maximo ficam ausentes "de graça".
    folga = df["nominal_um"] * df["tolerancia_pct"] / 100
    df["minimo"] = (df["nominal_um"] - folga).round(2)
    df["maximo"] = (df["nominal_um"] + folga).round(2)

    # 3. Ordem das regras: da mais geral para a mais específica (a última vence).
    dentro = df["espessura_um"].between(df["minimo"], df["maximo"])
    df["status"] = "REPROVADA"
    df.loc[dentro, "status"] = "APROVADA"
    # between com NaN dá False, então "sem especificação" cairia em REPROVADA.
    # Por isso esta regra vem por último: nunca reprove (nem aprove) sem regra.
    df.loc[df["nominal_um"].isna(), "status"] = "SEM ESPECIFICAÇÃO"

    # 4. merge já devolve índice 0, 1, 2...; só tiramos as colunas auxiliares.
    return df.drop(columns=["nominal_um", "tolerancia_pct"])
