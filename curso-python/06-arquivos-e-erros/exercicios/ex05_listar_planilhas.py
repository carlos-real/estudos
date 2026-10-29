"""
Exercício 06.05 — Listar as planilhas de uma pasta
Nível: ★☆☆

Contexto: Cada linha de produção salva seus laudos numa pasta compartilhada.
Lá dentro tem de tudo: CSV, Excel, PDF, subpastas e os arquivos temporários
que o Excel cria enquanto a planilha está aberta (começam com "~$").

Tarefa: implemente `listar_planilhas(pasta)`, que devolve a lista com os NOMES
(não os caminhos) dos arquivos da pasta que são planilhas:
- extensão .csv, .xlsx ou .xlsm, sem diferenciar maiúsculas ("LAUDO.CSV" vale);
- só arquivos (uma subpasta chamada "antigos.csv" não conta);
- ignore os temporários do Excel (nome começando com "~$");
- não entre nas subpastas;
- devolva em ordem alfabética (sorted);
- se a pasta não existir, levante FileNotFoundError com a mensagem
  f"Pasta não encontrada: {pasta}".

Exemplos (pasta com linha_A.csv, linha_B.XLSX, ~$linha_B.xlsx, foto.pdf):
    >>> listar_planilhas(Path("laudos"))
    ['linha_A.csv', 'linha_B.XLSX']

Dica: `pasta.iterdir()` percorre o conteúdo da pasta; cada item é um Path com
`.name`, `.suffix` e `.is_file()`.

Teste com:  python curso.py testar 06 ex05
"""

from pathlib import Path


def listar_planilhas(pasta: Path) -> list[str]:
    """Nomes das planilhas da pasta, em ordem alfabética."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
