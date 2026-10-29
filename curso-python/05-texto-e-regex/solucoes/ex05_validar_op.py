r"""
Exercício 05.05 — Validar código de OP
Nível: ★☆☆

Contexto: Antes de procurar a OP no ERP, o robô confere se o que foi digitado
tem cara de código de OP. Isso evita buscas inúteis e mensagens confusas.

Tarefa: implemente `validar_op(codigo)`, que devolve True ou False.
É válido o texto que, depois de tirar os espaços das pontas, é formado
EXATAMENTE por:
- as letras "OP" (maiúsculas ou minúsculas);
- opcionalmente, UM espaço ou UM hífen;
- exatamente 6 dígitos.
Nada antes, nada depois.

Exemplos:
    >>> validar_op("OP 123456")
    True
    >>> validar_op(" op-004512 ")
    True
    >>> validar_op("OP123456")
    True
    >>> validar_op("OP 12345")
    False
    >>> validar_op("OP 123456 cancelada")
    False

Dica: é o padrão construído na seção 10 da aula. `re.fullmatch` devolve um
Match ou None; transforme em bool. Lembre-se do `import re` no topo do arquivo.

Teste com:  python curso.py testar 05 ex05
"""

import re

# Padrão compilado uma vez só, numa constante com nome claro.
# [ -]? = "um espaço ou um hífen, ou nada"; \d{6} = exatamente seis dígitos.
PADRAO_OP = re.compile(r"OP[ -]?\d{6}", re.IGNORECASE)


def validar_op(codigo: str) -> bool:
    """Diz se o texto é um código de OP válido (ex.: "OP 123456")."""
    # fullmatch exige que o texto INTEIRO case. Com search, "XOP 1234567"
    # passaria, porque "OP 123456" aparece lá dentro.
    return PADRAO_OP.fullmatch(codigo.strip()) is not None

    # Alternativa equivalente, sem compilar:
    #     return bool(re.fullmatch(r"OP[ -]?\d{6}", codigo.strip(), re.IGNORECASE))
