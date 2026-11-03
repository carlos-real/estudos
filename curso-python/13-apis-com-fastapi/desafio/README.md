# Desafio do módulo 13 — API de Certificados do laboratório

## Contexto

Hoje a decisão "posso emitir o certificado desta OP?" mora na cabeça de quem olha a
planilha. Você vai transformar essa decisão numa **API**: um serviço que guarda as regras
de tolerância, recebe as medições, diz se a OP está liberada e só então registra o
certificado. O robô do módulo 12, uma planilha de BI ou um sistema da TI podem consultar
essa API, todos com a mesma regra.

## Requisitos obrigatórios

1. FastAPI + SQLite, com o banco num arquivo (caminho configurável por variável de
   ambiente) e a conexão entregue às rotas por uma dependência com `yield`.
2. Tabelas `regras`, `medicoes` e `certificados`. Regras iniciais para as linhas A a D,
   com os dois tipos: **faixa** (mínimo/máximo) e **nominal ± %**.
3. `GET /linhas/{linha}/regras`: regras da linha, já convertidas em mínimo e máximo.
   Linha fora de A–D responde 422.
4. `PUT /linhas/{linha}/regras/{ensaio}`: cria ou troca uma regra. Exige o cabeçalho
   `X-Chave` com perfil de escrita (401 sem chave válida; 403 com chave só de leitura).
   Regra inconsistente (mínimo > máximo, percentual zero...) responde 422.
5. `POST /medicoes`: valida o corpo com Pydantic, avalia contra a regra, grava e
   responde 201 com `aprovado`. Sem regra para o ensaio: 404.
6. `GET /ops/{op}/situacao`: total de medições, reprovadas e se a OP está liberada.
7. `POST /certificados` com OP, NF e peso: 201 se a OP está liberada; 409 se não tem
   medições, se tem reprovação, ou se o par OP/NF já tem certificado (idempotência).
8. `GET /certificados` com filtro opcional `?op=`.
9. Título, versão, tags e resumos para o `/docs` ficar organizado.
10. Rodar com uvicorn e ter um modo de demonstração que não precisa de servidor.

## Extras opcionais

- Testes com `TestClient` e banco em memória via `app.dependency_overrides`.
- Organizar em pacote (`main.py`, `banco.py`, `modelos.py`, `rotas/`), como o exemplo 07.
- `GET /ops/{op}/resumo` com média e desvio padrão por ensaio (exercício 11).
- Aceitar valores no formato brasileiro (`"41,2"`) nas medições (exercício 12).
- Gerar o PDF do certificado e devolvê-lo numa rota (`FileResponse`).
- Ligar o robô do módulo 12 à API: ele consulta `/ops/{op}/situacao` antes de emitir.

## Exemplo de execução

```text
> python 13-apis-com-fastapi/desafio/solucao_referencia.py
Regras da linha B:
   espessura  38.0 a 42.0
   gramatura  36.48 a 39.52
medição 123789 espessura   41.2 -> aprovado=True
medição 123789 gramatura   38.1 -> aprovado=True
medição 123456 espessura   43.0 -> aprovado=False
POST /certificados (OP liberada)   201 {'op': '123789', 'nf': '98766', 'peso_kg': 980.25, 'id': 1}
POST /certificados (de novo)       409 Certificado já emitido
POST /certificados (reprovada)     409 {'detail': 'OP 123456 com 1 medição(ões) reprovada(s)'}
PUT regra com chave de leitura     403 {'detail': 'Sem permissão de escrita'}
PUT regra com chave de escrita     200 {'linha': 'B', 'ensaio': 'cof', 'tipo': 'faixa', 'minimo': 0.2, 'maximo': 0.3}
Certificados emitidos: 1
```

Com `--servir`, abra `http://127.0.0.1:8000/docs` e faça o mesmo roteiro pelo navegador.

## Critérios de aceite

- [ ] A demonstração roda sem servidor e termina sem erro.
- [ ] Com `--servir`, o `/docs` mostra as rotas agrupadas por tag, com resumos.
- [ ] Espessura da linha B (40 ± 5%) aparece como 38,0 a 42,0.
- [ ] Uma OP com qualquer medição reprovada nunca recebe certificado.
- [ ] Pedir o mesmo certificado duas vezes não cria dois registros.
- [ ] Alterar regra sem chave dá 401; com chave de leitura dá 403.
- [ ] Todo SQL usa parâmetros `?` (nenhuma f-string montando SQL).
- [ ] Os dados continuam lá depois de parar e subir o servidor de novo.
- [ ] `ruff check` e `ruff format --check` passam.

## Dicas de como começar

1. Comece pelo banco: `ESQUEMA`, regras iniciais e a dependência `obter_conexao`.
   Teste no REPL que as tabelas são criadas.
2. Escreva a função pura `limites(...)` e teste com faixa e com nominal ± %.
3. Uma rota por vez, sempre com o `TestClient` num script de rascunho:
   regras → medições → situação → certificados.
4. Deixe a autenticação (`X-Chave`) por último: é uma dependência que você pluga
   na rota de escrita.
5. Para a idempotência, a restrição `UNIQUE (op, nf)` no banco é a última linha de
   defesa; a consulta antes do `INSERT` dá a mensagem amigável.

A solução de referência está em `solucao_referencia.py`. Tente antes de abrir.
