"""
Exercício 09.08 — Ler o arquivo de medições (TDD com tmp_path)
Nível: ★★☆

Contexto: o micrômetro do laboratório exporta um arquivo de texto com uma
medição por linha. O técnico às vezes deixa linhas em branco e comentários
(linhas que começam com #). Quando uma linha está ilegível, o programa precisa
dizer QUAL linha é, para alguém conferir no equipamento.

Tarefa: implemente ler_medicoes(caminho), que lê o arquivo (UTF-8) e devolve a
lista de valores (float), na ordem.
  - Aceita vírgula ou ponto decimal: "25,4" e "25.4" viram 25.4.
  - Remove espaços e tabulações em volta de cada linha.
  - Ignora linhas vazias (ou só com espaços) e linhas que começam com "#".
  - Linha que não é número: levante ValueError com a mensagem
        "linha <n>: valor inválido '<texto>'"
    em que <n> é o número da linha no arquivo, começando em 1 (contando
    também as linhas vazias e os comentários) e <texto> é a linha sem os
    espaços em volta.
  - Arquivo inexistente: deixe o FileNotFoundError acontecer (não trate).

Faça com TDD: rode só este teste parando na primeira falha, faça passar,
rode de novo (seção 13 da aula). Na pasta curso-python:
    python -m pytest 09-testes-e-qualidade/testes/test_m09_ex08_ler_medicoes.py -x

Exemplo (arquivo com as linhas "# OP 123", "25,4", "", "25.1"):
    >>> ler_medicoes(Path("medicoes.txt"))
    [25.4, 25.1]

Dica: enumerate(linhas, start=1) dá o número de cada linha. Para gerar o
ValueError com a sua mensagem, use try/except ValueError ao redor do float()
e levante um novo ValueError (módulo 06).

Teste com:  python curso.py testar 09 ex08
"""

from pathlib import Path


def ler_medicoes(caminho: Path) -> list[float]:
    """Lê o arquivo de medições e devolve os valores como floats."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
