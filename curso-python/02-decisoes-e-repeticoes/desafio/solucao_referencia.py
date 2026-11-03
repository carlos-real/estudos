"""Desafio do módulo 02 — Inspetor de série no terminal (solução de referência).

Rode na pasta curso-python:
    python 02-decisoes-e-repeticoes/desafio/solucao_referencia.py

Com MODO_DEMO = True (padrão), o programa usa as respostas de ENTRADAS_DEMO como se
alguém as tivesse digitado, e roda sem parar. Mude para False para digitar de verdade.
"""

MODO_DEMO = True
ENTRADAS_DEMO = [
    "E",  # linha inexistente: o programa pergunta de novo
    "b",
    "abc",  # nominal inválido
    "0",  # nominal precisa ser maior que zero
    "25",
    "25,3",
    "",  # Enter sem digitar: ignorado
    "24,9",
    "xx",  # leitura inválida: aviso
    "26,8",
    "25,1",
    "24,6",
    "25,0",
    "25,2",
    "fim",
]
LIMITE_LEITURAS = 50
SEGUIDAS_PARA_PARAR = 3
PCT_FORA_REPROVA = 0.20  # mais de 20% fora reprova a série


def ler(passo: int, pergunta: str) -> str:
    """Devolve a resposta número `passo`: da lista de demonstração ou do teclado."""
    if not MODO_DEMO:
        return input(pergunta)
    contador = 0
    for resposta in ENTRADAS_DEMO:
        contador += 1
        if contador == passo:
            print(pergunta + resposta)  # mostra como se alguém tivesse digitado
            return resposta
    print(pergunta + "fim")  # acabaram as respostas de demonstração
    return "fim"


def tolerancia_da_linha(linha: str) -> float | None:
    """Tolerância padrão (%) de cada linha, ou None se a linha não existe."""
    match linha:
        case "A" | "B":
            return 5.0
        case "C":
            return 8.0
        case "D":
            return 10.0
        case _:
            return None


def eh_numero(texto: str) -> bool:
    """True se o texto é um número decimal não negativo (aceita vírgula)."""
    limpo = texto.strip().replace(",", ".")
    if not limpo:
        return False
    pontos = 0
    digitos = 0
    for caractere in limpo:
        if caractere == ".":
            pontos += 1
        elif caractere in "0123456789":
            digitos += 1
        else:
            return False
    return pontos <= 1 and digitos >= 1


def para_float(texto: str) -> float:
    """Converte um texto já validado ('25,3') em float."""
    return float(texto.strip().replace(",", "."))


print("=" * 46)
print(f"{'INSPETOR DE SÉRIE — ESPESSURA':^46}")
print("=" * 46)
passo = 0

# 1) Linha de produção: pergunta até receber uma linha conhecida
while True:
    passo += 1
    linha = ler(passo, "Linha (A, B, C ou D): ").strip().upper()
    tolerancia = tolerancia_da_linha(linha)
    if tolerancia is not None:
        break
    print("  Linha desconhecida. Tente de novo.")

# 2) Espessura nominal: pergunta até receber um número maior que zero
while True:
    passo += 1
    texto = ler(passo, "Espessura nominal (µm): ")
    if eh_numero(texto) and para_float(texto) > 0:
        nominal = para_float(texto)
        break
    print("  Digite um número maior que zero, como 25 ou 25,5.")

minimo = nominal - nominal * tolerancia / 100
maximo = nominal + nominal * tolerancia / 100
print(f"Faixa da linha {linha} (±{tolerancia:.0f}%): {minimo:.2f} a {maximo:.2f} µm")
print("Digite as leituras (Enter vazio é ignorado; 'fim' encerra).")

# 3) Leituras até 'fim', até o limite ou até a regra de parada
validas = 0
soma = 0.0
menor = None
maior = None
fora = 0
seguidas = 0
parou_linha = False
while validas < LIMITE_LEITURAS:
    passo += 1
    texto = ler(passo, f"  Leitura {validas + 1}: ").strip()
    if texto.lower() == "fim":
        break
    if texto == "":
        continue
    if not eh_numero(texto):
        print("    Leitura inválida, não contada.")
        continue
    valor = para_float(texto)
    validas += 1
    soma += valor
    if menor is None or valor < menor:
        menor = valor
    if maior is None or valor > maior:
        maior = valor

    if valor < minimo:
        situacao = "FORA (abaixo)"
    elif valor > maximo:
        situacao = "FORA (acima)"
    else:
        situacao = "OK"
    print(f"    {valor:.2f} µm -> {situacao}")

    if situacao == "OK":
        seguidas = 0
    else:
        fora += 1
        seguidas += 1
        if seguidas == SEGUIDAS_PARA_PARAR:
            parou_linha = True
            print(f"    !!! {SEGUIDAS_PARA_PARAR} seguidas fora: PARE A LINHA.")
            break

# 4) Relatório
print("-" * 46)
if validas == 0:
    print("Nenhuma leitura válida. Nada a relatar.")
else:
    media = soma / validas
    pct_fora = fora / validas
    if parou_linha:
        veredito = "REPROVADO (processo fora de controle)"
    elif pct_fora > PCT_FORA_REPROVA:
        veredito = "REPROVADO (muitas leituras fora)"
    elif fora > 0:
        veredito = "CONDICIONAL (avaliar com o líder)"
    else:
        veredito = "APROVADO"
    print(f"{'Leituras válidas':<22}{validas:>24}")
    print(f"{'Média (µm)':<22}{media:>24.2f}")
    print(f"{'Mínima / máxima (µm)':<22}{f'{menor:.2f} / {maior:.2f}':>24}")
    print(f"{'Amplitude (µm)':<22}{maior - menor:>24.2f}")
    print(f"{'Fora da faixa':<22}{f'{fora} ({pct_fora:.0%})':>24}")
    print(f"Veredito: {veredito}")
print("=" * 46)
