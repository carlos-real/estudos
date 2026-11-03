"""
Exercício 09.09 — Relatório no terminal (testado com capsys)
Nível: ★★☆

Contexto: no fim da conferência, o programa imprime um resumo para o técnico
conferir na tela antes de emitir os certificados. Funções que só imprimem
também podem (e devem) ser testadas: a fixture capsys captura o que foi
impresso (seção 10 da aula).

Tarefa: implemente imprimir_relatorio(resultados). Cada resultado é uma tupla
(op, valor, dentro) em que dentro é True (OK) ou False (FORA).
  - Lista vazia: imprima apenas a linha "Nenhuma amostra."
  - Senão, imprima:
      1. o cabeçalho "OP | VALOR | SITUAÇÃO";
      2. uma linha por resultado: "<op> | <valor> | OK" ou "... | FORA",
         com o valor no formato brasileiro, 2 casas decimais e ponto de milhar
         (25.4 -> "25,40"; 1250.5 -> "1.250,50");
      3. a linha final "Total: <n> amostra(s), <k> fora".
  - A função não devolve nada (só imprime).

Exemplo:
    >>> imprimir_relatorio([("12345", 25.4, True), ("12346", 1250.5, False)])
    OP | VALOR | SITUAÇÃO
    12345 | 25,40 | OK
    12346 | 1.250,50 | FORA
    Total: 2 amostra(s), 1 fora

Dica: f"{valor:,.2f}" dá "1,250.50" (padrão americano). Troque os separadores
como no módulo 05, usando um caractere temporário. Uma função auxiliar
formatar_br(valor) deixa o código mais limpo.

Teste com:  python curso.py testar 09 ex09
"""


def imprimir_relatorio(resultados: list[tuple[str, float, bool]]) -> None:
    """Imprime o relatório da conferência no terminal."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
