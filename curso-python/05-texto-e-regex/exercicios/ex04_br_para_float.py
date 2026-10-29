"""
Exercício 05.04 — Converter número brasileiro
Nível: ★☆☆

Contexto: Na planilha e no e-mail, os números vêm no formato brasileiro:
"1.250,50", "25,4". O Python só entende ponto decimal, e "1.250" (mil duzentos
e cinquenta) viraria 1.25 sem nenhum aviso.

Tarefa: implemente `br_para_float(texto)`:
- aceite espaços nas pontas;
- "." é separador de milhar e "," é separador decimal;
- aceite sinal de menos na frente;
- se o texto não for um número válido, deixe o próprio `float()` levantar
  ValueError (não trate o erro: isso é assunto do módulo 06).

Exemplos:
    >>> br_para_float("1.250,50")
    1250.5
    >>> br_para_float(" 25,4 ")
    25.4
    >>> br_para_float("1.250")
    1250.0
    >>> br_para_float("-0,5")
    -0.5

Dica: a ordem das trocas importa (seção 6 da aula).

Teste com:  python curso.py testar 05 ex04
"""


def br_para_float(texto: str) -> float:
    """Converte um número no formato brasileiro ("1.250,5") para float."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
