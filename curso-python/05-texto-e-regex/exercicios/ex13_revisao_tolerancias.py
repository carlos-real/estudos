r"""
Exercício 05.13 — Revisão: ler a especificação da OP
Nível: ★★★

Contexto: Quando a OP tem especificação especial, ela chega como texto: um
título e uma linha por ensaio. Espessura e gramatura usam tolerância sobre o
valor nominal (± %); os outros ensaios usam faixa de mínimo a máximo.

    ESPECIFICAÇÃO ESPECIAL - CLIENTE PLASTIFORT
    Espessura: 25 µm ± 10%
    Gramatura: 23,0 g/m² +/- 5%
    COF estático: 0,15 a 0,30
    Tração MD: 30 a 45 MPa

Este exercício mistura regex (módulo 05) com dicionários e tuplas (módulo 03),
decisões (módulo 02) e funções auxiliares (módulo 04).

Tarefa 1: implemente `ler_tolerancias(texto)`, que devolve um dicionário
{chave_do_ensaio: (mínimo, máximo)}.
- Formato A (nominal): "<ensaio>: <nominal> [unidade] ± <pct>%"; aceite também
  "+/-" no lugar de "±". mínimo = nominal * (1 - pct/100) e
  máximo = nominal * (1 + pct/100).
- Formato B (faixa): "<ensaio>: <mínimo> a <máximo> [unidade]".
- Os números vêm no formato brasileiro ("23,0", "0,15").
- Chave do ensaio: minúsculas, sem acento, espaços trocados por "_"
  ("COF estático" vira "cof_estatico").
- Arredonde mínimo e máximo com round(valor, 4).
- Linhas em outro formato (como o título) são ignoradas.

Tarefa 2: implemente `conferir(texto_especificacao, medicoes)`. `medicoes` é um
dicionário {chave: valor medido}. Para cada ensaio DA ESPECIFICAÇÃO, devolva
"OK" (dentro da faixa, limites inclusive), "FORA" ou "SEM MEDIÇÃO" (quando a
chave não está em `medicoes`). Medições de ensaios que não estão na
especificação são ignoradas.

Exemplos:
    >>> spec = "Espessura: 25 µm ± 10%\nCOF estático: 0,15 a 0,30"
    >>> ler_tolerancias(spec)
    {'espessura': (22.5, 27.5), 'cof_estatico': (0.15, 0.3)}
    >>> conferir(spec, {"espessura": 26.1, "tracao_md": 40.0})
    {'espessura': 'OK', 'cof_estatico': 'SEM MEDIÇÃO'}

Dica: duas regex (uma para cada formato) são mais fáceis de testar do que uma
gigante. Escreva funções auxiliares pequenas: uma converte o número brasileiro,
outra cria a chave do ensaio (lembra da aula sobre remover acentos?).

Teste com:  python curso.py testar 05 ex13
"""


# Este exercício usa os módulos re e unicodedata.
# Apague o "# " do começo das duas linhas abaixo para importá-los:
# import re
# import unicodedata


def ler_tolerancias(texto: str) -> dict[str, tuple[float, float]]:
    """Lê a especificação e devolve {ensaio: (mínimo, máximo)}."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def conferir(texto_especificacao: str, medicoes: dict[str, float]) -> dict[str, str]:
    """Para cada ensaio da especificação: "OK", "FORA" ou "SEM MEDIÇÃO"."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
