"""Permite que test_solucao_referencia.py faça `import solucao_referencia`."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
