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

from pathlib import Path


def ler_ensaios_csv(caminho: Path) -> tuple[list[dict], int]:
    """Lê o CSV; devolve (registros válidos, quantidade de linhas ignoradas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_por_op(registros: list[dict]) -> dict[str, dict]:
    """Situação de cada OP (ordem alfabética de OP)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def salvar_json(dados: dict, caminho: Path) -> None:
    """Grava `dados` em JSON legível (UTF-8, acentos preservados)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
