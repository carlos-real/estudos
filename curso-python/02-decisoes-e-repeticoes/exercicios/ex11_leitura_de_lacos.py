"""
Exercício 02.11 — Leitura de código: preveja e conserte
Nível: ★★☆

Contexto: Programador passa mais tempo LENDO código do que escrevendo. Este exercício
treina isso: primeiro você prevê o que trechos prontos fazem; depois conserta uma
função com defeito.

PARTE 1 — Preveja. Para cada trecho abaixo, PRIMEIRO escreva sua previsão num papel
(faça um teste de mesa: anote o valor das variáveis a cada volta do laço). DEPOIS rode
o trecho no REPL para conferir. Se errou, descubra por quê. Por fim, faça cada função
`previsao_x()` devolver o valor final da variável pedida.

    Trecho A — valor final de `total`:
        total = 0
        for i in range(1, 10, 3):
            total += i

    Trecho B — valor final de `contador`:
        contador = 0
        n = 100
        while n > 1:
            n = n // 3
            contador += 1

    Trecho C — valor final de `texto`:
        texto = ""
        for letra in "bobina":
            if letra in "aeiou":
                continue
            texto += letra.upper()

    Trecho D — valor final de `achou`:
        posicao = 0
        achou = 0
        for valor in [25.1, 24.9, 22.0, 21.5, 20.0]:
            posicao += 1
            if valor < 23:
                achou = posicao
                break

PARTE 2 — Conserte. Um colega escreveu a função abaixo para calcular a média só das
notas maiores ou iguais a 7. Ela tem TRÊS defeitos. Encontre-os (rode, use print, faça
teste de mesa) e escreva a versão correta em `media_aprovadas`:

        def media_aprovadas(notas):
            for nota in notas:
                soma = 0
                quantidade = 0
                if nota >= 7:
                    soma += nota
                    quantidade + 1
            return soma / quantidade

    Regras da versão correta: média das notas >= 7; se nenhuma nota for >= 7 (ou a
    lista estiver vazia), devolva 0.0.

Exemplos:
    >>> media_aprovadas([8, 6, 9])
    8.5
    >>> media_aprovadas([5, 6])
    0.0

Dica: um dos defeitos só aparece com a lista vazia ou sem aprovados; outro faz a
função "esquecer" o que já somou.

Teste com:  python curso.py testar 02 ex11
"""


def previsao_a() -> int:
    """Devolve o valor final de `total` no trecho A."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_b() -> int:
    """Devolve o valor final de `contador` no trecho B."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_c() -> str:
    """Devolve o valor final de `texto` no trecho C."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def previsao_d() -> int:
    """Devolve o valor final de `achou` no trecho D."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def media_aprovadas(notas: list[float]) -> float:
    """Devolve a média das notas >= 7, ou 0.0 se não houver nenhuma."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
