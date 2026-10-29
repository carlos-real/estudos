"""
Exercício 07.13 — Revisão: do CSV do laboratório ao JSON da expedição
Nível: ★★★

Revisão de: módulo 06 (csv com ";", json, pathlib, tratar ValueError), módulo 05
(números no formato brasileiro) e módulo 03 (dicionários aninhados), junto com
defaultdict e datetime deste módulo.

Contexto: A expedição quer um arquivo JSON dizendo, para cada OP, se ela está
aprovada (todos os ensaios aprovados) ou reprovada, e quais ensaios reprovaram.
A planilha exportada pelo laboratório às vezes vem com linhas estragadas.

O CSV (UTF-8, separador ";") tem as colunas:
    data;op;linha;ensaio;valor;resultado
    01/10/2026;OP245101;A;espessura;20,4;aprovado

Tarefa:
1. `ler_ensaios_csv(caminho)` devolve uma tupla (registros, ignoradas):
   - registros: lista de dicionários com "data" (date), "op", "linha", "ensaio",
     "valor" (float; o texto pode ter milhar: "1.250,5") e "resultado" (minúsculo);
   - linhas com data ou valor inválidos (que geram ValueError na conversão) NÃO
     entram na lista: só são contadas em `ignoradas`.
2. `resumo_por_op(registros)` devolve um dicionário com as OPs em ordem alfabética:
       {"OP245101": {"linha": "A", "data": "01/10/2026", "ensaios": 3,
                     "reprovados": [], "situacao": "aprovada"}, ...}
   - "data": a data MAIS ANTIGA dos ensaios da OP, no formato dd/mm/aaaa;
   - "ensaios": quantos registros a OP tem;
   - "reprovados": nomes dos ensaios com resultado "reprovado", em ordem alfabética;
   - "situacao": "reprovada" se houver algum reprovado, senão "aprovada".
3. `salvar_json(dados, caminho)` grava o dicionário em JSON (UTF-8, indent=2,
   ensure_ascii=False), criando as pastas que faltarem no caminho.

Exemplo de JSON gerado:
    {
      "OP245103": {
        "linha": "C",
        "data": "05/10/2026",
        "ensaios": 3,
        "reprovados": ["espessura"],
        "situacao": "reprovada"
      }
    }

Dica: agrupe os registros por OP com defaultdict(list) e depois monte o resumo de
cada grupo. min() funciona com datas.

Teste com:  python curso.py testar 07 ex13
"""

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def numero_br(texto: str) -> float:
    """'1.250,5' -> 1250.5. Texto inválido gera ValueError (do float)."""
    return float(texto.strip().replace(".", "").replace(",", "."))


def ler_ensaios_csv(caminho: Path) -> tuple[list[dict], int]:
    """Lê o CSV; devolve (registros válidos, quantidade de linhas ignoradas)."""
    registros = []
    ignoradas = 0
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo, delimiter=";"):
            try:
                # Converte TUDO antes de guardar: ou a linha entra inteira, ou não entra.
                registro = {
                    "data": datetime.strptime(linha["data"].strip(), "%d/%m/%Y").date(),
                    "op": linha["op"].strip(),
                    "linha": linha["linha"].strip(),
                    "ensaio": linha["ensaio"].strip(),
                    "valor": numero_br(linha["valor"]),
                    "resultado": linha["resultado"].strip().lower(),
                }
            except ValueError:
                # Validação defensiva (módulo 06): conta e segue, sem derrubar o programa.
                ignoradas += 1
                continue
            registros.append(registro)
    return registros, ignoradas


def resumo_por_op(registros: list[dict]) -> dict[str, dict]:
    """Situação de cada OP (ordem alfabética de OP)."""
    por_op = defaultdict(list)
    for registro in registros:
        por_op[registro["op"]].append(registro)

    resumo = {}
    for op in sorted(por_op):
        grupo = por_op[op]
        reprovados = sorted(r["ensaio"] for r in grupo if r["resultado"] == "reprovado")
        primeira_data = min(r["data"] for r in grupo)  # datas se comparam como números
        resumo[op] = {
            "linha": grupo[0]["linha"],
            "data": primeira_data.strftime("%d/%m/%Y"),  # JSON não guarda date: vira texto
            "ensaios": len(grupo),
            "reprovados": reprovados,
            "situacao": "reprovada" if reprovados else "aprovada",
        }
    return resumo


def salvar_json(dados: dict, caminho: Path) -> None:
    """Grava `dados` em JSON legível (UTF-8, acentos preservados)."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)  # cria pastas que faltam
    with open(caminho, "w", encoding="utf-8") as arquivo:
        # ensure_ascii=False mantém "situação" legível em vez de "situação".
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
