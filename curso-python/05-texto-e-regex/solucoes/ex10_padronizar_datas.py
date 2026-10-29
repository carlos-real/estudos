"""
Exercício 05.10 — Datas no padrão ISO
Nível: ★★☆

Contexto: Os laudos antigos têm datas como "05/03/2025" e "7/3/2025" no meio do
texto. Para ordenar e filtrar, o sistema novo quer o formato ISO "2025-03-05"
(ano-mês-dia), que ordena certo em qualquer lugar.

Tarefa: implemente `padronizar_datas(texto)`, que troca cada data dia/mês/ano
por ano-mês-dia e devolve o texto novo:
- na entrada, dia e mês têm 1 ou 2 dígitos ("5/3/2025" ou "05/03/2025");
- na saída, dia e mês têm SEMPRE 2 dígitos ("2025-03-05");
- o ano tem 4 dígitos;
- a data não pode estar grudada em outros dígitos: "105/03/2025" e
  "01/02/20251" não são datas;
- não precisa validar se a data existe; o resto do texto não muda.

Exemplos:
    >>> padronizar_datas("Produzido em 05/03/2025, liberado em 7/3/2025.")
    'Produzido em 2025-03-05, liberado em 2025-03-07.'
    >>> padronizar_datas("NF 123/2025 sem data")
    'NF 123/2025 sem data'

Dica: `re.sub` aceita uma FUNÇÃO no lugar do texto de troca (seção 13 da aula).
A função recebe o Match e devolve o texto novo; `zfill` completa os zeros.

Teste com:  python curso.py testar 05 ex10
"""

import re

# \b nas pontas: a data não pode estar grudada em outros dígitos.
PADRAO_DATA = re.compile(r"\b(?P<dia>\d{1,2})/(?P<mes>\d{1,2})/(?P<ano>\d{4})\b")


def _data_iso(achado: re.Match) -> str:
    """Recebe o Match de uma data e devolve o texto no formato ISO."""
    # O "_" no começo do nome é uma convenção: função auxiliar, de uso interno.
    return f"{achado['ano']}-{achado['mes'].zfill(2)}-{achado['dia'].zfill(2)}"


def padronizar_datas(texto: str) -> str:
    """Troca datas dd/mm/aaaa (dia e mês com 1 ou 2 dígitos) por aaaa-mm-dd."""
    # Passamos a FUNÇÃO (sem parênteses!): o re.sub a chama para cada data.
    return PADRAO_DATA.sub(_data_iso, texto)

    # Por que não r"\g<ano>-\g<mes>-\g<dia>"? Funciona só quando dia e mês já
    # têm 2 dígitos: "7/3/2025" viraria "2025-3-7". A troca por texto não sabe
    # completar zeros; a função sabe.
    # Versão com lambda (mesmo resultado):
    #     PADRAO_DATA.sub(
    #         lambda m: f"{m['ano']}-{int(m['mes']):02d}-{int(m['dia']):02d}", texto
    #     )
