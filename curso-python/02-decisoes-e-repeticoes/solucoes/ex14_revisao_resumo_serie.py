"""
Exercício 02.14 — Revisão: resumo de uma série vinda da planilha
Nível: ★★★

Revisão: este exercício mistura o módulo 02 (laços, validação, contadores, máximo e
mínimo, if/elif) com o módulo 01 (strip, replace, float(), f-strings com :.2f).

Contexto: As leituras de espessura de uma série chegam da planilha como TEXTO, do jeito
que o operador digitou: "24,8", " 25.1 ", células vazias e, às vezes, lixo como "erro"
ou "25,4,1". O sistema precisa resumir a série sem quebrar.

Tarefa:
1. `eh_numero(texto)` devolve True se o texto representa um número decimal
   não negativo. Regras, depois de tirar os espaços das pontas e trocar "," por ".":
   - não pode ficar vazio;
   - só pode ter dígitos (0 a 9) e no máximo UM ponto;
   - precisa ter pelo menos um dígito.
   Não use try/except (módulo 06): verifique caractere por caractere.
2. `resumo_serie(leituras, minimo, maximo)` percorre as leituras e:
   - ignora as vazias (só espaços também conta como vazia);
   - conta como inválidas as que não passam em eh_numero;
   - converte as válidas para float e calcula: quantidade, média, mínimo, máximo e
     quantas estão fora da faixa [minimo, maximo] (limites inclusivos).
   Devolve o texto (valores com 2 casas):
       válidas=3 | inválidas=1 | média=25.97 | mín=24.80 | máx=28.00 | fora=1 | REPROVADO
   Status: "REPROVADO" se houver alguma fora; senão "REVISAR" se houver alguma
   inválida; senão "APROVADO".
   Se não houver nenhuma válida, devolva: Nenhuma leitura válida (inválidas=N)

Exemplos:
    >>> eh_numero(" 25,4 ")
    True
    >>> eh_numero("25,4,1")
    False
    >>> resumo_serie(["24,8", "25,3", "25,1"], 23, 27)
    'válidas=3 | inválidas=0 | média=25.07 | mín=24.80 | máx=25.30 | fora=0 | APROVADO'

Dica: resolva eh_numero primeiro e teste no REPL com vários textos. Em resumo_serie,
um único laço pode atualizar todos os contadores e acumuladores.

Teste com:  python curso.py testar 02 ex14
"""


def eh_numero(texto: str) -> bool:
    """Diz se o texto é um número decimal não negativo (aceita vírgula)."""
    limpo = texto.strip().replace(",", ".")
    if not limpo:  # string vazia é falsy
        return False
    pontos = 0
    digitos = 0
    for caractere in limpo:
        if caractere == ".":
            pontos += 1
        elif caractere in "0123456789":
            digitos += 1
        else:
            return False  # achou algo proibido ("-", "e", letra...): nem precisa continuar
    # Depois de olhar todos os caracteres, conferimos as contagens.
    return pontos <= 1 and digitos >= 1


def resumo_serie(leituras: list[str], minimo: float, maximo: float) -> str:
    """Devolve o resumo da série de leituras em uma linha de texto."""
    validas = 0
    invalidas = 0
    soma = 0.0
    menor = None
    maior = None
    fora = 0
    for leitura in leituras:
        texto = leitura.strip()
        if texto == "":
            continue  # célula vazia: não conta para nada
        if not eh_numero(texto):
            invalidas += 1
            continue
        valor = float(texto.replace(",", "."))  # seguro: eh_numero já garantiu
        validas += 1
        soma += valor
        if menor is None or valor < menor:
            menor = valor
        if maior is None or valor > maior:
            maior = valor
        if valor < minimo or valor > maximo:
            fora += 1

    if validas == 0:
        return f"Nenhuma leitura válida (inválidas={invalidas})"

    if fora > 0:
        status = "REPROVADO"
    elif invalidas > 0:
        status = "REVISAR"
    else:
        status = "APROVADO"

    media = soma / validas
    return (
        f"válidas={validas} | inválidas={invalidas} | média={media:.2f} | "
        f"mín={menor:.2f} | máx={maior:.2f} | fora={fora} | {status}"
    )
