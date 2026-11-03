"""Exemplo 01 — As exceções mais comuns e como reconhecê-las (seção 1).

Rode na pasta curso-python:
    python 06-arquivos-e-erros/exemplos/01_excecoes.py
"""

medicoes = {"espessura": 25.4}
valores = [25.4, 26.1]

# Cada função abaixo provoca um erro diferente. O try/except (seção 2) captura
# e mostra o TIPO e a MENSAGEM, como na última linha de um traceback.
tentativas = [
    ("float('25,4 kg')", lambda: float("25,4 kg")),
    ("'25,4' + 1", lambda: "25,4" + 1),
    ("medicoes['cof']", lambda: medicoes["cof"]),
    ("valores[5]", lambda: valores[5]),
    ("sum([]) / len([])", lambda: sum([]) / len([])),
    ("open('nao_existe.csv')", lambda: open("nao_existe.csv", encoding="utf-8")),
    (
        "'Expedição'.encode('cp1252').decode('utf-8')",
        lambda: "Expedição".encode("cp1252").decode("utf-8"),
    ),
]
for descricao, acao in tentativas:
    try:
        acao()
    except Exception as erro:  # aqui SIM: queremos ver qualquer erro, de propósito
        print(f"{descricao:<46} -> {type(erro).__name__}: {erro}")

print(
    "\nA família: UnicodeDecodeError é um ValueError?",
    issubclass(UnicodeDecodeError, ValueError),
)
print("FileNotFoundError é um OSError?", issubclass(FileNotFoundError, OSError))
