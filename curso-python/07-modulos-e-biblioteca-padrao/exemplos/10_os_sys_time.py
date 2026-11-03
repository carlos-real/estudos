"""os, sys e time: ambiente, argumentos, código de saída e tempo.

Rode com:  python exemplos/10_os_sys_time.py primeiro segundo
Experimente também definir uma variável de ambiente antes de rodar:
  PowerShell:     $env:LAB_PASTA = "C:\\laboratorio"
  Linux/macOS:    export LAB_PASTA=/home/voce/laboratorio
"""

import os
import sys
import time

print("Sistema:", sys.platform)  # 'win32' no Windows, 'linux', 'darwin' no macOS
print("Argumentos recebidos:", sys.argv)
print("Pasta atual:", os.getcwd())
print("LAB_PASTA =", os.environ.get("LAB_PASTA", "(não definida, usando padrão)"))

inicio = time.perf_counter()
soma = sum(n * n for n in range(1_000_000))
gasto = time.perf_counter() - inicio
print(f"Somar 1 milhão de quadrados ({soma:.2e}) levou {gasto:.3f} s")

time.sleep(0.2)  # robôs usam pausas curtas para esperar telas carregarem
print("Mensagem de erro vai para o stderr ->", end=" ")
print("cuidado!", file=sys.stderr)
sys.exit(0)  # 0 = deu tudo certo; outro número = algo falhou
