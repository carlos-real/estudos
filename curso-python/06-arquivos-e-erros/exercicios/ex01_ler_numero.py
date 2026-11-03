"""
Exercício 06.01 — Converter sem quebrar
Nível: ★☆☆

Contexto: Uma coluna da planilha deveria ter só números, mas aparecem células
vazias, "#N/D" do Excel e "25,4 kg" digitado à mão. Um único valor ruim não
pode derrubar o programa inteiro.

Tarefa: implemente `ler_numero(texto, padrao=None)`:
- converta o número no formato brasileiro ("1.250,5", "25,4", "-0,5", "980")
  para float;
- se a conversão der ValueError, devolva `padrao` em vez de deixar o erro
  estourar;
- use try/except (não tente validar o texto com if).

Exemplos:
    >>> ler_numero("1.250,5")
    1250.5
    >>> print(ler_numero("#N/D"))
    None
    >>> ler_numero("", padrao=0.0)
    0.0

Dica: a conversão é a do módulo 05. Coloque dentro do try só a linha que pode
dar erro.

Teste com:  python curso.py testar 06 ex01
"""


def ler_numero(texto: str, padrao: float | None = None) -> float | None:
    """Converte "1.250,5" em 1250.5; se não der, devolve `padrao`."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
