"""
Exercício 09.08 — Ler o arquivo de medições (TDD com tmp_path)
Nível: ★★☆

Solução comentada. Veja o enunciado completo em exercicios/ex08_ler_medicoes.py.
"""

from pathlib import Path


def ler_medicoes(caminho: Path) -> list[float]:
    """Lê o arquivo de medições e devolve os valores como floats."""
    # read_text já abre, lê e fecha o arquivo. Se ele não existir, o próprio
    # read_text levanta FileNotFoundError, exatamente como a regra pede.
    linhas = caminho.read_text(encoding="utf-8").splitlines()

    valores = []
    # start=1 porque, para pessoas, a primeira linha é a linha 1.
    for numero, linha in enumerate(linhas, start=1):
        texto = linha.strip()
        if not texto or texto.startswith("#"):
            continue  # linha vazia ou comentário: pula
        try:
            valores.append(float(texto.replace(",", ".")))
        except ValueError:
            # "from None" esconde o erro original do float() no traceback:
            # a nossa mensagem já diz tudo o que importa.
            raise ValueError(f"linha {numero}: valor inválido {texto!r}") from None
    return valores


# Como os testes foram escritos com TDD, a função cresceu em passos:
#   1) ler valores com ponto;  2) aceitar vírgula;  3) pular vazias;
#   4) pular comentários;      5) mensagem de erro com o número da linha.
# Em cada passo, um teste novo ficava vermelho e o código mínimo o deixava verde.
