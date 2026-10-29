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


# Este exercício usa o módulo re.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import re


def validar_op(codigo: str) -> bool:
    """Diz se o texto é um código de OP válido (ex.: "OP 123456")."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
