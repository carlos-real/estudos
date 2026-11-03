"""
Solução — Exercício 04.05 — A armadilha do padrão mutável

Ideia central: o valor padrão é criado UMA vez, quando o def roda. Se ele for
uma lista, todas as chamadas sem argumento compartilham a MESMA lista. O padrão
None + "crie aqui dentro" faz cada chamada ganhar uma lista nova.
"""


def adicionar_defeito(defeito: str, defeitos: list[str] | None = None) -> list[str]:
    """Acrescenta o defeito normalizado à lista (nova, se não vier uma) e a devolve."""
    if defeitos is None:
        defeitos = []  # criada AGORA, a cada chamada sem lista
    defeitos.append(defeito.strip().lower())
    return defeitos

    # Por que "is None" e não "if not defeitos"? Porque uma lista vazia que o
    # chamador passou de propósito também é falsy. Com "if not defeitos",
    # trocaríamos a lista dele por uma nova, e ele nunca veria o acréscimo.
