"""
Exercício 05.01 — Padronizar nome de cliente
Nível: ★☆☆

Contexto: O nome do cliente chega do ERP e dos e-mails de muitos jeitos:
"  embalagens   DO sul  ltda ", "EMBALAGENS DO SUL LTDA". O certificado de
qualidade precisa mostrar sempre o mesmo formato.

Tarefa: implemente `limpar_nome(nome)`, que devolve o nome padronizado:
- sem espaços nas pontas e com UM espaço entre as palavras (tabs e quebras de
  linha também contam como espaço);
- cada palavra com a primeira letra maiúscula e o resto minúsculo;
- exceção: as palavras "da", "das", "de", "do", "dos" e "e" ficam minúsculas,
  a não ser que sejam a PRIMEIRA palavra do nome;
- nome vazio (ou só com espaços) devolve "".

Exemplos:
    >>> limpar_nome("  embalagens   DO sul  ltda ")
    'Embalagens do Sul Ltda'
    >>> limpar_nome("JOÃO DA SILVA E FILHOS")
    'João da Silva e Filhos'
    >>> limpar_nome("de souza plásticos")
    'De Souza Plásticos'

Dica: `split()` sem argumento já resolve os espaços repetidos. Percorra as
palavras com `enumerate` para saber qual é a primeira.

Teste com:  python curso.py testar 05 ex01
"""


def limpar_nome(nome: str) -> str:
    """Devolve o nome com espaços normalizados e maiúsculas padronizadas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
