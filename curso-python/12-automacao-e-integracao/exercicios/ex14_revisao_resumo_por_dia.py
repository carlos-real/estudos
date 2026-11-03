"""
Exercício 12.14 — Revisão: resumo diário dos pedidos por e-mail
Nível: ★★☆

Revisão de: números brasileiros e regex (módulo 05), datas e acumuladores com
dicionário (módulos 03 e 07) + leitura de e-mails (este módulo).

Contexto: o supervisor da expedição quer saber, por dia, quantos pedidos de
certificado chegaram e quanto peso eles somam. Você tem os e-mails em bytes.

Tarefa: implemente resumir_por_dia(emails).
- Cada item de `emails` são os bytes de um .eml. Leia com
  BytesParser(policy=policy.default).
- A data de cada pedido vem do cabeçalho "Date": converta com
  email.utils.parsedate_to_datetime e use só a data (.date()), no fuso do
  próprio cabeçalho (não converta fusos).
- O peso vem do corpo em texto puro (msg.get_body(preferencelist=("plain",)));
  procure "Peso: 1.250,5 kg" (dois-pontos opcional, maiúsculas ou minúsculas)
  e converta o número brasileiro para float.
- E-mails sem peso no texto puro (ou sem texto puro) são IGNORADOS.
- Agrupe por data: quantidade de pedidos e soma dos pesos.
- Devolva uma lista de textos, do dia mais antigo para o mais recente, assim:
      "09/03/2026: 3 pedidos, 4.540,75 kg"
      "10/03/2026: 1 pedido, 640,00 kg"
  ("pedido" no singular quando for 1; peso com 2 casas, no formato brasileiro).
- Lista vazia de e-mails (ou nenhum válido) -> [].

Exemplos:
    >>> resumir_por_dia([eml1, eml2, eml3])
    ['09/03/2026: 2 pedidos, 2.230,75 kg', '10/03/2026: 1 pedido, 2.310,00 kg']

Dica: um dicionário {data: [quantidade, soma]} ou dois defaultdict. Objetos
date podem ser ordenados com sorted() e formatados com strftime("%d/%m/%Y").

Teste com:  python curso.py testar 12 ex14
"""


def resumir_por_dia(emails: list[bytes]) -> list[str]:
    """Uma linha por dia: data, quantidade de pedidos e peso total."""
    # Escreva seu código aqui
    raise NotImplementedError("Implemente esta função")
