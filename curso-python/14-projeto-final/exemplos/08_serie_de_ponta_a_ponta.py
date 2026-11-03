"""A série completa, de ponta a ponta, usando o pacote do projeto-completo.

Roda a CLI do projeto-completo sobre os dados de exemplo deste módulo, em modo
ensaio, gravando os relatórios numa pasta temporária (nada fica no seu disco).

Rode:  python exemplos/08_serie_de_ponta_a_ponta.py
"""

import sys
import tempfile
from pathlib import Path

MODULO = Path(__file__).resolve().parent.parent
# No seu projeto você instalaria o pacote (pip install -e .). Aqui, para o exemplo
# rodar sem instalar nada, colocamos a pasta src no caminho de importação.
sys.path.insert(0, str(MODULO / "projeto-completo" / "src"))

from validador_certificados.cli import main  # noqa: E402

DADOS = MODULO / "dados"

with tempfile.TemporaryDirectory() as pasta:
    codigo = main(
        [
            "--planilha",
            str(DADOS / "planilha_valores.xlsx"),
            "--regras",
            str(DADOS / "regras.db"),
            "--emails",
            str(DADOS / "emails"),
            "--saida",
            pasta,
        ]
    )
    arquivos = sorted(p.suffix for p in Path(pasta).iterdir())
print("código de saída:", codigo)
print("gerados na pasta de saída:", arquivos)
