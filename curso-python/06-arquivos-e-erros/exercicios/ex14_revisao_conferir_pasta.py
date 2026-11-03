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

# Este exercício usa o módulo csv.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import csv
from pathlib import Path


def conferir_pasta(pasta: Path, minimo: float, maximo: float, saida: Path) -> dict:
    """Confere todos os CSVs da pasta e grava um CSV de resultado único."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
