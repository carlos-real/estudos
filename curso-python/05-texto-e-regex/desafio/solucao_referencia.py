"""Solução de referência — Desafio 05: leitor de e-mails da expedição.

Lê todos os e-mails .txt da pasta dados/emails/ (em UTF-8, UTF-8 com BOM ou
cp1252), extrai os pedidos (OP, NF e peso), aponta as linhas que precisam de
conferência humana e imprime um resumo por e-mail e um resumo geral.

Uso (na pasta curso-python):
    python 05-texto-e-regex/desafio/solucao_referencia.py
"""

import re
import unicodedata
from pathlib import Path

# Pasta deste arquivo -> sobe um nível (o módulo) -> dados/emails.
PASTA_EMAILS = Path(__file__).resolve().parent.parent / "dados" / "emails"
LARGURA = 62

PADRAO_PEDIDO = re.compile(
    r"""
    ^ \s*
    OP   \s* [:-]? \s* (?P<op>\d{6})
    \s* [|;] \s*
    NF   \s* :?    \s* (?P<nf>\d[\d.]*)
    \s* [|;] \s*
    PESO \s* :?    \s* (?P<peso>\d[\d.]*(?:,\d+)?)
    \s* (?:kg)? \s* $
    """,
    re.VERBOSE | re.IGNORECASE,
)
# Uma linha "parece pedido" se fala de OP e também de NF ou de peso.
PADRAO_OP = re.compile(r"\bOP\b", re.IGNORECASE)
PADRAO_NF_OU_PESO = re.compile(r"\b(?:NF|peso)\b", re.IGNORECASE)
# Cabeçalho: "De: ...", "Assunto: ...", "Cliente: ..." no começo da linha.
PADRAO_CABECALHO = re.compile(
    r"^(?P<campo>De|Assunto|Cliente)\s*:\s*(?P<valor>.+?)\s*$", re.MULTILINE | re.IGNORECASE
)
PALAVRAS_MINUSCULAS = {"da", "das", "de", "do", "dos", "e"}


# ---------------------------------------------------------------- texto ----
def decodificar(dados: bytes) -> tuple[str, str]:
    """Devolve (texto, nome do encoding usado)."""
    if dados.startswith(b"\xef\xbb\xbf"):
        return dados.decode("utf-8-sig"), "UTF-8 com BOM"
    texto = dados.decode("utf-8", errors="replace")
    if "�" not in texto:  # sem losango: era UTF-8 mesmo
        return texto, "UTF-8"
    return dados.decode("cp1252"), "cp1252"


def limpar_nome(nome: str) -> str:
    """'  embalagens   DO sul ltda' -> 'Embalagens do Sul Ltda'."""
    palavras = []
    for posicao, palavra in enumerate(nome.split()):
        palavra = palavra.lower()
        if posicao == 0 or palavra not in PALAVRAS_MINUSCULAS:
            palavra = palavra.capitalize()
        palavras.append(palavra)
    return " ".join(palavras)


def chave_de_comparacao(texto: str) -> str:
    """Sem acento, minúsculo e com espaços normalizados (para comparar nomes)."""
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join([c for c in decomposto if not unicodedata.combining(c)])
    return " ".join(sem_acento.casefold().split())


def br_para_float(texto: str) -> float:
    return float(texto.replace(".", "").replace(",", "."))


def float_para_br(valor: float, casas: int = 2) -> str:
    return f"{valor:,.{casas}f}".translate(str.maketrans(",.", ".,"))


def formatar_nf(numero: str) -> str:
    digitos = "".join([c for c in numero if c.isdigit()]).zfill(9)
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:]}"


# ------------------------------------------------------------- e-mails ----
def ler_cabecalho(texto: str) -> dict[str, str]:
    """{'de': ..., 'assunto': ..., 'cliente': ...} (só o que existir)."""
    cabecalho = {}
    for achado in PADRAO_CABECALHO.finditer(texto):
        campo = achado["campo"].lower()
        # setdefault só grava se a chave ainda não existe: vale a 1ª ocorrência.
        cabecalho.setdefault(campo, achado["valor"])
    return cabecalho


def ler_pedidos(texto: str) -> tuple[list[dict], list[str]]:
    """Devolve (pedidos reconhecidos, linhas que parecem pedido mas não casaram)."""
    pedidos = []
    suspeitas = []
    for linha in texto.splitlines():
        achado = PADRAO_PEDIDO.fullmatch(linha)
        if achado:
            pedidos.append(
                {
                    "op": achado["op"],
                    "nf": achado["nf"].replace(".", ""),
                    "peso_kg": br_para_float(achado["peso"]),
                }
            )
        elif PADRAO_OP.search(linha) and PADRAO_NF_OU_PESO.search(linha):
            suspeitas.append(linha.strip())
    return pedidos, suspeitas


