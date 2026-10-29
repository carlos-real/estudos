"""
Exercício 06.14 — Revisão: conferir uma pasta inteira sem parar no erro
Nível: ★★★

Contexto: Toda manhã, a pasta de laudos tem um CSV por linha de produção. O
robô confere a espessura de todos os lotes e gera um único CSV de resultado
para o Excel. Se UM arquivo estiver com problema, os outros continuam sendo
processados, e o arquivo com problema é listado para alguém corrigir.

Este exercício mistura arquivos e exceções (módulo 06) com números brasileiros
(módulo 05), decomposição em funções (módulo 04), dicionários e contadores
(módulo 03) e decisões (módulo 02).

Tarefa: implemente `conferir_pasta(pasta, minimo, maximo, saida)`:
- processe cada arquivo *.csv da pasta (extensão em minúsculas), em ordem
  alfabética do nome; outros arquivos são ignorados;
- cada CSV tem as colunas "lote" e "espessura", separador ";", número
  brasileiro e encoding UTF-8 (com ou sem BOM: use "utf-8-sig");
- cada lote é "APROVADO" se minimo <= espessura <= maximo, senão "REPROVADO";
- grave `saida` como CSV do Excel brasileiro (";", "utf-8-sig", newline="")
  com o cabeçalho arquivo;lote;espessura;status e a espessura com vírgula e
  2 casas ("25,40");
- arquivo com problema (falta a coluna lote ou espessura, número inválido ou
  arquivo que não é UTF-8) é PULADO INTEIRO: nenhuma linha dele vai para a
  saída, mesmo as que estavam certas. Guarde {nome_do_arquivo: str(erro)} e
  siga para o próximo;
- devolva {"aprovados": N, "reprovados": N, "com_erro": {nome: mensagem}}.

Exemplos:
    >>> conferir_pasta(Path("laudos"), 22.5, 27.5, Path("resultado.csv"))
    {'aprovados': 3, 'reprovados': 1, 'com_erro': {'linha_C.csv': ...}}

Dica: escreva uma função que lê UM arquivo inteiro e devolve a lista de linhas
de resultado (ou levanta erro). Só depois que ela devolveu, junte as linhas à
lista geral: assim um arquivo com erro na 3ª linha não deixa as 2 primeiras
pela metade na saída. Erros a capturar: KeyError, ValueError (e lembre que
UnicodeDecodeError é um tipo de ValueError).

Teste com:  python curso.py testar 06 ex14
"""

import csv
from pathlib import Path


def numero_br(texto: str) -> float:
    return float(texto.strip().replace(".", "").replace(",", "."))


def conferir_arquivo(caminho: Path, minimo: float, maximo: float) -> list[dict]:
    """Lê UM arquivo e devolve as linhas de resultado. Pode levantar erro."""
    resultado = []
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            espessura = numero_br(linha["espessura"])  # KeyError ou ValueError
            status = "APROVADO" if minimo <= espessura <= maximo else "REPROVADO"
            resultado.append(
                {
                    "arquivo": caminho.name,
                    "lote": linha["lote"].strip(),
                    "espessura": f"{espessura:.2f}".replace(".", ","),
                    "status": status,
                }
            )
    return resultado


def conferir_pasta(pasta: Path, minimo: float, maximo: float, saida: Path) -> dict:
    """Confere todos os CSVs da pasta e grava um CSV de resultado único."""
    todas = []
    com_erro = {}
    arquivos = sorted(p for p in pasta.iterdir() if p.is_file() and p.suffix == ".csv")
    for caminho in arquivos:
        try:
            linhas = conferir_arquivo(caminho, minimo, maximo)
        except (KeyError, ValueError) as erro:
            # O arquivo inteiro fica de fora; registramos e seguimos em frente.
            # KeyError: falta coluna. ValueError: número inválido. E o
            # UnicodeDecodeError, que é filho de ValueError, vem junto.
            com_erro[caminho.name] = str(erro)
            continue
        todas.extend(linhas)  # só chega aqui se o arquivo inteiro deu certo

    with open(saida, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=["arquivo", "lote", "espessura", "status"], delimiter=";"
        )
        escritor.writeheader()
        escritor.writerows(todas)

    aprovados = sum(1 for linha in todas if linha["status"] == "APROVADO")
    return {
        "aprovados": aprovados,
        "reprovados": len(todas) - aprovados,
        "com_erro": com_erro,
    }
