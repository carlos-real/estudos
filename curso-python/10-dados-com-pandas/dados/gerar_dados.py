"""Gera os arquivos de dados usados na aula do módulo 10.

Os dados são FICTÍCIOS, mas imitam o que aparece num laboratório de qualidade de
embalagens flexíveis: medições de bobinas, OPs exportadas do ERP, especificações
de produto e a planilha de valores com uma aba por linha de produção.

Uso (na pasta curso-python):
    python 10-dados-com-pandas/dados/gerar_dados.py

O resultado é sempre o mesmo (a semente do sorteio é fixa). Se apagar algum
arquivo da pasta dados/, rode de novo para recriá-lo.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

PASTA = Path(__file__).resolve().parent
ARQUIVO_SALARIOS = PASTA.parent.parent.parent / "arquivos" / "salaries.csv"

# produto: (descrição, linha, espessura nominal µm, tolerância %, gramatura nominal, COF máx.)
PRODUTOS = {
    "PE-50": ("Filme PE alta barreira 50 µm", "A", 50.0, 10.0, 46.0, 0.30),
    "PE-70": ("Filme PE termoencolhível 70 µm", "A", 70.0, 10.0, 64.4, 0.30),
    "BOPP-20": ("BOPP transparente 20 µm", "B", 20.0, 8.0, 18.1, 0.35),
    "PET-12": ("PET metalizado 12 µm", "C", 12.0, 5.0, 16.7, 0.40),
    "LAM-62": ("Laminado PET/PE 62 µm", "D", 62.0, 7.0, 62.7, 0.25),
}

CLIENTES = [
    "Alimentos Boa Safra Ltda",
    "Laticínios Serra Azul",
    "Café São Bento",
    "Higiene Bem-Estar S.A.",
    "Biscoitos Pão de Mel",
]

# (op, produto, data de emissão, índice do cliente)
OPS = [
    ("004512", "PE-50", date(2026, 7, 2), 0),
    ("004513", "BOPP-20", date(2026, 7, 3), 3),
    ("004520", "PET-12", date(2026, 7, 8), 2),
    ("004521", "LAM-62", date(2026, 7, 10), 2),
    ("004530", "PE-70", date(2026, 7, 15), 1),
    ("004533", "BOPP-20", date(2026, 7, 21), 4),
    ("004540", "PE-50", date(2026, 7, 28), 0),
    ("004547", "LAM-62", date(2026, 8, 4), 1),
    ("004551", "PET-12", date(2026, 8, 6), 2),
    ("004558", "BOPP-20", date(2026, 8, 12), 3),
    ("004562", "PE-50", date(2026, 8, 18), 4),
    ("004566", "LAM-62", date(2026, 8, 25), 0),
    ("004570", "PE-70", date(2026, 9, 1), 1),
    ("004574", "PET-12", date(2026, 9, 3), 2),
    ("004579", "BOPP-20", date(2026, 9, 9), 4),
    ("004583", "PE-90", date(2026, 9, 15), 3),  # produto novo: ainda sem especificação
    ("004588", "LAM-62", date(2026, 9, 22), 1),
]
OP_SEM_CADASTRO = "004599"  # aparece nas medições, mas não no ERP (para o merge)


def br(valor: float, casas: int = 1) -> str:
    """Formata um número no padrão brasileiro: 1250.5 -> '1.250,5'."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_medicoes(sorteio: random.Random) -> list[dict]:
    medicoes = []
    for op, produto, emissao, _ in [*OPS, (OP_SEM_CADASTRO, "PE-50", date(2026, 9, 25), 0)]:
        linha = PRODUTOS[produto][1] if produto in PRODUTOS else "A"
        nominal = PRODUTOS[produto][2] if produto in PRODUTOS else 90.0
        gram_nominal = PRODUTOS[produto][4] if produto in PRODUTOS else 82.8
        cof_max = PRODUTOS[produto][5] if produto in PRODUTOS else 0.30
        for numero in range(1, sorteio.randint(3, 5) + 1):
            espessura = round(sorteio.gauss(nominal, nominal * 0.045), 1)
            gramatura = round(gram_nominal * espessura / nominal + sorteio.gauss(0, 0.4), 1)
            cof = round(sorteio.gauss(cof_max - 0.06, 0.035), 2)
            observacao = "COF: liberado" if cof > cof_max and sorteio.random() < 0.5 else ""
            medicoes.append(
                {
                    "data": emissao + timedelta(days=sorteio.randint(1, 3)),
                    "op": op,
                    "linha": linha,
                    "produto": produto,
                    "bobina": f"{op}-{numero:02d}",
                    "espessura_um": espessura,
                    "gramatura_gm2": gramatura,
                    "cof": cof,
                    "peso_kg": round(sorteio.uniform(780, 1650), 1),
                    "observacao": observacao,
                }
            )
    return medicoes


def gravar_medicoes_csv(medicoes: list[dict]) -> None:
    """CSV no padrão do Excel brasileiro: ponto e vírgula, vírgula decimal, UTF-8 com BOM."""
    caminho = PASTA / "medicoes.csv"
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(list(medicoes[0]))
        for m in medicoes:
            escritor.writerow(
                [
                    m["data"].strftime("%d/%m/%Y"),
                    m["op"],
                    m["linha"],
                    m["produto"],
                    m["bobina"],
                    br(m["espessura_um"]),
                    br(m["gramatura_gm2"]),
                    br(m["cof"], 2),
                    br(m["peso_kg"]),
                    m["observacao"],
                ]
            )


