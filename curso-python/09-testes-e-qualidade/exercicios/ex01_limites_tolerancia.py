"""
Exercício 09.01 — Limites de tolerância (TDD: os testes vêm primeiro)
Nível: ★☆☆

Contexto: a especificação de um filme diz "espessura 20 µm ± 5%". O laboratório
precisa saber o mínimo e o máximo aceitáveis para conferir cada bobina.

Tarefa: implemente calcular_limites(nominal, tolerancia_pct), que devolve a tupla
(minimo, maximo) de nominal ± tolerancia_pct %.
  - nominal deve ser maior que zero; senão, levante ValueError.
  - tolerancia_pct não pode ser negativa; senão, levante ValueError com uma
    mensagem que contenha a palavra "tolerância".
  - tolerância zero é válida: mínimo e máximo ficam iguais ao nominal.

Faça no ciclo do TDD (seção 13 da aula):
  1. VERMELHO: rode os testes e veja todos falharem. Leia o arquivo
     testes/test_m09_ex01_limites_tolerancia.py: ele é a especificação.
  2. VERDE: escreva o código mais simples que faça os testes passarem.
  3. REFATORAR: melhore nomes e organização, rodando os testes de novo.

Exemplos:
    >>> calcular_limites(20.0, 5.0)
    (19.0, 21.0)
    >>> calcular_limites(25.0, 10.0)
    (22.5, 27.5)

Dica: a margem é nominal * tolerancia_pct / 100.

Teste com:  python curso.py testar 09 ex01
"""


def calcular_limites(nominal: float, tolerancia_pct: float) -> tuple[float, float]:
    """Devolve (mínimo, máximo) de nominal ± tolerancia_pct %."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
