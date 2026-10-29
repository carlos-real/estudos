"""
Solução — Exercício 03.13 — Revisão: juntar pedidos e resultados

Ideia central: para juntar duas tabelas por uma chave, transforme uma delas
num DICIONÁRIO indexado pela chave (como um PROCV pronto) e depois percorra a
outra. É o que o SQL faz num LEFT JOIN e o pandas faz em merge(how="left").
"""


def normalizar_op(texto: str) -> str:
    """Padroniza o código da OP: " op 4512 " -> "OP-4512"."""
    # Métodos encadeados: cada um devolve uma string NOVA (strings são imutáveis).
    return texto.strip().upper().replace(" ", "-")


def indexar_por_op(resultados: list[dict]) -> dict[str, dict]:
    """Devolve OP normalizada -> resultado (o último, se houver repetição)."""
    # Numa compreensão de dicionário, se a chave se repete, a atribuição
    # seguinte sobrescreve a anterior. Por isso "vale o último" sai de graça.
    return {normalizar_op(resultado["op"]): resultado for resultado in resultados}


def juntar(pedidos: list[dict], resultados: list[dict]) -> list[dict]:
    """LEFT JOIN: cada pedido ganha "linha" e "status" do seu resultado."""
    indice = indexar_por_op(resultados)  # monta o "PROCV" UMA vez só

    juntados = []
    for pedido in pedidos:
        op = normalizar_op(pedido["op"])
        resultado = indice.get(op)  # busca instantânea, sem laço interno

        # {**pedido, ...} cria um dicionário NOVO com as chaves do pedido e
        # depois sobrescreve/acrescenta as chaves seguintes. O pedido original
        # não é tocado. (Equivalente: novo = pedido.copy(); novo["op"] = op ...)
        if resultado is None:
            novo = {**pedido, "op": op, "linha": None, "status": "sem resultado"}
        else:
            status = resultado["status"].strip().lower()
            novo = {**pedido, "op": op, "linha": resultado["linha"], "status": status}
        juntados.append(novo)
    return juntados


def resumo_expedicao(juntados: list[dict]) -> dict:
    """Separa as OPs em emitir / bloqueadas / sem_resultado e soma o peso."""
    emitir: list[str] = []
    bloqueadas: list[str] = []
    sem_resultado: list[str] = []
    peso_emitir = 0.0  # acumulador

    for registro in juntados:
        status = registro["status"]
        if status == "aprovado":
            emitir.append(registro["op"])
            peso_emitir += registro["peso_kg"]
        elif status == "sem resultado":
            sem_resultado.append(registro["op"])
        else:
            bloqueadas.append(registro["op"])

    return {
        "emitir": emitir,
        "bloqueadas": bloqueadas,
        "sem_resultado": sem_resultado,
        "peso_emitir_kg": round(peso_emitir, 1),
    }
