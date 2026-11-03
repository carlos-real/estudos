"""
Exercício 08.06 — Amostra protegida com @property
Nível: ★★☆

Contexto: Alguém digitou -25 na espessura e o certificado saiu com valor negativo.
Com @property, toda atribuição a `amostra.valor` passa por uma validação, e o
código da amostra não pode mais ser trocado depois de criado. Bônus: cada correção
de valor fica registrada (rastreabilidade, coisa que auditoria adora).

Tarefa: complete a classe `Amostra`.
1. `__init__(self, codigo, valor, unidade="µm")`:
   - `codigo` sem espaços nas pontas e em maiúsculas; vazio -> ValueError;
   - guarde o código num atributo "interno" `_codigo`;
   - o valor inicial passa pela MESMA validação do setter (abaixo) e NÃO entra no
     histórico;
   - `unidade` é um atributo comum.
2. `codigo`: property SÓ de leitura (sem setter). `a.codigo = "X"` deve dar
   AttributeError (o Python faz isso sozinho quando não há setter).
3. `valor`: property com setter que valida:
   - bool ou qualquer coisa que não seja int/float -> TypeError;
   - número negativo -> ValueError;
   - guarda como float; o valor ANTERIOR vai para o fim do histórico.
4. `historico`: property que devolve uma TUPLA com os valores anteriores, do mais
   antigo para o mais recente (tupla: quem lê não consegue alterar o original).

Exemplos:
    >>> a = Amostra("am-001", 25.3)
    >>> a.valor = 25.1
    >>> a.valor, a.historico
    (25.1, (25.3,))
    >>> a.valor = -1
    Traceback (most recent call last):
    ...
    ValueError: Valor não pode ser negativo: -1

Dica: True e False são do tipo int no Python! Teste bool ANTES de int/float:
isinstance(novo, bool).

Teste com:  python curso.py testar 08 ex06
"""


class Amostra:
    """Amostra com código fixo e valor validado."""

    def __init__(self, codigo: str, valor: float, unidade: str = "µm") -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def codigo(self) -> str:
        """Código da amostra (só leitura)."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def valor(self) -> float:
        """Valor medido."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @valor.setter
    def valor(self, novo: float) -> None:
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")

    @property
    def historico(self) -> tuple[float, ...]:
        """Valores anteriores (do mais antigo ao mais recente)."""
        # Escreva seu código aqui
        raise NotImplementedError("Implemente este método")
