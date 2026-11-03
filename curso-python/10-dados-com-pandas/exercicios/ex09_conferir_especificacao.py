"""
Exercício 10.09 — Conferir medições contra a especificação (merge)
Nível: ★★★

Contexto: as medições dizem o produto de cada bobina; a tabela de
especificações diz o nominal e a tolerância (%) de cada produto. Conferir uma
contra a outra é um PROCV no Excel. No pandas, é um merge.

Tarefa: implemente conferir_espessura(medicoes, specs).
  medicoes: colunas "bobina", "produto", "espessura_um" (pode ter outras).
  specs:    colunas "produto", "nominal_um", "tolerancia_pct".
Devolva uma tabela NOVA com todas as colunas de medicoes, na mesma ordem de
linhas, índice 0, 1, 2..., mais três colunas no fim:
  - "minimo" = nominal_um - nominal_um * tolerancia_pct / 100 (2 casas)
  - "maximo" = nominal_um + nominal_um * tolerancia_pct / 100 (2 casas)
  - "status":
      "SEM ESPECIFICAÇÃO" se o produto não existe em specs (minimo e maximo
                          ficam ausentes, NaN);
      "APROVADA"  se minimo <= espessura_um <= maximo;
      "REPROVADA" nos outros casos.
As colunas "nominal_um" e "tolerancia_pct" NÃO devem aparecer no resultado.
Se specs tiver o mesmo produto em duas linhas, levante ValueError (a regra
ficaria ambígua).

Exemplo:
    >>> conferir_espessura(medicoes, specs)
      bobina produto  espessura_um  minimo  maximo             status
    0     01  LAM-62          67.5   57.66   66.34          REPROVADA
    1     02   PE-40          38.1   36.00   44.00           APROVADA
    2     03   PE-90          94.4     NaN     NaN  SEM ESPECIFICAÇÃO

Dica: merge(..., how="left", validate="many_to_one") mantém todas as medições e
reclama (com um erro que é ValueError) se a especificação estiver duplicada.

Teste com:  python curso.py testar 10 ex09
"""

import pandas as pd


def conferir_espessura(medicoes: pd.DataFrame, specs: pd.DataFrame) -> pd.DataFrame:
    """Junta medições e especificações e classifica cada bobina."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
