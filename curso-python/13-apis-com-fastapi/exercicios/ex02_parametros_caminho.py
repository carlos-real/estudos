"""
Exercício 13.02 — Parâmetros de caminho
Nível: ★☆☆

Contexto: um pedaço do endereço pode ser variável, como o número da bobina em
/bobinas/42. O FastAPI lê esse pedaço, converte para o tipo que você declarar
e recusa (com 422) o que não servir.

Tarefa: no `app` abaixo, crie duas rotas GET:
- "/dobro/{numero}"    numero é int. Devolva {"numero": numero, "dobro": numero * 2}.
                       Um número inválido ("abc") deve dar 422 (o FastAPI faz isso
                       sozinho se você declarar o tipo).
- "/saudacao/{nome}"   devolva {"mensagem": "Olá, <nome>!"}

Exemplos:
    >>> cliente.get("/dobro/21").json()
    {'numero': 21, 'dobro': 42}
    >>> cliente.get("/saudacao/Carla").json()
    {'mensagem': 'Olá, Carla!'}
    >>> cliente.get("/dobro/abc").status_code
    422

Dica: o nome entre chaves no caminho tem de ser IGUAL ao nome do parâmetro
da função: @app.get("/dobro/{numero}") -> def dobro(numero: int).

Teste com:  python curso.py testar 13 ex02
"""

from fastapi import FastAPI

app = FastAPI()

# Escreva suas rotas aqui
