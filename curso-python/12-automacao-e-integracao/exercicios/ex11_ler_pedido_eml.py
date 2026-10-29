"""
Exercício 12.11 — Ler o pedido da expedição num arquivo .eml
Nível: ★★☆

Contexto: os pedidos de certificado chegam por e-mail. Salvos como .eml (ou
exportados por uma regra/fluxo do Outlook), eles viram BYTES que o Python lê.
Alguns vêm em texto puro, outros só em HTML, e alguns vêm incompletos.

Tarefa: implemente ler_pedido(conteudo), onde `conteudo` são os bytes do .eml.
- Leia com BytesParser(policy=policy.default).parsebytes(conteudo).
- Pegue o corpo com msg.get_body(preferencelist=("plain", "html")). Se o
  corpo escolhido for HTML (get_content_type() == "text/html"), troque cada
  tag <...> por um espaço antes de procurar os campos.
- Procure no texto (maiúsculas ou minúsculas):
    "OP: 123456"      -> op = "123456"   (exatamente 6 dígitos)
    "NF: 98765"       -> nf = "98765"    (1 ou mais dígitos)
    "Peso: 1.250,5 kg" -> peso_kg = 1250.5 (formato brasileiro -> float)
  Os dois-pontos são opcionais e pode haver espaços entre as partes.
- Devolva o dicionário:
    {"remetente": <só o endereço, sem o nome>, "assunto": <assunto>,
     "op": ..., "nf": ..., "peso_kg": ...}
- Se faltar OP, NF ou peso, levante ValueError com a mensagem
  "Campo não encontrado: OP" (ou NF, ou peso), checando nessa ordem.

Exemplos (o arquivo dados/emails/pedido_001.eml):
    >>> ler_pedido(Path("dados/emails/pedido_001.eml").read_bytes())
    {'remetente': 'expedicao@embalagens.example',
     'assunto': 'Pedido de certificado - OP 123456',
     'op': '123456', 'nf': '98765', 'peso_kg': 1250.5}

Dica: email.utils.parseaddr("Nome <a@b.c>") devolve ("Nome", "a@b.c").
Para o peso: tire os pontos de milhar e troque a vírgula por ponto (módulo 05).

Teste com:  python curso.py testar 12 ex11
"""


def ler_pedido(conteudo: bytes) -> dict:
    """Extrai remetente, assunto, OP, NF e peso de um e-mail (.eml em bytes)."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
