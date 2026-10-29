"""
Exercício 12.07 — Organizar laudos em pastas (com modo ensaio)
Nível: ★★☆

Contexto: a pasta "Entrada" acumula centenas de PDFs de laudos com nomes
padronizados, por exemplo  laudo_123456_B_2026-03-10.pdf  (OP, linha e data).
Você vai arrumar tudo em  destino/linha_B/2026-03/laudo_123456_B_2026-03-10.pdf.
Como mover arquivos em lote é perigoso, o padrão é rodar primeiro em ENSAIO.

Tarefa: implemente organizar_laudos(origem, destino, ensaio=True).
- Considere só arquivos (não pastas) da origem cujo nome segue EXATAMENTE o
  padrão  laudo_<6 dígitos>_<linha A a D>_<AAAA-MM-DD>.pdf  (tudo minúsculo,
  linha maiúscula). Os demais arquivos ficam onde estão.
- O destino de cada laudo é  destino / f"linha_{linha}" / "AAAA-MM" / nome.
- Devolva uma lista de tuplas (nome_do_arquivo, caminho_relativo), em ordem
  alfabética pelo nome. caminho_relativo é o destino relativo à pasta destino,
  com barras "/" (ex.: "linha_B/2026-03/laudo_123456_B_2026-03-10.pdf").
- ensaio=True: só devolve o plano. Não cria pastas nem move nada.
- ensaio=False: cria as pastas que faltarem e move os arquivos.
- Nunca sobrescreva: se o arquivo já existir no destino, deixe o original na
  origem e NÃO inclua esse arquivo na lista devolvida.

Exemplos:
    >>> organizar_laudos(Path("entrada"), Path("laudos"))
    [('laudo_123456_B_2026-03-10.pdf', 'linha_B/2026-03/laudo_123456_B_2026-03-10.pdf')]

Dica: re.fullmatch com grupos; shutil.move(origem, destino);
Path.relative_to(...).as_posix() dá o caminho relativo com "/".

Teste com:  python curso.py testar 12 ex07
"""

from pathlib import Path


def organizar_laudos(
    origem: Path, destino: Path, ensaio: bool = True
) -> list[tuple[str, str]]:
    """Planeja (e, fora do ensaio, executa) a organização dos laudos."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
