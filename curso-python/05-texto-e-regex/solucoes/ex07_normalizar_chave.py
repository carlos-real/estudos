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

import re
import unicodedata


def normalizar_chave(texto: str) -> str:
    """Transforma um nome de coluna numa chave: minúsculas, sem acento, com _."""
    # 1) O µ do teclado (U+00B5) precisa ser trocado ANTES da NFKD: ela o
    #    transformaria na letra grega mi (U+03BC), e o replace não acharia mais.
    texto = texto.replace("µ", "u")
    # 2) NFKD separa letra e acento ("ç" -> "c" + cedilha) e ainda simplifica
    #    caracteres "parecidos" ("²" -> "2"). Depois descartamos os combinantes.
    decomposto = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join([c for c in decomposto if not unicodedata.combining(c)])
    # 3) e 4) minúsculas e troca de tudo que não é [a-z0-9] por "_".
    #    O "+" faz uma sequência inteira ("  (" ou " – ") virar UM "_" só.
    com_sublinhado = re.sub(r"[^a-z0-9]+", "_", sem_acento.lower())
    # 5) Parênteses ou espaços nas pontas viram "_" nas pontas: tiramos.
    return com_sublinhado.strip("_")
