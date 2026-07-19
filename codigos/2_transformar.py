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

# ===========================================================
# silver_passagem
# ===========================================================

SQL_PASSAGEM = """
INSERT INTO silver_passagem (
    id_viagem,
    meio_transporte,
    pais_origem_ida,
    uf_origem_ida,
    cidade_origem_ida,
    pais_destino_ida,
    uf_destino_ida,
    cidade_destino_ida,
    valor_passagem,
    taxa_servico,
    data_emissao
)
SELECT
    NULLIF(TRIM(id_viagem), ''),
    NULLIF(TRIM(meio_transporte), ''),
    NULLIF(TRIM(pais_origem_ida), ''),
    NULLIF(TRIM(uf_origem_ida), ''),
    NULLIF(TRIM(cidade_origem_ida), ''),
    NULLIF(TRIM(pais_destino_ida), ''),
    NULLIF(TRIM(uf_destino_ida), ''),
    NULLIF(TRIM(cidade_destino_ida), ''),

    CAST(
        REPLACE(
            REPLACE(
                NULLIF(TRIM(valor_passagem), ''),
                '.',
                ''
            ),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    ),

    CAST(
        REPLACE(
            REPLACE(
                NULLIF(TRIM(taxa_servico), ''),
                '.',
                ''
            ),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    ),

    STR_TO_DATE(
        NULLIF(TRIM(data_emissao), ''),
        '%d/%m/%Y'
    )

FROM raw_passagem
WHERE id_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

# ===========================================================
# silver_trecho
# ===========================================================

SQL_TRECHO = """
INSERT INTO silver_trecho (
    id_viagem,
    sequencia_trecho,
    origem_data,
    origem_uf,
    origem_cidade,
    destino_data,
    destino_uf,
    destino_cidade,
    meio_transporte,
    numero_diarias
)
SELECT
    NULLIF(TRIM(id_viagem), ''),

    CAST(
        NULLIF(TRIM(sequencia_trecho), '')
        AS UNSIGNED
    ),

    STR_TO_DATE(
        NULLIF(TRIM(origem_data), ''),
        '%d/%m/%Y'
    ),

    NULLIF(TRIM(origem_uf), ''),
    NULLIF(TRIM(origem_cidade), ''),

    STR_TO_DATE(
        NULLIF(TRIM(destino_data), ''),
        '%d/%m/%Y'
    ),

    NULLIF(TRIM(destino_uf), ''),
    NULLIF(TRIM(destino_cidade), ''),
    NULLIF(TRIM(meio_transporte), ''),

    CAST(
        REPLACE(
            REPLACE(
                NULLIF(TRIM(numero_diarias), ''),
                '.',
                ''
            ),
            ',',
            '.'
        ) AS DECIMAL(10,2)
    )

FROM raw_trecho
WHERE id_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

# ===========================================================
# Validacao de duplicidades
# ===========================================================

# silver_viagem: id_viagem deve identificar uma única viagem.
SQL_DUPLICADOS_VIAGEM = """
SELECT
    id_viagem,
    COUNT(*) AS quantidade
FROM silver_viagem
GROUP BY id_viagem
HAVING COUNT(*) > 1
ORDER BY quantidade DESC, id_viagem
"""

def validar_duplicidades(conexao):
    """
    Verifica duplicidades nas tabelas silver_viagem e silver_passagem.

    """

    duplicados_viagem = banco.consultar(
        conexao,
        SQL_DUPLICADOS_VIAGEM
    )

    if not duplicados_viagem:
        print(
            "[OK] silver_viagem: "
            "nenhum id_viagem duplicado."
        )

    else:
        print(
            "[ATENCAO] silver_viagem: "
            f"{len(duplicados_viagem)} id(s) duplicado(s)."
        )

        print("Exemplos encontrados:")

        for id_viagem, quantidade in duplicados_viagem[:10]:
            print(
                f"    id_viagem={id_viagem} "
                f"| quantidade={quantidade}"
            )

    return duplicados_viagem

def main():

    print("=== FASE 2: TRANSFORMACAO + CAMADA SILVER ===")

    conexao = None

    try:

        conexao = banco.conectar()

        print("[1/7] Limpando tabelas SILVER...")

        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/7] Carregando silver_viagem...")
        banco.executar(conexao, SQL_VIAGEM)
        print("      silver_viagem carregada.")

        print("[3/7] Calculando valor_total e duracao_dias...")
        banco.executar(conexao, SQL_CALC_VIAGEM)
        print("      Colunas calculadas.")

        print("[4/7] Carregando silver_pagamento...")
        banco.executar(conexao, SQL_PAGAMENTO)
        print("      silver_pagamento carregada.")

        print("[5/7] Carregando silver_passagem...")
        banco.executar(conexao, SQL_PASSAGEM)
        print("      silver_passagem carregada.")

        print("[6/7] Carregando silver_trecho...")
        banco.executar(conexao, SQL_TRECHO)
        print("      silver_trecho carregada.")

        print("[7/7] Validando duplicidades...")
        validar_duplicidades(conexao)


    except Exception as erro:

        print("[ERRO]", erro)
        raise

    finally:

        if conexao is not None:
            conexao.close()
            print("Conexao com o MySQL encerrada.")


if __name__ == "__main__":
    main()