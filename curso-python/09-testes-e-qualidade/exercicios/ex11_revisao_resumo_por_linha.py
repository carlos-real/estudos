"""
Exercício 09.11 — Revisão: resumo por linha de produção (conserte os bugs)
Nível: ★★★

Revisão: mistura dicionários acumuladores (módulo 03), texto e números no
formato brasileiro (módulo 05) e exceções (módulo 06) com depuração guiada
por testes (este módulo).

Contexto: a planilha de valores tem registros "linha;valor", como "A;25,4". O
gerente quer, para cada linha de produção (A a D), quantas medições foram
feitas, quantas ficaram fora da tolerância e o percentual fora. O código abaixo
foi escrito às pressas e tem 4 bugs.

Tarefa: leia o código com calma, preveja o que ele faz e corrija os 4 bugs.
Sugestão de método (é o que um profissional faz):
  1. Rode os testes. Escolha UMA falha e leia o esperado x obtido.
  2. Formule uma hipótese ("acho que o total está sendo zerado porque...").
  3. Confirme no REPL ou com breakpoint() antes de mudar o código.
  4. Corrija, rode de novo, e só então passe para o próximo bug.

Regras (o comportamento CORRETO):
  - Cada registro é "linha;valor". A linha pode vir em minúsculas ou com
    espaços (" a "): normalize para maiúsculas sem espaços. O valor usa
    vírgula decimal ("25,4").
  - A tolerância de cada linha vem em tolerancias[linha] = (minimo, maximo).
    Um valor está FORA se for menor que o mínimo ou maior que o máximo
    (as bordas estão DENTRO).
  - O resultado é {linha: {"total": n, "fora": k, "percentual_fora": p}}, com
    p = k / n * 100 arredondado para 1 casa decimal.
  - Linha sem tolerância cadastrada levanta ValueError com a mensagem
    "linha <linha> sem tolerância cadastrada".

Exemplo (comportamento correto):
    >>> resumo = resumir_por_linha(
    ...     ["A;25,0", "A;27,0", "B;19,5", "A;25,5"],
    ...     {"A": (24.0, 26.0), "B": (18.0, 21.0)},
    ... )
    >>> resumo["A"]
    {'total': 3, 'fora': 1, 'percentual_fora': 33.3}
    >>> resumo["B"]
    {'total': 1, 'fora': 0, 'percentual_fora': 0.0}

Dica: nem todo bug aparece na primeira rodada; alguns só ficam visíveis depois
que você corrige outro. É normal: corrija, rode, leia de novo.

Teste com:  python curso.py testar 09 ex11
"""


def resumir_por_linha(
    registros: list[str], tolerancias: dict[str, tuple[float, float]]
) -> dict[str, dict]:
    """Resumo por linha: total de medições, quantas fora e o percentual fora."""
    resumo = {}
    for registro in registros:
        linha, texto_valor = registro.split(";")
        linha = linha.strip().upper()
        valor = float(texto_valor.strip().replace(",", "."))
        minimo, maximo = tolerancias[linha]
        fora = 1 if valor <= minimo or valor > maximo else 0
        resumo[linha] = {"total": 1, "fora": fora}
    for dados in resumo.values():
        dados["percentual_fora"] = round(dados["fora"] // dados["total"] * 100, 1)
    return resumo
