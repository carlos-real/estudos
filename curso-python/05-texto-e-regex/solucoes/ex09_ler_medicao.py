"""
Exercício 05.09 — Ler uma linha de medição
Nível: ★★☆

Contexto: O equipamento de ensaio exporta um texto com uma medição por linha:
"Espessura: 25,4 µm", "Gramatura = 23,10 g/m²", "COF estático: 0,21". Você
quer cada linha como um dicionário.

Tarefa: implemente `ler_medicao(linha)`. O formato da linha é:
    <ensaio> <separador> <valor> <unidade opcional>
- ensaio: o texto antes do primeiro ":" ou "=", sem espaços nas pontas; não
  pode ser vazio;
- separador: ":" ou "=";
- valor: número no formato brasileiro (dígitos, pontos de milhar opcionais,
  vírgula decimal opcional), podendo ter "-" na frente;
- unidade: tudo o que vem depois do número, sem espaços nas pontas (pode ser "").
Devolva {"ensaio": str, "valor": float, "unidade": str}, ou None se a linha
não estiver nesse formato.

Exemplos:
    >>> ler_medicao("Espessura: 25,4 µm")
    {'ensaio': 'Espessura', 'valor': 25.4, 'unidade': 'µm'}
    >>> ler_medicao("  Selagem = 1.250,5 N/15 mm ")
    {'ensaio': 'Selagem', 'valor': 1250.5, 'unidade': 'N/15 mm'}
    >>> ler_medicao("COF estático: 0,21")
    {'ensaio': 'COF estático', 'valor': 0.21, 'unidade': ''}
    >>> print(ler_medicao("Observação: COF liberado"))
    None

Dica: `re.fullmatch` com grupos nomeados. Para o ensaio, pense em "tudo que não
é : nem =". Teste cada grupo separado no REPL antes de juntar.

Teste com:  python curso.py testar 05 ex09
"""

import re

PADRAO_MEDICAO = re.compile(
    r"""
    \s*
    (?P<ensaio>[^:=]*[^:=\s])        # tudo que não é : nem =, terminando sem espaço
    \s* [:=] \s*                     # o separador
    (?P<valor>-?\d[\d.]*(?:,\d+)?)   # -1.250,5 : sinal, dígitos, milhar, decimais
    \s*
    (?P<unidade>.*?)                 # o resto (preguiçoso, para sobrar os espaços)
    \s*
    """,
    re.VERBOSE,
)


def ler_medicao(linha: str) -> dict | None:
    """Lê "Ensaio: valor unidade" e devolve um dicionário (ou None)."""
    achado = PADRAO_MEDICAO.fullmatch(linha)
    if achado is None:  # retorno antecipado (módulo 04): caso ruim sai logo
        return None
    valor = float(achado["valor"].replace(".", "").replace(",", "."))
    return {"ensaio": achado["ensaio"], "valor": valor, "unidade": achado["unidade"]}

    # Por que o ensaio é [^:=]*[^:=\s] e não [^:=]+ ? Com [^:=]+, o grupo
    # engoliria o espaço antes do ":" ("Selagem "), e teríamos de dar strip()
    # depois. As duas formas funcionam; esta deixa o grupo já limpo.
    # E por que a unidade é preguiçosa (.*?)? Com .* gulosa, ela pegaria também
    # os espaços do fim da linha, e o \s* final não teria o que casar.