def gravar_medicoes_sujas_csv() -> None:
    """Um arquivo pequeno com os defeitos típicos de planilha digitada à mão."""
    linhas = [
        ["data", "op", "linha", "bobina", "espessura_um", "peso_kg", "operador"],
        ["01/09/2026", "004570", "A", "004570-01", "71,2", "1.120,5", "Marcos"],
        ["01/09/2026", "004570", " a", "004570-02", "69,8", "1.098,0", "marcos "],
        ["01/09/2026", "004570", "A", "004570-02", "69,8", "1.098,0", "marcos "],
        ["02/09/2026", "004570", "A ", "004570-03", "n/d", "1.205,3", "Marcos"],
        ["04/09/2026", "004574", "c", "004574-01", "12,3", "845,0", "Júlia"],
        ["04/09/2026", "004574", "C", "004574-02", "", "910,2", "JÚLIA"],
        ["04/09/2026", "004574", "C", "004574-03", "11,9", "", "Júlia"],
        ["", "004574", "C", "004574-04", "12,1", "877,7", "Júlia"],
        ["10/09/2026", "004579", "b", "004579-01", "20,4", "1.310,0", "Ana"],
        ["10/09/2026", "004579", "B", "004579-02", "19,7 ", "1.288,4", "ana"],
    ]
    caminho = PASTA / "medicoes_sujas.csv"
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        csv.writer(arquivo, delimiter=";").writerows(linhas)


def gravar_ops_protheus_csv(sorteio: random.Random) -> None:
    """Exportação do ERP: separador ';' e encoding cp1252 (padrão antigo do Windows)."""
    caminho = PASTA / "ops_protheus.csv"
    with caminho.open("w", encoding="cp1252", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["op", "cliente", "produto", "emissao", "quantidade_kg"])
        for op, produto, emissao, cliente in OPS:
            quantidade = sorteio.randrange(2_000, 6_001, 250)
            escritor.writerow(
                [op, CLIENTES[cliente], produto, emissao.strftime("%d/%m/%Y"), br(quantidade)]
            )


def gravar_especificacoes_csv() -> None:
    caminho = PASTA / "especificacoes.csv"
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(
            ["produto", "descricao", "espessura_nominal", "tolerancia_pct", "gramatura_nominal",
             "cof_max"]
        )  # fmt: skip
        for produto, (descricao, _, nominal, tol, gram, cof) in PRODUTOS.items():
            escritor.writerow([produto, descricao, br(nominal), br(tol), br(gram), br(cof, 2)])


def gravar_planilha_linhas(medicoes: list[dict]) -> None:
    """A 'planilha de valores' do laboratório: uma aba por linha de produção.

    Como muita planilha feita à mão, ela tem um título na linha 1 e o cabeçalho
    só na linha 2. Os nomes das colunas têm acento e unidade.
    """
    cabecalho = [
        "OP",
        "Bobina",
        "Data",
        "Espessura (µm)",
        "Gramatura (g/m²)",
        "COF",
        "Peso (kg)",
        "Observação",
    ]
    livro = Workbook()
    livro.remove(livro.active)
    for linha in "ABCD":
        aba = livro.create_sheet(f"Linha {linha}")
        aba["A1"] = f"Controle de qualidade — Linha {linha}"
        aba["A1"].font = Font(bold=True, size=13)
        aba.append(cabecalho)
        for celula in aba[2]:
            celula.font = Font(bold=True, color="FFFFFF")
            celula.fill = PatternFill("solid", fgColor="1F4E78")
            celula.alignment = Alignment(horizontal="center")
        for m in medicoes:
            if m["linha"] != linha:
                continue
            aba.append(
                [
                    m["op"],
                    m["bobina"],
                    m["data"],
                    m["espessura_um"],
                    m["gramatura_gm2"],
                    m["cof"],
                    m["peso_kg"],
                    m["observacao"] or None,
                ]
            )
        for linha_planilha in aba.iter_rows(min_row=3, min_col=3, max_col=3):
            linha_planilha[0].number_format = "DD/MM/YYYY"
        for coluna, largura in zip("ABCDEFGH", [10, 12, 12, 15, 17, 8, 11, 16]):
            aba.column_dimensions[coluna].width = largura
        aba.freeze_panes = "A3"
    livro.save(PASTA / "planilha_linhas.xlsx")


def gravar_amostra_salarios() -> None:
    """Amostra pequena do arquivo de salários, para estudar sem o arquivo grande."""
    if not ARQUIVO_SALARIOS.exists():
        print(f"(pulei a amostra de salários: {ARQUIVO_SALARIOS} não existe)")
        return
    import pandas as pd

    df = pd.read_csv(ARQUIVO_SALARIOS)
    amostra = df.sample(n=600, random_state=42).sort_index()
    amostra.to_csv(PASTA / "salarios_amostra.csv", index=False)


def main() -> None:
    sorteio = random.Random(2026)
    medicoes = gerar_medicoes(sorteio)
    gravar_medicoes_csv(medicoes)
    gravar_medicoes_sujas_csv()
    gravar_ops_protheus_csv(sorteio)
    gravar_especificacoes_csv()
    gravar_planilha_linhas(medicoes)
    gravar_amostra_salarios()
    for arquivo in sorted(PASTA.iterdir()):
        if arquivo.suffix in {".csv", ".xlsx"}:
            print(f"{arquivo.name:<24} {arquivo.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
