"""
Exercício 12.03 — Buscar tolerâncias numa API (SOLUÇÃO)

O ponto principal é a assinatura: `sessao` vem de fora (injeção de
dependência). A função não sabe nem quer saber se a sessão é real ou falsa;
ela só precisa de algo que tenha um método .get() devolvendo uma resposta com
.raise_for_status() e .json(). Isso deixa o código testável sem internet.
"""

import requests

LINHAS_VALIDAS = {"A", "B", "C", "D"}


def buscar_tolerancias(
    sessao: requests.Session, base_url: str, linha: str, timeout: float = 10
) -> dict[str, tuple[float, float]]:
    """Consulta a API e devolve {ensaio: (mínimo, máximo)} da linha."""
    # 1) Validar ANTES de gastar uma chamada de rede ("falhe cedo").
    linha = linha.strip().upper()
    if linha not in LINHAS_VALIDAS:
        raise ValueError(f"Linha inválida: {linha!r}. Use A, B, C ou D.")

    # 2) params= deixa o requests montar "?linha=A" com a codificação certa.
    #    timeout= evita que o robô fique travado para sempre se a API sumir.
    resposta = sessao.get(f"{base_url}/tolerancias", params={"linha": linha}, timeout=timeout)

    # 3) Sem isto, um 404 ou 500 passaria em silêncio e o .json() abaixo
    #    falharia com uma mensagem confusa (ou devolveria lixo).
    resposta.raise_for_status()

    # 4) Transformar o formato da API no formato que o RESTO do nosso
    #    programa quer usar. Assim, se a API mudar, só esta função muda.
    dados = resposta.json()
    return {item["ensaio"]: (item["minimo"], item["maximo"]) for item in dados["itens"]}
