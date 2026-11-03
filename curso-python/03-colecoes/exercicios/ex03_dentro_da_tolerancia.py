"""
Exercício 03.03 — Dentro da tolerância?
Nível: ★☆☆

Contexto: Cada linha de produção tem uma faixa de espessura aceitável (mín, máx),
guardada num dicionário. Na planilha, o nome da linha às vezes vem digitado em
minúscula ou com espaços (" a ").

Tarefa: implemente `dentro_da_tolerancia(valor, linha, tolerancias)`.
- `tolerancias` é um dicionário  linha -> (mínimo, máximo), por exemplo
  {"A": (45.0, 55.0), "B": (18.0, 22.0)}.
- Limpe o nome da linha (tire espaços e passe para maiúscula) antes de procurar.
- Devolva True se mínimo <= valor <= máximo (os limites contam como dentro).
- Devolva False se o valor estiver fora da faixa.
- Devolva None se a linha não existir no dicionário.

Exemplos:
    >>> tolerancias = {"A": (45.0, 55.0), "B": (18.0, 22.0)}
    >>> dentro_da_tolerancia(50.2, "A", tolerancias)
    True
    >>> dentro_da_tolerancia(23.5, " b ", tolerancias)
    False
    >>> print(dentro_da_tolerancia(30.0, "Z", tolerancias))
    None

Dica: `tolerancias.get(chave)` devolve None quando a chave não existe, sem erro.
Depois, desempacote a tupla em duas variáveis.

Teste com:  python curso.py testar 03 ex03
"""


def dentro_da_tolerancia(
    valor: float, linha: str, tolerancias: dict[str, tuple[float, float]]
) -> bool | None:
    """Diz se o valor está na faixa da linha (None se a linha não existe)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
