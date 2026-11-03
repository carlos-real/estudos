@echo off
REM Exemplo 11 - Lancador para o Agendador de Tarefas do Windows.
REM Ajuste as duas linhas abaixo para o seu computador.
set PASTA=C:\robos\curso-python
set SCRIPT=12-automacao-e-integracao\exemplos\09_robo_certificados.py

REM Entra na pasta do projeto (o Agendador comeca em C:\Windows\System32).
cd /d "%PASTA%"

REM Usa o Python do ambiente virtual direto: nao precisa "ativar" o venv.
REM A saida (e os erros) vao para um arquivo de log.
if not exist logs mkdir logs
".venv\Scripts\python.exe" "%SCRIPT%" >> "logs\agendador.log" 2>&1

REM Repassa o codigo de saida do Python para o Agendador (0 = sucesso).
exit /b %ERRORLEVEL%
