"""
Exercício 06.13 — Revisão: leitura validada de medições
Nível: ★★★

Contexto: Este é o leitor "de verdade" da planilha de medições exportada em
CSV. O arquivo pode vir em UTF-8 (com ou sem BOM) ou cp1252, os nomes das
colunas vêm escritos de vários jeitos ("Lote", " LINHA ", "Espessura") e, de
vez em quando, alguém digita "2O,1" (com a letra O) no lugar de "20,1". O
programa precisa recusar o arquivo com uma mensagem que diga ONDE está o erro.

Este exercício mistura arquivos e exceções (módulo 06) com números brasileiros
e acentos (módulo 05), conjuntos e dicionários (módulo 03) e validação com
decisões (módulo 02).

A exceção `ArquivoInvalido` já está criada no arquivo.

Tarefa: implemente `ler_medicoes(caminho)`, que devolve uma lista de
dicionários {"lote": str, "linha": str, "espessura": float, "gramatura": float}.
- Encoding: tente UTF-8 com "utf-8-sig"; se der UnicodeDecodeError, use
  "cp1252".
- Separador ";". Use o módulo csv (há campos entre aspas com ";" dentro).
- Nomes de coluna: compare sem espaços nas pontas, em minúsculas e sem acento.
  Colunas a mais (como "Observação") são ignoradas.
- Arquivo sem nenhuma linha: ArquivoInvalido("arquivo vazio").
- Faltando colunas obrigatórias (lote, linha, espessura, gramatura):
  ArquivoInvalido(f"colunas ausentes: {nomes}"), com os nomes que faltam em
  ordem alfabética, separados por ", ".
- Linhas totalmente vazias (como ";;;;") são puladas.
- "linha" (de produção) precisa ser A, B, C ou D (aceite minúscula e espaços;
  devolva maiúscula). Senão:
  ArquivoInvalido(f"linha {n}: linha de produção inválida: {valor!r}").
- espessura e gramatura: número brasileiro. Se não converter:
  ArquivoInvalido(f"linha {n}: valor inválido em {coluna}: {valor!r}"),
  encadeado com `from erro`.
- n é o número da linha no ARQUIVO: o cabeçalho é a linha 1.
- Os valores de texto voltam sem espaços nas pontas.

Exemplos (arquivo com "Lote;Linha;Espessura;Gramatura" e "A-0153; a ;25,4;23,1"):
    >>> ler_medicoes(Path("medicoes.csv"))
    [{'lote': 'A-0153', 'linha': 'A', 'espessura': 25.4, 'gramatura': 23.1}]

Dica: leia o texto inteiro primeiro (com o fallback de encoding) e depois use
`csv.reader(texto.splitlines(), delimiter=";")`: o csv aceita qualquer lista
de linhas. Um conjunto resolve as colunas ausentes: obrigatorias - cabecalho.
Funções pequenas ajudam muito: ler_texto, normalizar_coluna, numero_br.

Teste com:  python curso.py testar 06 ex13
"""

# Este exercício usa os módulos csv e unicodedata.
# Apague o "# " do começo das linhas abaixo para importá-los:
# import csv
# import unicodedata
from pathlib import Path


class ArquivoInvalido(Exception):
    """O arquivo existe, mas não está no formato esperado."""


def ler_medicoes(caminho: Path) -> list[dict]:
    """Lê e valida o CSV de medições; levanta ArquivoInvalido se algo estiver errado."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
