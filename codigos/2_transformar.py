"""
2_transformar.py - FASE 2: Transformação e Camada SILVER
--------------------------------------------------------

Passo a passo:
    1. Limpa as tabelas SILVER.
    2. Copia os dados RAW para SILVER convertendo os tipos.
    3. Calcula as colunas valor_total e duracao_dias.
"""

import banco



# Esvaziar as tabelas SILVER

LIMPAR_SILVER = [
    "DELETE FROM silver_trecho",
    "DELETE FROM silver_pagamento",
    "DELETE FROM silver_passagem",
    "DELETE FROM silver_viagem",
]


def main():

    print("=== FASE 2: TRANSFORMACAO + CAMADA SILVER ===")

    conexao = None

    try:

        conexao = banco.conectar()

        print("[1/2] Limpando tabelas SILVER...")

        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/2] Transformações ainda não implementadas.")

        print("=== Camada SILVER preparada ===")

    except Exception as erro:

        print("[ERRO]", erro)
        raise

    finally:

        if conexao is not None:
            conexao.close()


if __name__ == "__main__":
    main()