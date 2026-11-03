"""
Exercício 05.07 — Normalizar nome de coluna
Nível: ★★☆

Contexto: Cada setor batiza as colunas da planilha de um jeito:
"Gramatura (g/m²)", "COEFICIENTE DE ATRITO – Estático". Para juntar planilhas,
você transforma cada nome numa "chave" simples, como um nome de variável:
gramatura_g_m2.

Tarefa: implemente `normalizar_chave(texto)`, seguindo NESTA ORDEM:
1. troque o símbolo de micro "µ" por "u";
2. normalize com NFKD e remova os caracteres combinantes (os acentos);
   assim "ç" vira "c" e "²" vira "2";
3. passe tudo para minúsculas;
4. troque cada sequência de caracteres que NÃO seja letra de a a z nem dígito
   de 0 a 9 por um único "_";
5. tire os "_" das pontas.

Exemplos:
    >>> normalizar_chave("Gramatura (g/m²)")
    'gramatura_g_m2'
    >>> normalizar_chave("  Coeficiente de Atrito – Estático ")
    'coeficiente_de_atrito_estatico'
    >>> normalizar_chave("Espessura (µm)")
    'espessura_um'
    >>> normalizar_chave("Tração MD (N/15mm)")
    'tracao_md_n_15mm'

Dica: o passo 4 é um `re.sub` com a classe `[^a-z0-9]+`. Você vai precisar de
`import re` e `import unicodedata` no topo do arquivo.

Teste com:  python curso.py testar 05 ex07
"""


# Este exercício usa os módulos re e unicodedata.
# Apague o "# " do começo das duas linhas abaixo para importá-los:
# import re
# import unicodedata


def normalizar_chave(texto: str) -> str:
    """Transforma um nome de coluna numa chave: minúsculas, sem acento, com _."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
