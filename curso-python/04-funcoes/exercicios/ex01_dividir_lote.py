"""
Exercício 04.01 — Dividir o lote em bobinas
Nível: ★☆☆

Contexto: A produção precisa saber em quantas bobinas cheias um lote vai ser
dividido e quanto sobra. Às vezes alguém digita o peso da bobina como 0 na
planilha, e o programa não pode quebrar por isso.

Tarefa: implemente duas funções.
1. `dividir_em_bobinas(peso_total_kg, peso_bobina_kg)` devolve uma TUPLA
   (bobinas_cheias, sobra_kg), com a sobra arredondada com round(..., 2).
   Se peso_bobina_kg for 0 ou negativo, devolva None (retorno antecipado).
2. `descrever_divisao(peso_total_kg, peso_bobina_kg)` usa a primeira função e
   devolve um texto:
   - "4 bobinas de 300.0 kg + sobra de 50.5 kg"
   - "peso da bobina inválido"  (quando a primeira devolve None)
   Os pesos no texto aparecem com 1 casa decimal.

Exemplos:
    >>> dividir_em_bobinas(1250.5, 300)
    (4, 50.5)
    >>> dividir_em_bobinas(900, 300)
    (3, 0.0)
    >>> print(dividir_em_bobinas(500, 0))
    None
    >>> descrever_divisao(1250.5, 300)
    '4 bobinas de 300.0 kg + sobra de 50.5 kg'

Dica: // dá a parte inteira da divisão e % dá o resto (módulo 01). Na segunda
função, desempacote a tupla: bobinas, sobra = resultado.

Teste com:  python curso.py testar 04 ex01
"""


def dividir_em_bobinas(
    peso_total_kg: float, peso_bobina_kg: float
) -> tuple[int, float] | None:
    """Devolve (bobinas cheias, sobra em kg) ou None se o peso da bobina for inválido."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def descrever_divisao(peso_total_kg: float, peso_bobina_kg: float) -> str:
    """Descreve a divisão em texto, usando dividir_em_bobinas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
