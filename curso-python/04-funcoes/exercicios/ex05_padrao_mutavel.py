"""
Exercício 04.05 — A armadilha do padrão mutável
Nível: ★☆☆

Contexto: Um colega escreveu esta função para anotar defeitos de inspeção:

    def adicionar_defeito(defeito, defeitos=[]):
        defeitos.append(defeito.strip().lower())
        return defeitos

Na primeira inspeção do dia, adicionar_defeito("Bolha") devolveu ["bolha"].
Na segunda, numa bobina sem relação nenhuma com a primeira,
adicionar_defeito("Risco") devolveu ["bolha", "risco"]. A "bolha" veio de onde?
(Resposta na seção 3 da aula.)

Tarefa: implemente `adicionar_defeito(defeito, defeitos=None)` do jeito certo.
- Normalize o defeito (strip + lower) antes de acrescentar.
- Se `defeitos` não for informado, comece uma lista NOVA a cada chamada.
- Se `defeitos` for informado, acrescente nessa lista (é o objetivo declarado
  da função) e devolva essa mesma lista.

Exemplos:
    >>> adicionar_defeito("Bolha")
    ['bolha']
    >>> adicionar_defeito("Risco")
    ['risco']
    >>> anotados = ["gel"]
    >>> adicionar_defeito(" Bolha ", anotados)
    ['gel', 'bolha']
    >>> anotados
    ['gel', 'bolha']

Dica: o idioma é "if defeitos is None: defeitos = []".

Teste com:  python curso.py testar 04 ex05
"""


def adicionar_defeito(defeito: str, defeitos: list[str] | None = None) -> list[str]:
    """Acrescenta o defeito normalizado à lista (nova, se não vier uma) e a devolve."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
