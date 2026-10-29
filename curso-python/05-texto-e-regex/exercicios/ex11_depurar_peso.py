r"""
Exercício 05.11 — Depure a função do estagiário
Nível: ★★☆

Contexto: Um estagiário escreveu a função abaixo para pegar o peso de uma linha
do e-mail da expedição. "Funcionou no exemplo dele", mas a expedição reclamou
de pesos errados e de o programa quebrar.

    import re

    def extrair_peso_original(linha):
        achado = re.search("(\d+,\d+) kg", linha)
        return float(achado.group(1).replace(",", "."))

Tarefa, parte 1 (LEIA antes de rodar): sem executar o código, preveja o que
`extrair_peso_original` faz em cada caso e complete `previsoes()`, que devolve
uma tupla com 3 respostas:
  a) o valor devolvido para "Peso: 25,0 kg";
  b) o valor devolvido para "Peso: 1.250,5 kg";
  c) o NOME do erro (por exemplo, "ValueError") levantado para "Peso: 980 kg".
Só depois copie a função para o REPL e confira suas respostas.

Tarefa, parte 2: escreva `extrair_peso(linha)`, a versão corrigida:
- o número que interessa é o que vem depois da palavra "Peso" (maiúscula ou
  minúscula, com ou sem ":"); outros números da linha, como a tara, não contam;
- aceite ponto de milhar e decimais opcionais ("1.250,5", "980", "2.000,00");
- "kg" depois do número é opcional;
- devolva o peso como float, ou None se a linha não tiver peso.

Exemplos:
    >>> extrair_peso("OP: 123456 | NF: 98765 | Peso: 1.250,5 kg")
    1250.5
    >>> extrair_peso("peso 980")
    980.0
    >>> print(extrair_peso("Bom dia, laboratório!"))
    None

Dica: a função original tem 5 defeitos. Procure: o "r" que falta, o rótulo
"Peso" que ninguém procura, o ponto de milhar, os decimais obrigatórios e o
None que não é tratado.

Teste com:  python curso.py testar 05 ex11
"""


# Este exercício usa o módulo re.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import re


def previsoes() -> tuple:
    """Devolve (a, b, c): suas previsões para a função original."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def extrair_peso(linha: str) -> float | None:
    """Devolve o peso (em kg) que aparece depois de "Peso", ou None."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
