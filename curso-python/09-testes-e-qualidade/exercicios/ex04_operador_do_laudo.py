"""
Exercício 09.04 — Operador do laudo (variável de ambiente)
Nível: ★☆☆

Contexto: cada computador do laboratório tem uma variável de ambiente
LAB_OPERADOR com o nome de quem está usando a máquina. O laudo precisa trazer
esse nome. Os testes deste exercício usam monkeypatch para criar e apagar a
variável sem mexer no seu computador de verdade (seção 12 da aula).

Tarefa: implemente as duas funções.
  operador_atual():
    - lê a variável de ambiente LAB_OPERADOR (use os.environ.get);
    - remove espaços em volta;
    - se a variável não existir ou estiver vazia (só espaços), devolve
      "não informado".
  assinatura_laudo(op):
    - devolve o texto "OP <op> | operador: <nome>", usando operador_atual().

Exemplos (com LAB_OPERADOR="  Maria Souza "):
    >>> operador_atual()
    'Maria Souza'
    >>> assinatura_laudo("12345")
    'OP 12345 | operador: Maria Souza'

Exemplo (sem a variável):
    >>> assinatura_laudo("777")
    'OP 777 | operador: não informado'

Dica: os.environ funciona como um dicionário. Não esqueça do "import os" no
topo do arquivo. Leia os testes para ver como o monkeypatch prepara o ambiente.

Teste com:  python curso.py testar 09 ex04
"""


def operador_atual() -> str:
    """Nome do operador (variável LAB_OPERADOR) ou 'não informado'."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def assinatura_laudo(op: str) -> str:
    """Texto 'OP <op> | operador: <nome>' para o rodapé do laudo."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
