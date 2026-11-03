"""
Exercício 12.02 — Montar a URL de uma consulta
Nível: ★☆☆

Contexto: o robô chama várias rotas da mesma API. Juntar pedaços de URL "na
mão" gera erros clássicos: barra dobrada (api//medicoes), barra faltando
(apimedicoes) e acentos que quebram o endereço.

Tarefa: implemente montar_url(base, caminho, params=None).
- Junte base e caminho com exatamente UMA barra entre eles, não importa se a
  base termina com "/" ou se o caminho começa com "/".
- params é opcional. Ignore as chaves cujo valor é None. As que sobrarem
  viram a "query string" (?chave=valor&...) na ordem do dicionário,
  codificadas com urllib.parse.urlencode (espaço vira "+", acentos viram %XX).
- Se não sobrar nenhum parâmetro, a URL não leva "?".

Exemplos:
    >>> montar_url("https://api.lab.local/", "/medicoes", {"linha": "A", "limite": 10})
    'https://api.lab.local/medicoes?linha=A&limite=10'
    >>> montar_url("https://api.lab.local", "tolerancias")
    'https://api.lab.local/tolerancias'
    >>> montar_url("https://api.lab.local", "busca", {"texto": "filme PE", "op": None})
    'https://api.lab.local/busca?texto=filme+PE'

Dica: str.rstrip("/") e str.lstrip("/") removem barras só de uma ponta.
Para codificar: from urllib.parse import urlencode.

Teste com:  python curso.py testar 12 ex02
"""


def montar_url(base: str, caminho: str, params: dict | None = None) -> str:
    """Junta base + caminho e acrescenta a query string (sem valores None)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
