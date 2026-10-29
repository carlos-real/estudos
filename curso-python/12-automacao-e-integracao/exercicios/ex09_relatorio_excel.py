"""
Exercício 12.09 — Relatório Excel de medições, pronto para o gerente
Nível: ★★★

Contexto: todo fim de turno alguém copia as medições para uma planilha, pinta
os reprovados de vermelho e manda por e-mail. Vamos automatizar a planilha.

Cada medição chega como dicionário:
    {"op": "123456", "linha": "A", "ensaio": "Espessura",
     "valor": 20.4, "minimo": 18.0, "maximo": 22.0}

Tarefa: implemente gerar_relatorio(medicoes, caminho) com openpyxl.
1. Uma planilha (aba) chamada "Medições".
2. Linha 1 = cabeçalho:
   ["OP", "Linha", "Ensaio", "Valor", "Mínimo", "Máximo", "Status"]
   em negrito, fonte branca ("FFFFFF") e fundo sólido azul "1F4E78".
3. Uma linha por medição, na ordem recebida. Status = "APROVADO" se
   minimo <= valor <= maximo, senão "REPROVADO".
4. Colunas D, E e F (Valor, Mínimo, Máximo) das linhas de dados com
   number_format "0.00".
5. Largura de cada coluna = maior texto da coluna (cabeçalho incluído) + 2.
6. Cabeçalho congelado (freeze_panes = "A2") e filtro ligado em toda a
   tabela (auto_filter.ref = "A1:G<última linha>").
7. Formatação condicional na coluna Status (G2:G<última linha>): regra
   CellIsRule com operator="equal" e formula=['"REPROVADO"'], fonte
   "9C0006" e fundo "FFC7CE". Se não houver medições, pule este item.
8. Crie a pasta de `caminho` se ela não existir, salve e devolva `caminho`.

Exemplos:
    >>> gerar_relatorio(medicoes, Path("saida/turno.xlsx"))
    PosixPath('saida/turno.xlsx')         # no Windows: WindowsPath(...)

Dica: siga o exemplo 05 da aula, mas escreva com as suas palavras.
Imports úteis: Workbook (openpyxl), Font, PatternFill (openpyxl.styles),
CellIsRule (openpyxl.formatting.rule), get_column_letter (openpyxl.utils).

Teste com:  python curso.py testar 12 ex09
"""

from pathlib import Path

CABECALHO = ["OP", "Linha", "Ensaio", "Valor", "Mínimo", "Máximo", "Status"]


def gerar_relatorio(medicoes: list[dict], caminho: Path) -> Path:
    """Gera o relatório .xlsx das medições e devolve o caminho do arquivo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
