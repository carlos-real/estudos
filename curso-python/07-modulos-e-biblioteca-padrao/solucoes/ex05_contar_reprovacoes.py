"""
Exercício 07.05 — Reprovações por linha com Counter
Nível: ★☆☆

Contexto: Toda sexta a coordenação pergunta: "qual linha mais reprovou na semana?".
Você tem a lista de ensaios do período, cada um como um dicionário:
    {"op": "OP245103", "linha": "C", "ensaio": "espessura", "resultado": "reprovado"}

Tarefa:
1. `contar_reprovacoes(ensaios)` devolve um Counter com quantas reprovações cada
   linha teve. Compare o resultado sem diferenciar maiúsculas ("REPROVADO" também
   conta). Linhas sem reprovação não precisam aparecer.
2. `piores_linhas(ensaios, n=2)` devolve a lista das `n` linhas com mais reprovações,
   como tuplas (linha, quantidade), da maior para a menor (empate: quem apareceu
   primeiro na lista vem antes, que é o comportamento do most_common).
3. `taxa_reprovacao(ensaios)` devolve um dicionário {linha: % de reprovação}, com
   round(..., 1), para TODAS as linhas que aparecem nos ensaios (inclusive 0.0%).

Exemplos:
    >>> ensaios = [
    ...     {"linha": "A", "resultado": "aprovado"},
    ...     {"linha": "C", "resultado": "reprovado"},
    ...     {"linha": "C", "resultado": "REPROVADO"},
    ...     {"linha": "B", "resultado": "reprovado"},
    ... ]
    >>> contar_reprovacoes(ensaios)
    Counter({'C': 2, 'B': 1})
    >>> piores_linhas(ensaios, 1)
    [('C', 2)]
    >>> taxa_reprovacao(ensaios)
    {'A': 0.0, 'C': 100.0, 'B': 100.0}

Dica: from collections import Counter. Um Counter devolve 0 para chave ausente.

Teste com:  python curso.py testar 07 ex05
"""

from collections import Counter


def contar_reprovacoes(ensaios: list[dict]) -> Counter:
    """Quantidade de reprovações por linha."""
    # O Counter recebe qualquer sequência e conta quantas vezes cada item aparece.
    # Aqui a sequência é "a linha de cada ensaio reprovado".
    return Counter(e["linha"] for e in ensaios if e["resultado"].lower() == "reprovado")


def piores_linhas(ensaios: list[dict], n: int = 2) -> list[tuple[str, int]]:
    """As n linhas com mais reprovações, da maior para a menor."""
    return contar_reprovacoes(ensaios).most_common(n)


def taxa_reprovacao(ensaios: list[dict]) -> dict[str, float]:
    """Percentual de reprovação de cada linha (todas as linhas presentes)."""
    total_por_linha = Counter(e["linha"] for e in ensaios)
    reprovados = contar_reprovacoes(ensaios)
    # Percorremos o total (que tem TODAS as linhas). Para linha sem reprovação,
    # reprovados[linha] vale 0: é a vantagem do Counter sobre o dict comum.
    return {
        linha: round(reprovados[linha] / total * 100, 1)
        for linha, total in total_por_linha.items()
    }