def processar_email(caminho: Path) -> dict:
    texto, encoding = decodificar(caminho.read_bytes())
    cabecalho = ler_cabecalho(texto)
    pedidos, suspeitas = ler_pedidos(texto)
    return {
        "arquivo": caminho.name,
        "encoding": encoding,
        "de": cabecalho.get("de", "(sem remetente)"),
        "assunto": cabecalho.get("assunto", "(sem assunto)"),
        "cliente": limpar_nome(cabecalho.get("cliente", "(não informado)")),
        "pedidos": pedidos,
        "suspeitas": suspeitas,
    }


# ----------------------------------------------------------- relatório ----
def linhas_do_resumo(pedidos: list[dict]) -> list[str]:
    if not pedidos:
        return ["Nenhum pedido encontrado."]
    linhas = []
    for pedido in sorted(pedidos, key=lambda p: p["op"]):
        peso = float_para_br(pedido["peso_kg"])
        linhas.append(f"OP {pedido['op']} | NF {formatar_nf(pedido['nf'])} | {peso:>10} kg")
    total = sum(p["peso_kg"] for p in pedidos)
    palavra = "pedido" if len(pedidos) == 1 else "pedidos"
    rotulo = f"Total: {len(pedidos)} {palavra}"
    linhas.append(f"{rotulo:<26} | {float_para_br(total):>10} kg")
    return linhas


def imprimir_email(email: dict) -> None:
    print("=" * LARGURA)
    print(f"E-mail : {email['arquivo']}  ({email['encoding']})")
    print(f"De     : {email['de']}")
    print(f"Assunto: {email['assunto']}")
    print(f"Cliente: {email['cliente']}")
    print("-" * LARGURA)
    for linha in linhas_do_resumo(email["pedidos"]):
        print(linha)
    for linha in email["suspeitas"]:
        print(f"  ! conferir: {linha}")


def ops_repetidas(emails: list[dict]) -> dict[str, list[str]]:
    """{op: [arquivos]} só para as OPs que aparecem em mais de um e-mail."""
    onde = {}
    for email in emails:
        for pedido in email["pedidos"]:
            # setdefault devolve a lista da OP (criando uma vazia na 1ª vez).
            onde.setdefault(pedido["op"], []).append(email["arquivo"])
    return {op: arquivos for op, arquivos in onde.items() if len(arquivos) > 1}


def imprimir_resumo_geral(emails: list[dict]) -> None:
    # Compreensão com dois for: "para cada e-mail, para cada pedido dele".
    todos = [pedido for email in emails for pedido in email["pedidos"]]
    peso_total = sum(p["peso_kg"] for p in todos)
    suspeitas = [(e["arquivo"], linha) for e in emails for linha in e["suspeitas"]]
    clientes = {chave_de_comparacao(e["cliente"]): e["cliente"] for e in emails}

    print("=" * LARGURA)
    print("RESUMO GERAL")
    print(f"E-mails lidos  : {len(emails)}")
    print(f"Clientes       : {', '.join(sorted(clientes.values()))}")
    print(f"Pedidos        : {len(todos)}")
    print(f"Peso total     : {float_para_br(peso_total)} kg")
    print(f"Para conferir  : {len(suspeitas)} linha(s)")
    for arquivo, linha in suspeitas:
        print(f"  - {arquivo}: {linha}")
    repetidas = ops_repetidas(emails)
    if repetidas:
        print("OPs repetidas  :")
        for op, arquivos in sorted(repetidas.items()):
            print(f"  - OP {op} em: {', '.join(arquivos)}")
    else:
        print("OPs repetidas  : nenhuma")


def main() -> None:
    arquivos = sorted(PASTA_EMAILS.glob("*.txt"))
    if not arquivos:
        print(f"Nenhum e-mail .txt em {PASTA_EMAILS}")
        return
    emails = [processar_email(arquivo) for arquivo in arquivos]
    for email in emails:
        imprimir_email(email)
    imprimir_resumo_geral(emails)


# Esta condição é verdadeira só quando você roda o arquivo diretamente
# (python solucao_referencia.py), e não quando ele é importado. Módulo 07.
if __name__ == "__main__":
    main()
