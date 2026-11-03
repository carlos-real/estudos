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

import re

PADRAO_PEDIDO = re.compile(
    r"""
    ^ \s*
    OP   \s* [:-]? \s* (?P<op>\d{6})       # OP, separador opcional, 6 dígitos
    \s* [|;] \s*                           # separador entre campos: | ou ;
    NF   \s* :?    \s* (?P<nf>\d[\d.]*)    # NF com pontos de milhar opcionais
    \s* [|;] \s*
    PESO \s* :?    \s* (?P<peso>\d[\d.]*(?:,\d+)?)   # peso brasileiro
    \s* (?:kg)? \s* $                      # "kg" opcional e mais nada
    """,
    re.VERBOSE | re.IGNORECASE | re.MULTILINE,
)


def br_para_float(texto: str) -> float:
    """Converte "1.250,5" em 1250.5 (mesma ideia do ex04)."""
    return float(texto.replace(".", "").replace(",", "."))


def ler_email_expedicao(texto: str) -> list[dict]:
    """Extrai os pedidos (OP, NF e peso) do texto do e-mail."""
    pedidos = []
    # MULTILINE faz ^ e $ valerem para cada linha. finditer entrega um Match
    # por pedido, na ordem do texto.
    for achado in PADRAO_PEDIDO.finditer(texto):
        pedidos.append(
            {
                "op": achado["op"],
                "nf": achado["nf"].replace(".", ""),
                "peso_kg": br_para_float(achado["peso"]),
            }
        )
    return pedidos

    # Alternativa com for nas linhas (o padrão continua o mesmo, sem MULTILINE,
    # usando fullmatch em cada linha):
    #     for linha in texto.splitlines():
    #         achado = PADRAO_PEDIDO.fullmatch(linha)
    #         if achado: ...
    # E-mails com quebra de linha do Windows ("\r\n") também funcionam: o \s*
    # antes do $ engole o "\r".
