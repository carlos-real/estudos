"""
Exercício 10.14 — Revisão: relatório Excel formatado a partir de objetos
Nível: ★★★

Revisão intercalada: dataclasses (módulo 08), pathlib e exceções (módulo 06) e
exportação para Excel com formatação (este módulo).

Contexto: o seu sistema de conferência produz uma lista de objetos Resultado
(a dataclass abaixo, já pronta). O gerente quer receber isso numa planilha
"apresentável": cabeçalho destacado, colunas largas o bastante, cabeçalho
congelado e as bobinas reprovadas pintadas de vermelho claro.

Tarefa: implemente duas funções.
  1. resultados_para_dataframe(resultados): devolve um DataFrame com uma linha
     por objeto e as colunas na ordem dos campos da dataclass ("op", "bobina",
     "espessura_um", "status"). Lista vazia -> DataFrame vazio com essas colunas.
  2. exportar_relatorio(resultados, caminho): grava um .xlsx com UMA aba chamada
     "Resultados" (sem a coluna de índice do pandas) e:
       - cabeçalho (linha 1) em negrito;
       - painel congelado abaixo do cabeçalho (freeze_panes = "A2");
       - largura de cada coluna >= tamanho do texto do cabeçalho + 2;
       - linhas com status "REPROVADA": TODAS as células da linha com
         preenchimento sólido na cor "FFC7CE"; as outras linhas sem preenchimento.
     Crie as pastas do caminho se não existirem. Lista vazia -> ValueError
     (não faz sentido mandar relatório vazio). Devolva o caminho como Path.

Exemplo:
    >>> r = [Resultado("024447", "024447-03", 67.5, "REPROVADA"),
    ...      Resultado("024447", "024447-04", 62.0, "APROVADA")]
    >>> exportar_relatorio(r, Path("saida/relatorio.xlsx"))
    PosixPath('saida/relatorio.xlsx')      (no Windows aparece WindowsPath)

Dica: dataclasses.asdict e dataclasses.fields; pd.ExcelWriter(caminho,
engine="openpyxl") e, dentro do with, escritor.sheets["Resultados"] dá a aba
do openpyxl; Font(bold=True), PatternFill("solid", fgColor="FFC7CE"),
aba.column_dimensions["A"].width, get_column_letter(1) == "A".

Teste com:  python curso.py testar 10 ex14
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Resultado:
    """Resultado da conferência de uma bobina (já pronto, não precisa mexer)."""

    op: str
    bobina: str
    espessura_um: float
    status: str


def resultados_para_dataframe(resultados: list[Resultado]) -> pd.DataFrame:
    """Lista de Resultado -> DataFrame com as colunas na ordem dos campos."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def exportar_relatorio(resultados: list[Resultado], caminho: str | Path) -> Path:
    """Grava o relatório formatado e devolve o caminho do arquivo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
