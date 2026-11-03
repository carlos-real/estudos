"""API do Laboratório de Qualidade organizada em módulos (exemplo 07 do módulo 13).

Estrutura:
    main.py           cria o app e "pluga" os routers
    banco.py          conexão SQLite, tabelas e dados iniciais
    modelos.py        modelos Pydantic (o que entra e o que sai)
    regras.py         lógica pura de tolerância (sem FastAPI, sem banco)
    rotas/            um arquivo por assunto, cada um com seu APIRouter

Para subir o servidor, de dentro da pasta exemplos:
    uvicorn api_laboratorio.main:app --reload
"""
