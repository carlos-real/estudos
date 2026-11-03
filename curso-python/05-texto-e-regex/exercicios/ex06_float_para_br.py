"""
Exercício 05.06 — Número no formato brasileiro
Nível: ★★☆

Contexto: O certificado e a resposta para a expedição mostram números no padrão
brasileiro: "1.250,50 kg", "0,215". As contas são feitas em float; a conversão
para texto só acontece na hora de mostrar.

Tarefa: implemente `float_para_br(valor, casas=2)`:
- ponto como separador de milhar e vírgula como separador decimal;
- exatamente `casas` casas decimais (arredondadas como faz a f-string);
- com `casas=0`, sem vírgula nenhuma;
- números negativos mantêm o sinal de menos.

Exemplos:
    >>> float_para_br(1250.5)
    '1.250,50'
    >>> float_para_br(0.215, 3)
    '0,215'
    >>> float_para_br(-1234567.891, 1)
    '-1.234.567,9'
    >>> float_para_br(980, 0)
    '980'

Dica: f"{valor:,.{casas}f}" gera o formato americano com a quantidade de casas
que está na variável. Depois é só trocar os símbolos sem que uma troca desfaça
a outra (seção 6 da aula).

Teste com:  python curso.py testar 05 ex06
"""


def float_para_br(valor: float, casas: int = 2) -> str:
    """Formata o número no padrão brasileiro (1.250,50)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
