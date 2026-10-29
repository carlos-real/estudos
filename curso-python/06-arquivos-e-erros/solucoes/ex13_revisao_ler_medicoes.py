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

import csv
import unicodedata
from pathlib import Path

OBRIGATORIAS = {"lote", "linha", "espessura", "gramatura"}
LINHAS_VALIDAS = {"A", "B", "C", "D"}


class ArquivoInvalido(Exception):
    """O arquivo existe, mas não está no formato esperado."""


def ler_texto(caminho: Path) -> str:
    """Lê como UTF-8 (com ou sem BOM); se não for, como cp1252."""
    try:
        return caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="cp1252")


def normalizar_coluna(nome: str) -> str:
    """'  Observação ' -> 'observacao' (módulo 05: sem acento e minúsculo)."""
    decomposto = unicodedata.normalize("NFD", nome.strip().lower())
    return "".join([c for c in decomposto if not unicodedata.combining(c)])


def numero_br(texto: str) -> float:
    return float(texto.replace(".", "").replace(",", "."))


def ler_medicoes(caminho: Path) -> list[dict]:
    """Lê e valida o CSV de medições; levanta ArquivoInvalido se algo estiver errado."""
    linhas_csv = list(csv.reader(ler_texto(caminho).splitlines(), delimiter=";"))
    if not linhas_csv:
        raise ArquivoInvalido("arquivo vazio")

    cabecalho = [normalizar_coluna(nome) for nome in linhas_csv[0]]
    faltando = OBRIGATORIAS - set(cabecalho)  # diferença de conjuntos (módulo 03)
    if faltando:
        raise ArquivoInvalido(f"colunas ausentes: {', '.join(sorted(faltando))}")

    medicoes = []
    # start=2: o cabeçalho é a linha 1 do arquivo; os dados começam na 2.
    for numero, valores in enumerate(linhas_csv[1:], start=2):
        if not any(v.strip() for v in valores):
            continue  # linha vazia ou ";;;;"
        # strict=False: uma linha com MENOS células que o cabeçalho (o Excel às
        # vezes corta as vazias do fim) não quebra o zip; as que faltam viram "".
        registro = dict(zip(cabecalho, [v.strip() for v in valores], strict=False))
        for coluna in OBRIGATORIAS:
            registro.setdefault(coluna, "")

        linha = registro["linha"].upper()
        if linha not in LINHAS_VALIDAS:
            raise ArquivoInvalido(
                f"linha {numero}: linha de produção inválida: {registro['linha']!r}"
            )
        medicao = {"lote": registro["lote"], "linha": linha}
        for coluna in ("espessura", "gramatura"):
            try:
                medicao[coluna] = numero_br(registro[coluna])
            except ValueError as erro:
                raise ArquivoInvalido(
                    f"linha {numero}: valor inválido em {coluna}: {registro[coluna]!r}"
                ) from erro
        medicoes.append(medicao)
    return medicoes

    # Observação: splitlines() quebraria um campo entre aspas com quebra de
    # linha dentro. Nas planilhas de medição isso não acontece; se acontecesse,
    # o caminho seria abrir o arquivo com open(..., newline="") e o csv.reader.
