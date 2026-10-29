"""
Exercício 06.03 — Ler um arquivo de texto
Nível: ★☆☆

Contexto: A lista de OPs a liberar fica num .txt, uma por linha. O pessoal
deixa linhas em branco e comentários começando com "#".

Tarefa: implemente `ler_linhas(caminho)`:
- abra o arquivo em UTF-8 usando `with`;
- devolva a lista das linhas sem espaços nas pontas (e sem a quebra de linha);
- ignore as linhas vazias e as que, depois do strip, começam com "#";
- se o arquivo não existir, deixe o FileNotFoundError acontecer.

Exemplos (arquivo com "# OPs de hoje", "OP 123456", "", "  OP 123457  "):
    >>> ler_linhas(Path("ops.txt"))
    ['OP 123456', 'OP 123457']

Dica: percorrer o arquivo com `for linha in arquivo` entrega uma linha por vez,
já com o "\\n" no fim.

Teste com:  python curso.py testar 06 ex03
"""

from pathlib import Path


def ler_linhas(caminho: Path) -> list[str]:
    """Lê as linhas úteis do arquivo (sem vazias e sem comentários)."""
    linhas = []
    # with fecha o arquivo sozinho, mesmo se acontecer um erro no meio.
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # tira espaços e o "\n" do fim
            if not linha or linha.startswith("#"):
                continue
            linhas.append(linha)
    return linhas

    # Alternativa com pathlib, lendo tudo de uma vez:
    #     texto = caminho.read_text(encoding="utf-8")
    #     return [l.strip() for l in texto.splitlines()
    #             if l.strip() and not l.strip().startswith("#")]
    # Para arquivos pequenos, as duas são equivalentes. O for linha a linha
    # gasta menos memória em arquivos enormes.
