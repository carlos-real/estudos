"""
Exercício 09.03 — Escreva os testes: média das medições
Nível: ★☆☆

Contexto: até aqui você escreveu funções e o curso escreveu os testes. Agora o
papel se inverte: a função calcular_media já existe, e VOCÊ escreve os testes
que garantem que ela está certa. É assim no trabalho: quem testa bem pega o bug
antes do cliente.

Tarefa: complete testar_calcular_media(calcular_media). Ela recebe como
parâmetro a função a testar (funções são valores, lembra do módulo 04?). Escreva
asserts que confiram as regras abaixo. Se a função recebida estiver errada,
algum assert deve falhar. Se estiver certa, nada pode falhar.

Regras de calcular_media(valores) — a especificação:
  - recebe uma lista de números e devolve a média aritmética (float);
  - funciona com valores negativos (ex.: desvios em relação ao nominal);
  - lista vazia levanta ValueError.

Como o curso corrige: chama a sua função com uma versão CORRETA de
calcular_media (nada pode falhar) e com 3 versões COM BUG escondidas nos testes
do curso (cada uma precisa ser reprovada por algum assert seu).

Exemplos de asserts que você pode usar:
    assert calcular_media([20.0, 21.0]) == pytest.approx(20.5)
    with pytest.raises(ValueError):
        calcular_media([])

Dica: pense nos erros que alguém cometeria ao escrever uma média. Uma média
"redonda" como [2, 4] -> 3 esconde vários bugs. Para usar pytest.approx e
pytest.raises, escreva "import pytest" no topo deste arquivo.

Teste com:  python curso.py testar 09 ex03
"""

from collections.abc import Callable


def testar_calcular_media(calcular_media: Callable[[list[float]], float]) -> None:
    """Confere a função recebida com asserts. Não devolve nada."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
