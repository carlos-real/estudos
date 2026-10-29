"""
Solução — Exercício 04.08 — Filtros com **kwargs

Ideia central: **nome recolhe os argumentos NOMEADOS que sobraram num
dicionário. Na chamada, o nome do argumento vira a chave.
"""


def criar_amostra(op: str, linha: str, **medicoes: float) -> dict:
    """Monta o dicionário da amostra com as medições recebidas por nome."""
    # medicoes já é um dicionário: {"espessura": 50.2, "cof": 0.22}.
    # {**medicoes} "despeja" esses pares no dicionário novo, na ordem recebida.
    return {"op": op, "linha": linha.strip().upper(), **medicoes}


def filtrar_registros(registros: list[dict], **criterios) -> list[dict]:
    """Devolve os registros que atendem a TODOS os critérios coluna=valor."""
    # Para cada registro, conferimos todos os pares (coluna, valor) dos
    # critérios. Sem critérios, all() de nada é True: todos passam.
    return [
        registro
        for registro in registros
        if all(registro.get(coluna) == valor for coluna, valor in criterios.items())
    ]

    # Versão com laços (mesmo resultado):
    #     resultado = []
    #     for registro in registros:
    #         passou = True
    #         for coluna, valor in criterios.items():
    #             if registro.get(coluna) != valor:
    #                 passou = False
    #                 break
    #         if passou:
    #             resultado.append(registro)
    #     return resultado
