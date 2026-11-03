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

import re  # noqa: F401 (você vai usar)

LINHAS_VALIDAS = "ABCD"


def normalizar_linha(texto: object) -> str | None:
    """Letra da linha ("Linha A", " a " -> "A") ou None se não for reconhecida."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def conferir_linha(nome_aba: str, linha_informada: object) -> str | None:
    """None se a linha informada bate com a aba; senão, o motivo da pendência."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
