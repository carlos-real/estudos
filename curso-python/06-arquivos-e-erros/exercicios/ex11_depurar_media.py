"""
Exercício 06.11 — Depure a média que mente
Nível: ★★☆

Contexto: Esta função calcula a média das espessuras gravadas num .txt (um
valor por linha). Ela "nunca dá erro"... e por isso ninguém percebeu que ela
devolve 0 em situações bem diferentes.

    def media_do_arquivo_original(caminho):
        try:
            arquivo = open(caminho)
            valores = [float(linha) for linha in arquivo]
            return sum(valores) / len(valores)
        except:
            return 0

Tarefa, parte 1 (LEIA antes de rodar!): preveja o que a função original
devolve em cada caso e complete `previsoes()`, que devolve uma tupla com 4
respostas (números):
  a) arquivo com as linhas "25.0" e "27.0";
  b) arquivo com as linhas "25,4" e "26,0" (vírgula decimal);
  c) arquivo vazio;
  d) arquivo que não existe.
Depois copie a função para um script, rode os 4 casos e confira.

Tarefa, parte 2: escreva `media_do_arquivo(caminho)`, a versão corrigida:
- abra com `with` e encoding UTF-8;
- ignore as linhas em branco;
- aceite números no formato brasileiro ("25,4", "1.250,5"), com a conversão
  do módulo 05;
- valor inválido: levante ValueError(f"linha {n}: valor inválido {texto!r}"),
  em que n é o número da linha no arquivo (a primeira é 1) e texto é o
  conteúdo da linha sem espaços nas pontas; encadeie com `from erro`;
- arquivo sem nenhum valor: levante ValueError("arquivo sem valores");
- arquivo inexistente: NÃO trate; deixe o FileNotFoundError aparecer.

Exemplos (arquivo com "25,4", "", "26,0"):
    >>> media_do_arquivo(Path("espessuras.txt"))
    25.7

Dica: os defeitos da original são: except "pega-tudo", arquivo nunca fechado,
sem encoding, sem tratar linha em branco nem vírgula decimal, e o mesmo 0 para
problemas diferentes. Use `enumerate(arquivo, start=1)` para numerar as linhas.

Teste com:  python curso.py testar 06 ex11
"""

from pathlib import Path


def previsoes() -> tuple:
    """Devolve (a, b, c, d): o que a função original devolve em cada caso."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def media_do_arquivo(caminho: Path) -> float:
    """Média dos valores do arquivo (um por linha, formato brasileiro)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
