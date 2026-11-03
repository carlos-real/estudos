"""
Exercício 14.08 — A linha digitada bate com a aba?
Nível: ★☆☆

Contexto: Cada aba da planilha é de uma linha de produção, mas cada OP também tem a
coluna "Linha". Quando alguém copia uma OP para a aba errada, as duas discordam. O
sistema não pode escolher uma delas: o padrão da linha muda as tolerâncias. Vira
pendência.

Tarefa: implemente duas funções.
1. `normalizar_linha(texto)`: aceita "A", " a ", "Linha A", "LINHA  b" e devolve a
   letra maiúscula ("A".."D"). Qualquer outra coisa ("Linha E", "AB", "", None,
   "Resumo") devolve None.
2. `conferir_linha(nome_aba, linha_informada)` devolve None se estiver tudo certo, ou:
   - "aba '<nome_aba>' não corresponde a uma linha de produção" se a aba não for
     de linha;
   - "linha não informada ou inválida: '<texto>'" se a linha informada não for
     reconhecida (None conta como texto vazio: '');
   - "linha informada <X> diferente da aba <nome_aba>" se as letras forem diferentes.

Exemplos:
    >>> normalizar_linha(" linha  b ")
    'B'
    >>> print(normalizar_linha("Linha E"))
    None
    >>> print(conferir_linha("Linha B", "b"))
    None
    >>> conferir_linha("Linha B", "C")
    'linha informada C diferente da aba Linha B'

Dica: depois de strip() e upper(), re.fullmatch(r"(?:LINHA\\s*)?([A-D])", texto)
resolve normalizar_linha: o grupo 1 é a letra. Para as aspas da mensagem, {texto!r}.

Teste com:  python curso.py testar 14 ex08
"""

import re

LINHAS_VALIDAS = "ABCD"


def normalizar_linha(texto: object) -> str | None:
    """Letra da linha ("Linha A", " a " -> "A") ou None se não for reconhecida."""
    # Sem regex também dá: tirar o prefixo com removeprefix("LINHA"), strip() e
    # conferir se sobrou uma letra de LINHAS_VALIDAS. A regex deixa a regra num
    # lugar só e fácil de testar.
    if texto is None:
        return None
    # fullmatch exige que o texto INTEIRO case: "AB" e "Linha A2" ficam de fora.
    # (?:...) é um grupo que não captura: só agrupa o "LINHA" opcional.
    achado = re.fullmatch(r"(?:LINHA\s*)?([A-Z])", str(texto).strip().upper())
    if achado and achado.group(1) in LINHAS_VALIDAS:
        return achado.group(1)
    return None


def conferir_linha(nome_aba: str, linha_informada: object) -> str | None:
    """None se a linha informada bate com a aba; senão, o motivo da pendência."""
    da_aba = normalizar_linha(nome_aba)
    if da_aba is None:
        return f"aba {nome_aba!r} não corresponde a uma linha de produção"
    informada = normalizar_linha(linha_informada)
    if informada is None:
        # Célula vazia também é pendência: "nunca chutar" vale para os dois lados.
        texto = "" if linha_informada is None else str(linha_informada)
        return f"linha não informada ou inválida: {texto!r}"
    if informada != da_aba:
        return f"linha informada {informada} diferente da aba {nome_aba}"
    return None
