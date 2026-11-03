"""
Exercício 10.05 — Todas as abas numa tabela só
Nível: ★★☆

Contexto: a planilha de valores do laboratório tem uma aba por linha de produção
("Linha A", "Linha B", ...). Às vezes alguém acrescenta outras abas, como
"Instruções". Cada aba de linha tem um TÍTULO na primeira linha da planilha e o
cabeçalho só na segunda:

    linha 1:  Controle de qualidade — Linha A
    linha 2:  OP | Bobina | Espessura (µm)
    linha 3:  024412 | 024412-01 | 38.1
    ...

Tarefa: implemente ler_todas_as_abas(caminho), que devolve UMA tabela com:
  - só as abas cujo nome começa com "Linha " (as outras são ignoradas);
  - as colunas, nesta ordem: "linha", "op", "bobina", "espessura_um";
  - "linha" = a letra do nome da aba ("Linha C" -> "C");
  - "op" como texto (preserve zeros à esquerda: "024412");
  - as linhas na ordem das abas e, dentro da aba, na ordem da planilha;
  - índice 0, 1, 2, ...
Se nenhuma aba começar com "Linha ", levante ValueError.

Exemplo:
    >>> ler_todas_as_abas("planilha.xlsx")
      linha      op     bobina  espessura_um
    0     A  024412  024412-01          38.1
    1     A  024412  024412-02          36.4
    2     B  024413  024413-01          32.9

Dica: pd.ExcelFile(caminho).sheet_names dá a lista de nomes das abas.
pd.read_excel(caminho, sheet_name=[nomes], header=1, dtype={"OP": str})
devolve um dicionário {nome da aba: DataFrame}. Cuidado: header=1 numa aba de
uma linha só (como "Instruções") dá erro; escolha as abas ANTES de ler.
Junte as partes com pd.concat.

Teste com:  python curso.py testar 10 ex05
"""

from pathlib import Path

import pandas as pd


def ler_todas_as_abas(caminho: str | Path) -> pd.DataFrame:
    """Junta as abas 'Linha X' numa tabela com a coluna 'linha'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
