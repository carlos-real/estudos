"""
Exercício 12.06 — Nunca sobrescrever um arquivo
Nível: ★☆☆

Contexto: o robô salva o PDF de cada certificado numa pasta. Se já existir um
"certificado_123456.pdf" (de uma emissão anterior), gravar por cima apagaria
uma evidência. A saída é fazer como o Windows: "certificado_123456 (2).pdf".

Tarefa: implemente nome_disponivel(pasta, nome).
- Se pasta / nome não existe, devolva esse caminho.
- Se existe, tente "<nome sem extensão> (2)<extensão>", depois " (3)", e assim
  por diante, e devolva o primeiro caminho livre.
- A função NÃO cria nenhum arquivo: só escolhe o nome.

Exemplos (a pasta já tem relatorio.xlsx e relatorio (2).xlsx):
    >>> nome_disponivel(Path("saida"), "relatorio.xlsx")
    PosixPath('saida/relatorio (3).xlsx')      # no Windows: WindowsPath(...)
    >>> nome_disponivel(Path("saida"), "novo.xlsx")
    PosixPath('saida/novo.xlsx')

Dica: Path("certificado.pdf").stem é "certificado" e .suffix é ".pdf".

Teste com:  python curso.py testar 12 ex06
"""

from pathlib import Path


def nome_disponivel(pasta: Path, nome: str) -> Path:
    """Primeiro caminho livre para `nome` dentro de `pasta`."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
