# ======== FUNÇÕES DE PESQUISA ========

def busca_sequencial(lista, valor):
    for item in lista:
        if item["nome"].lower() == valor.lower():
            return item
    return None

def busca_indexada(indice, valor):
    primeira_letra = valor.lower()[0]
    if primeira_letra in indice:
        for item in indice[primeira_letra]:
            if item["nome"].lower() == valor.lower():
                return item
    return None

def busca_hash(tabela_hash, valor):
    return tabela_hash.get(valor.lower(), None)