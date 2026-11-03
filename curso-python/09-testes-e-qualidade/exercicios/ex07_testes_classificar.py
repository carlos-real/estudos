"""
Exercício 09.07 — Escreva os testes: classificar uma medição
Nível: ★★☆

Contexto: a função classificar decide se uma medição está ABAIXO, OK ou ACIMA
da tolerância. Ela vai para o validador de certificados, então um erro aqui
libera bobina reprovada para o cliente. Sua missão é escrever testes tão bons
que nenhuma versão com bug passe por eles.

Tarefa: complete testar_classificar(classificar), escrevendo asserts que
confiram TODAS as regras abaixo.

Regras de classificar(valor, minimo, maximo) — a especificação:
  - devolve "ABAIXO" se valor < minimo;
  - devolve "ACIMA" se valor > maximo;
  - devolve "OK" se minimo <= valor <= maximo (as bordas estão DENTRO);
  - levanta ValueError se minimo > maximo (tolerância cadastrada errada).

Como o curso corrige: chama sua função com a versão CORRETA (nada pode falhar)
e com 4 versões COM BUG (cada uma precisa ser reprovada por algum assert seu).

Exemplo de assert:
    assert classificar(20.0, 19.0, 21.0) == "OK"

Dica: bugs adoram morar nas BORDAS e nos casos de erro. Para cada regra, pense
num valor que a confirma e num valor "no limite". Se quiser organizar melhor,
crie uma lista de casos (valor, minimo, maximo, esperado) e percorra com for.
Para pytest.raises, escreva "import pytest" no topo.

Teste com:  python curso.py testar 09 ex07
"""

from collections.abc import Callable


def testar_classificar(classificar: Callable[[float, float, float], str]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
