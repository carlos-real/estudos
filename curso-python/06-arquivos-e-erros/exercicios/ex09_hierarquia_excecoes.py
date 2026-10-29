"""
Exercício 06.09 — Suas próprias exceções
Nível: ★★☆

Contexto: O sistema de qualidade tem problemas de tipos diferentes: a OP não
tem especificação cadastrada, ou a medição saiu da faixa. Quem chama precisa
poder tratar cada um do seu jeito, ou todos de uma vez.

Tarefa 1: crie TRÊS classes de exceção (seção 5 da aula):
- ErroDeQualidade, filha de Exception (a "mãe" de todas);
- EspecificacaoAusente, filha de ErroDeQualidade;
- ValorForaDaTolerancia, filha de ErroDeQualidade.

Tarefa 2: implemente `verificar_medicao(op, ensaio, valor, especificacoes)`.
`especificacoes` tem o formato {"123456": {"espessura": (22.5, 27.5)}}.
- OP fora de `especificacoes`: levante
  EspecificacaoAusente(f"OP {op} sem especificação");
- ensaio fora da especificação da OP: levante
  EspecificacaoAusente(f"OP {op} sem limite para {ensaio}");
- valor fora da faixa (limites contam como dentro): levante
  ValorForaDaTolerancia(f"OP {op}: {ensaio} = {valor} fora de [{mín}, {máx}]");
- tudo certo: devolva "OK".

Tarefa 3: implemente `resumir_conferencia(medicoes, especificacoes)`.
`medicoes` é uma lista de tuplas (op, ensaio, valor). Confira cada uma com
`verificar_medicao` e devolva {"aprovadas": N, "problemas": [mensagens]}, em que
cada mensagem é str(erro). Capture SÓ ErroDeQualidade: qualquer outro erro
(um bug) deve continuar subindo.

Exemplos:
    >>> specs = {"123456": {"espessura": (22.5, 27.5)}}
    >>> verificar_medicao("123456", "espessura", 25.0, specs)
    'OK'
    >>> resumir_conferencia([("123456", "espessura", 25.0), ("999999", "cof", 0.2)], specs)
    {'aprovadas': 1, 'problemas': ['OP 999999 sem especificação']}

Dica: uma classe de exceção pode ter só a docstring no corpo. E um único
`except ErroDeQualidade as erro:` captura as duas filhas.

Teste com:  python curso.py testar 06 ex09
"""


# Tarefa 1: crie aqui as três classes de exceção (ErroDeQualidade,
# EspecificacaoAusente e ValorForaDaTolerancia).


def verificar_medicao(op: str, ensaio: str, valor: float, especificacoes: dict) -> str:
    """Devolve "OK" ou levanta EspecificacaoAusente / ValorForaDaTolerancia."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def resumir_conferencia(medicoes: list[tuple], especificacoes: dict) -> dict:
    """Confere todas as medições sem parar no primeiro problema."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
