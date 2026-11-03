"""
Exercício 09.02 — Conserte o bug: número no formato brasileiro
Nível: ★☆☆

Contexto: a planilha do laboratório traz pesos e medidas como texto no formato
brasileiro ("1.250,50"). Um colega escreveu a função abaixo para converter esse
texto em float, mas os laudos estão saindo com números absurdos.

Tarefa: este exercício NÃO começa com NotImplementedError. A função já está
escrita e tem 1 bug. Encontre e corrija.
  1. Antes de rodar, LEIA o código e preveja: o que converter_numero_br("12,5")
     devolve hoje? Anote seu palpite.
  2. Rode os testes e leia a primeira falha: compare o esperado com o obtido.
  3. Teste sua hipótese no REPL (python) com um caso pequeno.
  4. Corrija com a menor mudança possível e rode os testes de novo.

Regras da função (o comportamento CORRETO):
  - Ponto é separador de milhar; vírgula é separador decimal.
  - Espaços em volta são ignorados.
  - Texto que não é um número válido levanta ValueError (o próprio float()
    já faz isso, desde que a conversão esteja certa).

Exemplos (comportamento correto):
    >>> converter_numero_br("1.250,50")
    1250.5
    >>> converter_numero_br(" 0,35 ")
    0.35

Dica: a ordem das operações importa. Escreva no papel o texto depois de cada
replace, para "12,5".

Teste com:  python curso.py testar 09 ex02
"""


def converter_numero_br(texto: str) -> float:
    """Converte '1.250,50' (formato brasileiro) em 1250.5."""
    limpo = texto.strip()
    limpo = limpo.replace(",", ".")
    limpo = limpo.replace(".", "")
    return float(limpo)
