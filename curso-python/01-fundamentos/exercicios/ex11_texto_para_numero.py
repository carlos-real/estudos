"""
Exercício 01.11 — Texto para número
Nível: ★★☆

Contexto: Valores que vêm de planilhas, e-mails e formulários chegam como TEXTO:
" 25,4 ", "1250.5", "12,5 kg". Antes de fazer qualquer conta, é preciso converter.

Tarefa:
1. `texto_para_numero(texto)` devolve o número (float) contido no texto:
   - ignore maiúsculas/minúsculas e remova a unidade "kg", se houver;
   - remova os espaços do começo e do fim;
   - troque a vírgula decimal por ponto;
   - converta com float().
   Se o texto não for um número (ex.: "abc" ou ""), deixe o float() levantar
   ValueError (não trate o erro).
   Não precisa tratar separador de milhar como "1.250,5" (isso fica para o módulo 05).
2. `somar_pesos(peso1, peso2)` recebe dois textos, converte os dois com a função acima
   e devolve a soma arredondada com round() para 2 casas.

Exemplos:
    >>> texto_para_numero(" 25,4 ")
    25.4
    >>> texto_para_numero("12,5 KG")
    12.5
    >>> somar_pesos("0,1", "0,2")
    0.3

Dica: sem o round(), quanto dá 0.1 + 0.2? Teste no REPL.

Teste com:  python curso.py testar 01 ex11
"""


def texto_para_numero(texto: str) -> float:
    """Converte um texto como ' 12,5 kg' em número (12.5)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")


def somar_pesos(peso1: str, peso2: str) -> float:
    """Soma dois pesos escritos como texto e arredonda em 2 casas."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
