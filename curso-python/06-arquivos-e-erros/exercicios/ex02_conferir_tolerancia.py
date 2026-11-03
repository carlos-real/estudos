"""
Exercício 06.02 — Levantar erro fora da tolerância
Nível: ★☆☆

Contexto: Antes de emitir um certificado, o sistema confere cada medição. Se
um valor estiver fora da faixa, o certificado NÃO pode sair: em vez de devolver
um aviso que alguém pode ignorar, a função levanta um erro.

A exceção `ValorForaDaTolerancia` já está criada no arquivo (seção 5 da aula).

Tarefa: implemente `conferir_tolerancia(valor, minimo, maximo)`:
- se `minimo` for maior que `maximo`, levante
  ValueError("faixa inválida: mínimo maior que máximo");
- se o valor estiver fora da faixa (os limites contam como dentro), levante
  ValorForaDaTolerancia com a mensagem
  f"{valor} fora da faixa [{minimo}, {maximo}]";
- se estiver tudo certo, devolva o próprio valor.

Exemplos:
    >>> conferir_tolerancia(25.4, 22.5, 27.5)
    25.4
    >>> conferir_tolerancia(28.0, 22.5, 27.5)
    Traceback (most recent call last):
      ...
    ValorForaDaTolerancia: 28.0 fora da faixa [22.5, 27.5]

Dica: confira primeiro a faixa, depois o valor. Cada problema, um `raise`.

Teste com:  python curso.py testar 06 ex02
"""


class ValorForaDaTolerancia(Exception):
    """Uma medição saiu da faixa permitida."""


def conferir_tolerancia(valor: float, minimo: float, maximo: float) -> float:
    """Devolve o valor se estiver na faixa; senão, levanta ValorForaDaTolerancia."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
