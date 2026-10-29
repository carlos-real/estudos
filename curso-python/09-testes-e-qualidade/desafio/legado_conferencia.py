"""Script antigo de conferência: funciona, mas ninguém tem coragem de mexer.

É o ponto de partida do desafio do módulo 09. Rode (na pasta do módulo):
    python desafio/legado_conferencia.py
"""

import csv
import sys
from pathlib import Path

L = {
    "A": {"espessura": (19.0, 21.0), "gramatura": (18.2, 19.0), "cof": (0.20, 0.35)},
    "B": {"espessura": (23.75, 26.25), "gramatura": (21.5, 22.5), "cof": (0.20, 0.35)},
    "C": {"espessura": (28.5, 31.5), "cof": (0.25, 0.40)},
    "D": {"espessura": (14.25, 15.75), "gramatura": (13.8, 14.6)},
}


def f(arq):
    d = []
    with open(arq, encoding="utf-8") as a:
        r = csv.reader(a, delimiter=";")
        next(r)
        n = 1
        for x in r:
            n = n + 1
            try:
                v = float(x[3].replace(",", "."))
            except ValueError:
                print("AVISO: linha " + str(n) + " ignorada, valor: " + x[3])
                continue
            d.append([x[0], x[1], x[2], v])
    print("CONFERÊNCIA DE MEDIÇÕES")
    t = {}
    for x in d:
        if x[1] in L and x[2] in L[x[1]]:
            if x[3] >= L[x[1]][x[2]][0] and x[3] <= L[x[1]][x[2]][1]:
                s = "OK"
            else:
                s = "FORA"
            if x[1] not in t:
                t[x[1]] = [0, 0]
            t[x[1]][0] = t[x[1]][0] + 1
            if s == "FORA":
                t[x[1]][1] = t[x[1]][1] + 1
        else:
            s = "SEM REGRA"
        v = format(x[3], ".2f").replace(".", ",")
        print("OP " + x[0] + " | linha " + x[1] + " | " + x[2] + " | " + v + " | " + s)
    print("RESUMO POR LINHA")
    for k in sorted(t):
        p = format(t[k][1] / t[k][0] * 100, ".1f").replace(".", ",")
        print(k + ": " + str(t[k][0]) + " medições, " + str(t[k][1]) + " fora (" + p + "%)")


if len(sys.argv) > 1:
    f(sys.argv[1])
else:
    f(Path(__file__).parent / "dados" / "medicoes_exemplo.csv")
