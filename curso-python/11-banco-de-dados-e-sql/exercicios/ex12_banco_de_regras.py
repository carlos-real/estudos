"""
Exercício 11.12 — O banco de regras do projeto final
Nível: ★★★

Contexto: no Validador de Certificados (módulo 14), as regras ficam num banco
SQLite com três tabelas (veja dados/regras.sql e a seção da aula):
    linha(codigo, descricao)
    especificacao(titulo, texto, linha)  -- linha preenchida = PADRÃO da linha;
                                         -- linha NULL = especificação de cliente
    tolerancia(titulo, caracteristica, tipo, minimo, maximo, percentual)
                                         -- tipo 'fixa' usa minimo/maximo;
                                         -- tipo 'nominal' usa percentual
A OP traz a linha e, às vezes, o título de uma especificação de cliente. As
tolerâncias que valem são as do padrão da linha, trocadas pelas da
especificação do cliente nas características que ela define.

Tarefa: implemente três funções.
  1. especificacao_da_op(conexao, linha, titulo=None): devolve (titulo, texto).
     Título vazio ou None -> o padrão da linha. Título informado -> essa
     especificação, comparando sem diferenciar maiúsculas e ignorando espaços
     nas pontas (" esp-0533 " acha "ESP-0533"). Não encontrou (título
     desconhecido ou linha sem padrão) -> LookupError.
  2. tolerancias_efetivas(conexao, linha, titulo=None): dicionário
     {caracteristica: {"tipo", "minimo", "maximo", "percentual", "origem"}}, em
     que "origem" é o título de onde a tolerância veio. Começa pelas do padrão
     da linha e sobrescreve com as da especificação do cliente (se houver).
     Erros como na função 1.
  3. limites(tolerancia, nominal=None): devolve (minimo, maximo).
     tipo 'fixa' -> (minimo, maximo) da própria tolerância (podem ser None).
     tipo 'nominal' -> nominal ± percentual%, arredondado em 4 casas; nominal
     None ou <= 0 -> ValueError.

Exemplos:
    >>> especificacao_da_op(conexao, "A")
    ('PADRAO-A', 'Padrão da linha A (filmes PE monocamada).')
    >>> efetivas = tolerancias_efetivas(conexao, "A", "ESP-0533")
    >>> efetivas["espessura"]
    {'tipo': 'nominal', 'minimo': None, 'maximo': None, 'percentual': 5.0,
     'origem': 'ESP-0533'}
    >>> limites(efetivas["espessura"], nominal=60)
    (57.0, 63.0)
    >>> limites(efetivas["cof"])
    (0.15, 0.35)

Dica: UPPER(TRIM(titulo)) = UPPER(TRIM(?)). Para as efetivas, duas consultas
(padrão e cliente) e um dicionário que a segunda atualiza já resolvem; a aula
mostra também a versão numa consulta só, com UNION ALL.

Teste com:  python curso.py testar 11 ex12
"""

import sqlite3


def especificacao_da_op(
    conexao: sqlite3.Connection, linha: str, titulo: str | None = None
) -> tuple[str, str]:
    """(titulo, texto) da especificação que vale para a OP."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def tolerancias_efetivas(
    conexao: sqlite3.Connection, linha: str, titulo: str | None = None
) -> dict[str, dict]:
    """Tolerâncias do padrão da linha, sobrescritas pelas da especificação."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def limites(
    tolerancia: dict, nominal: float | None = None
) -> tuple[float | None, float | None]:
    """(minimo, maximo) de uma tolerância fixa ou nominal ± %."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
