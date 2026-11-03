"""
Solução — Exercício 00.02 — Saudação personalizada

Ideia central: o parâmetro `nome` é uma "caixa" que recebe um valor diferente a cada
chamada. Escrevendo `nome` SEM aspas, usamos o conteúdo da caixa.
"""


def saudar(nome: str) -> str:
    """Devolve a saudação 'Olá, <nome>!'."""
    # O `+` entre textos junta (concatena) os pedaços:
    #   "Olá, " + "Carlos" + "!"  ->  "Olá, Carlos!"
    # Repare no espaço depois da vírgula: ele faz parte do primeiro pedaço.
    return "Olá, " + nome + "!"

    # Alternativa muito usada (você vai dominar no módulo 01): f-string.
    # O f antes das aspas permite colocar variáveis entre chaves:
    #     return f"Olá, {nome}!"
    #
    # Erro comum: escrever "Olá, nome!" — aí sai a palavra "nome" literalmente,
    # porque dentro das aspas tudo é texto fixo.
