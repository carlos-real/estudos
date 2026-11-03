"""
Exercício 05.02 — Formatar número de NF
Nível: ★☆☆

Contexto: O número da nota fiscal eletrônica tem até 9 dígitos. No e-mail ele
aparece de todo jeito ("12345", "NF-e 98.765"), mas no certificado precisa
aparecer sempre igual: 9 dígitos em grupos de 3, como "000.012.345".

Tarefa: implemente `formatar_nf(numero)`:
- fique só com os dígitos do texto (ignore letras, espaços, pontos, hífens);
- complete com zeros à esquerda até ter 9 dígitos;
- devolva no formato "DDD.DDD.DDD";
- se o texto não tiver nenhum dígito, devolva "".
Você pode supor que nunca haverá mais de 9 dígitos.

Exemplos:
    >>> formatar_nf("12345")
    '000.012.345'
    >>> formatar_nf("NF-e 98.765")
    '000.098.765'
    >>> formatar_nf("123456789")
    '123.456.789'
    >>> formatar_nf("sem número")
    ''

Dica: `"".join([c for c in texto if c.isdigit()])` fica só com os dígitos.
Depois, `zfill` e fatiamento.

Teste com:  python curso.py testar 05 ex02
"""


def formatar_nf(numero: str) -> str:
    """Devolve a NF com 9 dígitos no formato DDD.DDD.DDD (ou "" sem dígitos)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
