"""
Exercício 04.11 — Laudo decomposto em funções pequenas
Nível: ★★★

Contexto: O supervisor quer uma linha de resumo por OP no fim do turno:

    OP-4512 | 5/6 conformes (83.3%) | 1 abaixo, 0 acima | REPROVADO

Em vez de uma função gigante, você vai DECOMPOR o problema (seção 11 da aula):
cada função faz uma coisa só, e a última apenas junta as outras.

Tarefa: implemente as cinco funções, nesta ordem (de baixo para cima).
1. `calcular_limites(nominal, tol_pct)` -> (mínimo, máximo), nominal ∓ tol_pct %,
   cada um com round(..., 2).
2. `classificar(valor, limites)` -> "abaixo", "ok" ou "acima". `limites` é a
   tupla (mínimo, máximo); os limites contam como "ok".
3. `classificar_todas(medicoes, limites)` -> lista com a classe de cada medição.
4. `contar_por_classe(classes)` -> dicionário SEMPRE com as três chaves, na
   ordem {"abaixo": n, "ok": n, "acima": n} (zero quando não houver).
5. `resumo_lote(op, medicoes, nominal, tol_pct)` -> o texto do resumo:
   "{op} | {ok}/{total} conformes ({pct:.1f}%) | {abaixo} abaixo, {acima} acima | {situação}"
   - situação: "APROVADO" se todas estiverem ok; senão "REPROVADO".
   - sem medições: "{op} | sem medições".
   resumo_lote deve USAR as outras quatro funções.
Nenhuma função imprime nada nem altera a lista recebida.

Exemplos:
    >>> calcular_limites(50.0, 10.0)
    (45.0, 55.0)
    >>> classificar(44.9, (45.0, 55.0))
    'abaixo'
    >>> classificar_todas([50.2, 44.1, 56.3], (45.0, 55.0))
    ['ok', 'abaixo', 'acima']
    >>> contar_por_classe(["ok", "ok", "acima"])
    {'abaixo': 0, 'ok': 2, 'acima': 1}
    >>> resumo_lote("OP-4512", [50.2, 49.8, 44.1, 51.0, 50.5, 49.9], 50.0, 10.0)
    'OP-4512 | 5/6 conformes (83.3%) | 1 abaixo, 0 acima | REPROVADO'
    >>> resumo_lote("OP-4513", [], 50.0, 10.0)
    'OP-4513 | sem medições'

Dica: teste cada função no REPL antes de escrever a próxima. Quando chegar em
resumo_lote, ela deve ter poucas linhas: só chamadas e a montagem do texto.

Teste com:  python curso.py testar 04 ex11
"""


def calcular_limites(nominal: float, tol_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) para nominal ± tol_pct %, com 2 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def classificar(valor: float, limites: tuple[float, float]) -> str:
    """Classifica um valor como "abaixo", "ok" ou "acima" dos limites."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def classificar_todas(medicoes: list[float], limites: tuple[float, float]) -> list[str]:
    """Classifica cada medição, na mesma ordem."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def contar_por_classe(classes: list[str]) -> dict[str, int]:
    """Conta "abaixo", "ok" e "acima" (as três chaves sempre presentes)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumo_lote(op: str, medicoes: list[float], nominal: float, tol_pct: float) -> str:
    """Monta a linha de resumo do lote usando as outras funções."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
