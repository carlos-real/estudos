"""
Exercício 03.12 — Revisão: relatório de tolerâncias
Nível: ★★★

Contexto: Este exercício mistura o módulo 03 (dicionário aninhado, lista de
dicionários) com o 01 (strip, upper, f-strings, round) e o 02 (if, for,
acumuladores). As tolerâncias de cada linha ficam num dicionário aninhado:

    TOLERANCIAS = {
        "A": {"espessura": {"nominal": 50.0, "tol_pct": 10.0},
              "gramatura": {"nominal": 46.0, "tol_pct": 5.0}},
        "B": {"espessura": {"nominal": 20.0, "tol_pct": 8.0}},
    }

Tarefa: implemente quatro funções pequenas, cada uma usando a anterior.
1. `limites(nominal, tol_pct)` devolve a tupla (mínimo, máximo), com
   mínimo = nominal × (1 − tol_pct/100) e máximo = nominal × (1 + tol_pct/100),
   ambos arredondados com round(..., 2).
2. `falhas_da_amostra(amostra, tolerancias)` devolve a lista de falhas.
   - Normalize a linha da amostra (strip + upper).
   - Se a linha não tem tolerância cadastrada, devolva None.
   - Para cada propriedade da linha (na ordem do dicionário), se a amostra
     tiver valor (não None) e ele estiver fora de [mínimo, máximo], acrescente
     o texto  f"{propriedade} {valor:.1f} fora de {minimo:.1f} a {maximo:.1f}".
3. `linha_do_relatorio(amostra, tolerancias)` devolve um texto:
   - "OP-4512 | linha A | APROVADA"  (sem falhas)
   - "OP-4512 | linha A | REPROVADA: falha 1; falha 2"  (falhas unidas por "; ")
   - "OP-4512 | linha E | PENDENTE: sem tolerância cadastrada"  (None)
4. `relatorio(amostras, tolerancias)` devolve a lista com uma linha de
   relatório por amostra e, no fim, o total:
   "Total: 3 amostras, 1 aprovadas (33.3%)". Sem amostras: 0.0%.
Não altere as amostras nem as tolerâncias.

Exemplos:
    >>> limites(46.0, 5.0)
    (43.7, 48.3)
    >>> amostra = {"op": "OP-4512", "linha": " a", "espessura": 56.3, "gramatura": 46.2}
    >>> falhas_da_amostra(amostra, TOLERANCIAS)
    ['espessura 56.3 fora de 45.0 a 55.0']
    >>> linha_do_relatorio(amostra, TOLERANCIAS)
    'OP-4512 | linha A | REPROVADA: espessura 56.3 fora de 45.0 a 55.0'

Dica: "; ".join(lista) junta textos de uma lista separando por "; " (o join é
visto a fundo no módulo 05). Um laço que concatena strings também resolve.

Teste com:  python curso.py testar 03 ex12
"""

# Dados do exemplo (os testes usam os próprios dados).
TOLERANCIAS = {
    "A": {
        "espessura": {"nominal": 50.0, "tol_pct": 10.0},
        "gramatura": {"nominal": 46.0, "tol_pct": 5.0},
    },
    "B": {"espessura": {"nominal": 20.0, "tol_pct": 8.0}},
}


def limites(nominal: float, tol_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± tol_pct %, em 2 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def falhas_da_amostra(amostra: dict, tolerancias: dict) -> list[str] | None:
    """Lista as propriedades fora da tolerância (None se a linha não existe)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def linha_do_relatorio(amostra: dict, tolerancias: dict) -> str:
    """Monta o texto de uma amostra: APROVADA, REPROVADA: ... ou PENDENTE: ..."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def relatorio(amostras: list[dict], tolerancias: dict) -> list[str]:
    """Uma linha por amostra e uma linha final de total."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
