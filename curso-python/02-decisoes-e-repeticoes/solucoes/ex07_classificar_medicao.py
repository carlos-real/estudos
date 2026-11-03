"""
Exercício 02.07 — Classificar uma medição
Nível: ★★☆

Contexto: Não basta saber se a medição está fora: o operador da extrusora precisa saber
para que LADO ela saiu, para ajustar a máquina (abrir ou fechar a matriz).

Tarefa: implemente `classificar_medicao(valor, nominal, tolerancia_pct)`, que:
1. devolve "INVÁLIDA" se o valor for menor ou igual a zero (falha do micrômetro);
2. calcula os limites: nominal ± tolerancia_pct% do nominal;
3. devolve "ABAIXO" se o valor for menor que o mínimo;
4. devolve "ACIMA" se o valor for maior que o máximo;
5. devolve "DENTRO" nos demais casos (os limites estão dentro).

Exemplos:
    >>> classificar_medicao(25.4, 25, 10)
    'DENTRO'
    >>> classificar_medicao(22.4, 25, 10)
    'ABAIXO'
    >>> classificar_medicao(0, 25, 10)
    'INVÁLIDA'

Dica: calcule minimo e maximo em variáveis ANTES dos ifs. Fica mais legível e você
confere os limites com um print se algo der errado.

Teste com:  python curso.py testar 02 ex07
"""


def classificar_medicao(valor: float, nominal: float, tolerancia_pct: float) -> str:
    """Classifica a medição em 'INVÁLIDA', 'ABAIXO', 'DENTRO' ou 'ACIMA'."""
    # Validação primeiro (cláusula de guarda): um zero não é "ABAIXO", é falha.
    if valor <= 0:
        return "INVÁLIDA"

    margem = nominal * tolerancia_pct / 100
    minimo = nominal - margem
    maximo = nominal + margem

    if valor < minimo:
        return "ABAIXO"
    elif valor > maximo:
        return "ACIMA"
    else:
        # Sobrou: minimo <= valor <= maximo. Os limites estão dentro porque usamos
        # < e > estritos acima.
        return "DENTRO"
