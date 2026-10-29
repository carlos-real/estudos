"""Mostra onde o Python procura módulos (sys.path) e qual Python está rodando.

Rode com:  python exemplos/03_onde_python_procura.py
A saída muda de computador para computador. Compare com o venv ativado e desativado.
"""

import statistics
import sys

print("Python em uso:", sys.executable)
print("Versão:", sys.version.split()[0])
print("\nPastas onde o import procura, em ordem:")
for posicao, pasta in enumerate(sys.path):
    print(f"  {posicao}: {pasta or '(pasta atual)'}")

print("\nO statistics veio de:", statistics.__file__)
print("Módulos já carregados nesta execução:", len(sys.modules))
