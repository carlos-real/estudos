"""
Exercício 01.01 — Apresentação
Nível: ★☆☆

Contexto: Todo programa começa conversando com alguém. Aqui você monta uma frase de
apresentação a partir de três informações.

Tarefa: implemente `apresentar(nome, idade, cidade)`, que DEVOLVE (com return, sem
print) exatamente a frase:
    Meu nome é <nome>, tenho <idade> anos e moro em <cidade>.
- Use uma f-string.
- Não mude nada nos valores recebidos (nem maiúsculas, nem espaços).

Exemplos:
    >>> apresentar("Ana", 28, "Joinville")
    'Meu nome é Ana, tenho 28 anos e moro em Joinville.'
    >>> apresentar("Carlos Souza", 41, "São Bento do Sul")
    'Meu nome é Carlos Souza, tenho 41 anos e moro em São Bento do Sul.'

Dica: o REPL mostra o texto devolvido entre aspas; as aspas não fazem parte da frase.

Teste com:  python curso.py testar 01 ex01
"""


def apresentar(nome: str, idade: int, cidade: str) -> str:
    """Devolve a frase de apresentação com nome, idade e cidade."""
    # A f-string encaixa cada valor no lugar das chaves. Repare que a idade é um int
    # e mesmo assim entra no texto sem str(): a f-string converte sozinha.
    return f"Meu nome é {nome}, tenho {idade} anos e moro em {cidade}."

    # Alternativa (funciona, mas é mais fácil errar espaços e esquecer o str()):
    # return "Meu nome é " + nome + ", tenho " + str(idade) + " anos e moro em " + cidade + "."
