"""
Exercício 12.06 — Nunca sobrescrever um arquivo (SOLUÇÃO)
"""

from pathlib import Path


def nome_disponivel(pasta: Path, nome: str) -> Path:
    """Primeiro caminho livre para `nome` dentro de `pasta`."""
    candidato = pasta / nome
    if not candidato.exists():
        return candidato  # caso mais comum: retorno antecipado

    # Path(nome) separa as partes: "laudo.final.pdf" -> stem "laudo.final",
    # suffix ".pdf". Só a ÚLTIMA extensão é considerada, que é o que queremos.
    base = Path(nome)
    numero = 2
    # while: não sabemos quantas cópias já existem, então repetimos até achar
    # um nome livre. O laço sempre termina, porque a pasta tem arquivos finitos.
    while True:
        candidato = pasta / f"{base.stem} ({numero}){base.suffix}"
        if not candidato.exists():
            return candidato
        numero += 1

    # Cuidado no mundo real: entre "escolher o nome" e "gravar" outro programa
    # pode criar o mesmo arquivo. Para robôs simples isso é raro; se precisar
    # de garantia, abra o arquivo com open(caminho, "xb"), que FALHA se ele já
    # existir (FileExistsError) em vez de sobrescrever.
