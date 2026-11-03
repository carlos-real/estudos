"""
Exercício 05.08 — Encontrar OPs num texto
Nível: ★★☆

Contexto: Nem todo e-mail segue o padrão. Às vezes alguém escreve "liberar a
OP 123456 e a op-123457 hoje". O robô precisa achar todas as OPs citadas.

Tarefa: implemente `extrair_ops(texto)`, que devolve a lista dos números de OP
(como texto, 6 dígitos) na ordem em que aparecem, SEM repetir.
Uma OP no texto é:
- a sigla "OP", maiúscula ou minúscula, sem letra ou dígito colado ANTES dela
  ("TOP 111111" não conta);
- seguida de separadores opcionais, em qualquer quantidade: espaços, ":" ou "-";
- seguida de exatamente 6 dígitos, que não podem ter letra nem dígito colado
  depois ("OP 1234567" não conta).

Exemplos:
    >>> extrair_ops("Liberar OP 123456 e op-123457. A OP: 123456 já foi.")
    ['123456', '123457']
    >>> extrair_ops("OP 1234567 tem dígito demais; TOP 111111 não é OP")
    []
    >>> extrair_ops("Sem OPs hoje")
    []

Dica: com UM grupo de captura no padrão, `re.findall` devolve só o conteúdo do
grupo. Para não repetir, confira se o número já está na lista antes de pôr.

Teste com:  python curso.py testar 05 ex08
"""


# Este exercício usa o módulo re.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import re


def extrair_ops(texto: str) -> list[str]:
    """Devolve os números de OP citados no texto, na ordem, sem repetir."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
