"""
Exercício 07.07 — Agrupar a expedição por NF
Nível: ★★☆

Contexto: Cada e-mail da expedição traz uma lista de itens (op, nf, peso_kg). Um
mesmo dia tem vários e-mails, e uma NF pode ter várias OPs. Para emitir os
certificados você precisa juntar tudo e agrupar por NF.

Tarefa:
1. `juntar_emails(emails)` recebe uma lista de listas de itens e devolve UMA lista com
   todos os itens, na ordem (use itertools.chain).
2. `ops_por_nf(itens)` devolve {nf: [ops]} com as OPs na ordem em que aparecem, sem
   repetir a mesma OP dentro da mesma NF (use defaultdict(list)).
3. `peso_por_nf(itens)` devolve {nf: peso total}, com round(..., 2)
   (use defaultdict(float)).
As funções 2 e 3 devolvem dict comum (converta com dict(...)).

Exemplos:
    >>> email_1 = [("OP245101", "123456", 1250.5)]
    >>> email_2 = [("OP245102", "123456", 980.0), ("OP245103", "123457", 410.25)]
    >>> itens = juntar_emails([email_1, email_2])
    >>> len(itens)
    3
    >>> ops_por_nf(itens)
    {'123456': ['OP245101', 'OP245102'], '123457': ['OP245103']}
    >>> peso_por_nf(itens)
    {'123456': 2230.5, '123457': 410.25}

Dica: chain.from_iterable(lista_de_listas) "achata" uma lista de listas.

Teste com:  python curso.py testar 07 ex07
"""


def juntar_emails(emails: list[list[tuple[str, str, float]]]) -> list[tuple[str, str, float]]:
    """Todos os itens de todos os e-mails numa lista só."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def ops_por_nf(itens: list[tuple[str, str, float]]) -> dict[str, list[str]]:
    """OPs de cada NF, na ordem, sem repetição."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def peso_por_nf(itens: list[tuple[str, str, float]]) -> dict[str, float]:
    """Peso total de cada NF (kg, 2 casas)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
