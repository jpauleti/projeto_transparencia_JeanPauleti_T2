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

# ===============================================
# silver_viagem
# ===============================================

# Query para copiar raw_viagem para silver_viagem

SQL_VIAGEM = """
INSERT INTO silver_viagem (
    id_viagem,
    num_proposta,
    situacao,
    viagem_urgente,
    cod_orgao_superior,
    nome_orgao_superior,
    nome_viajante,
    cargo,
    data_inicio,
    data_fim,
    destinos,
    motivo,
    valor_diarias,
    valor_passagens,
    valor_devolucao,
    valor_outros_gastos
)
SELECT
    NULLIF(TRIM(id_viagem), ''),
    NULLIF(TRIM(num_proposta), ''),
    NULLIF(TRIM(situacao), ''),
    NULLIF(TRIM(viagem_urgente), ''),
    NULLIF(TRIM(cod_orgao_superior), ''),
    NULLIF(TRIM(nome_orgao_superior), ''),
    NULLIF(TRIM(nome_viajante), ''),
    NULLIF(TRIM(cargo), ''),

    STR_TO_DATE(
        NULLIF(TRIM(data_inicio), ''),
        '%d/%m/%Y'
    ),

    STR_TO_DATE(
        NULLIF(TRIM(data_fim), ''),
        '%d/%m/%Y'
    ),

    NULLIF(TRIM(destinos), ''),
    NULLIF(TRIM(motivo), ''),

    CAST(
        REPLACE(
            REPLACE(NULLIF(TRIM(valor_diarias), ''), '.', ''),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    ),

    CAST(
        REPLACE(
            REPLACE(NULLIF(TRIM(valor_passagens), ''), '.', ''),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    ),

    CAST(
        REPLACE(
            REPLACE(NULLIF(TRIM(valor_devolucao), ''), '.', ''),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    ),

    CAST(
        REPLACE(
            REPLACE(NULLIF(TRIM(valor_outros_gastos), ''), '.', ''),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    )

FROM raw_viagem
"""

# Query para calcular as colunas derivadas de silver_viagem

SQL_CALC_VIAGEM = """
UPDATE silver_viagem
SET
    valor_total =
        COALESCE(valor_diarias, 0)
        + COALESCE(valor_passagens, 0)
        + COALESCE(valor_outros_gastos, 0)
        - COALESCE(valor_devolucao, 0),

    duracao_dias =
        DATEDIFF(data_fim, data_inicio)
"""

# ===========================================================
# silver_pagamento
# ===========================================================

# Query para copiar raw_pagamento para silver_pagamento

SQL_PAGAMENTO = """
INSERT INTO silver_pagamento (
    id_viagem,
    num_proposta,
    nome_orgao_pagador,
    nome_ug_pagadora,
    tipo_pagamento,
    valor
)
SELECT
    NULLIF(TRIM(id_viagem), ''),
    NULLIF(TRIM(num_proposta), ''),
    NULLIF(TRIM(nome_orgao_pagador), ''),
    NULLIF(TRIM(nome_ug_pagadora), ''),
    NULLIF(TRIM(tipo_pagamento), ''),

    CAST(
        REPLACE(
            REPLACE(
                NULLIF(TRIM(valor), ''),
                '.',
                ''
            ),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    )

FROM raw_pagamento
WHERE id_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

def main():

    print("=== FASE 2: TRANSFORMACAO + CAMADA SILVER ===")

    conexao = None

    try:

        conexao = banco.conectar()

        print("[1/4] Limpando tabelas SILVER...")

        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/4] Carregando silver_viagem...")
        banco.executar(conexao, SQL_VIAGEM)
        print("      silver_viagem carregada.")

        print("[3/4] Calculando valor_total e duracao_dias...")
        banco.executar(conexao, SQL_CALC_VIAGEM)
        print("      Colunas calculadas.")

        print("[4/4] Carregando silver_pagamento...")
        banco.executar(conexao, SQL_PAGAMENTO)
        print("      silver_pagamento carregada.")
        
        print("=== Transformacao de silver_viagem concluida! ===")


    except Exception as erro:

        print("[ERRO]", erro)
        raise

    finally:

        if conexao is not None:
            conexao.close()
            print("Conexao com o MySQL encerrada.")


if __name__ == "__main__":
    main()