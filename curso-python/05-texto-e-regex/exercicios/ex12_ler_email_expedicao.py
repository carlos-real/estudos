"""
Exercício 05.12 — Ler o e-mail da expedição
Nível: ★★★

Contexto: A expedição manda um e-mail por carga, com uma linha por pedido. O
formato padrão é "OP: 123456 | NF: 98765 | Peso: 1.250,5 kg", mas cada pessoa
digita de um jeito: "op 123457; nf 98.766; peso 980". O robô dos certificados
precisa entender todas as variações abaixo.

Tarefa: implemente `ler_email_expedicao(texto)`, que devolve uma lista com um
dicionário por pedido, na ordem do e-mail:
    {"op": "123456", "nf": "98765", "peso_kg": 1250.5}
Uma linha de pedido tem os campos OP, NF e Peso, NESTA ORDEM, separados por
"|" ou ";":
- os rótulos OP, NF e Peso podem vir em maiúsculas ou minúsculas, com ou sem
  ":" depois; entre "OP" e o número também pode haver um "-" ("OP-123456");
- OP: exatamente 6 dígitos;
- NF: dígitos, com ou sem pontos de milhar ("98.765"); devolva só os dígitos;
- Peso: número no formato brasileiro, com "kg" opcional depois;
- espaços extras em volta de qualquer parte são permitidos.
Linhas fora desse formato são ignoradas. E-mail sem pedidos devolve [].

Exemplos:
    >>> email = '''Bom dia!
    ... OP: 123456 | NF: 98765 | Peso: 1.250,5 kg
    ... op 123457; nf 98.766; peso 980
    ... A OP 123459 vai na próxima carga.'''
    >>> for pedido in ler_email_expedicao(email):
    ...     print(pedido)
    {'op': '123456', 'nf': '98765', 'peso_kg': 1250.5}
    {'op': '123457', 'nf': '98766', 'peso_kg': 980.0}

Dica: parta do padrão da seção 15 da aula e acrescente UMA variação por vez,
testando todos os exemplos a cada mudança. Tanto `re.MULTILINE` quanto um `for`
nas linhas (`splitlines`) funcionam.

Teste com:  python curso.py testar 05 ex12
"""


# Este exercício usa o módulo re.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import re


def ler_email_expedicao(texto: str) -> list[dict]:
    """Extrai os pedidos (OP, NF e peso) do texto do e-mail."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
