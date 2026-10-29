"""
Exercício 12.05 — Listar as planilhas de uma pasta
Nível: ★☆☆

Contexto: toda manhã o robô precisa processar as planilhas de resultados que o
pessoal salva na pasta de rede. Só que a pasta também tem PDFs, anotações,
subpastas e os famosos arquivos "~$Resultados.xlsx", que o Excel cria
enquanto a planilha está aberta (não são planilhas de verdade!).

Tarefa: implemente listar_planilhas(pasta).
- Devolva os NOMES (str) dos arquivos .xlsx e .xlsm que estão diretamente na
  pasta (não entre nas subpastas). A extensão vale em maiúsculas ou
  minúsculas (.XLSX também conta).
- Ignore arquivos cujo nome começa com "~$".
- Ignore pastas, mesmo que o nome termine em .xlsx.
- Devolva a lista em ordem alfabética, sem diferenciar maiúsculas de
  minúsculas (use key=str.lower no sorted).
- Se a pasta não existir, levante FileNotFoundError.

Exemplos (pasta com: Linha_B.xlsx, linha_a.xlsx, ~$linha_a.xlsx, laudo.pdf):
    >>> listar_planilhas(Path("resultados"))
    ['linha_a.xlsx', 'Linha_B.xlsx']

Dica: Path.iterdir(), .is_file(), .suffix e .name. Lembre de .lower().

Teste com:  python curso.py testar 12 ex05
"""

from pathlib import Path


def listar_planilhas(pasta: Path) -> list[str]:
    """Nomes das planilhas Excel da pasta, em ordem alfabética."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
