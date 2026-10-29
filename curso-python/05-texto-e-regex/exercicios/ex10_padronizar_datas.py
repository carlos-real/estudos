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


# Este exercício usa o módulo re.
# Apague o "# " do começo da linha abaixo para importá-lo:
# import re


def padronizar_datas(texto: str) -> str:
    """Troca datas dd/mm/aaaa (dia e mês com 1 ou 2 dígitos) por aaaa-mm-dd."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
