"""
Exercício 01.12 — Formatar em reais
Nível: ★★★

Contexto: O Python formata números no padrão americano: f"{1234.5:,.2f}" vira
"1,234.50". No Brasil, o certo é "1.234,50". Relatórios para a diretoria e para
clientes precisam do formato brasileiro.

Tarefa: implemente `formatar_reais(valor)`, que devolve o valor no formato
"R$ 1.234,56":
- sempre 2 casas decimais;
- ponto separando os milhares e vírgula separando os centavos;
- "R$ " (com espaço) na frente.
Considere apenas valores maiores ou iguais a zero.

Exemplos:
    >>> formatar_reais(1234.56)
    'R$ 1.234,56'
    >>> formatar_reais(0.5)
    'R$ 0,50'
    >>> formatar_reais(1234567.891)
    'R$ 1.234.567,89'

Dica: formate no padrão americano primeiro e depois troque os separadores. Se trocar
"," por "." e logo em seguida "." por ",", tudo vira vírgula. Use um caractere
provisório no meio do caminho.

Teste com:  python curso.py testar 01 ex12
"""


def formatar_reais(valor: float) -> str:
    """Devolve o valor formatado como moeda brasileira (R$ 1.234,56)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
