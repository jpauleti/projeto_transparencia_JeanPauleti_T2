"""
1_extrair.py - FASE 1: Extração e Camada RAW
--------------------------------------------

Passos:
    1. Baixar o arquivo ZIP do Google Drive, caso ainda não exista.
    2. Ler os quatro CSVs diretamente de dentro do ZIP.
    3. Inserir os dados sem transformação nas tabelas RAW do MySQL.

A camada RAW preserva os dados originais como texto.
"""

import zipfile
import gdown
import pandas as pd
import banco
import config


# ---------------------------------------------------------------------------
# Passo 1 - Baixar o arquivo ZIP
# ---------------------------------------------------------------------------
def baixar_zip():
    """Baixa o arquivo ZIP do Google Drive caso ele ainda não exista."""

    if config.CAMINHO_ZIP.exists():
        print("[1/4] Arquivo ZIP encontrado:", config.NOME_ZIP)
        return

    print("[1/4] Arquivo ZIP não encontrado.")
    print("      Baixando do Google Drive...")

    url = f"https://drive.google.com/uc?id={config.DRIVE_FILE_ID}"

    gdown.download(
        url,
        str(config.CAMINHO_ZIP),
        quiet=False,
    )

    print("      Download concluído.")


# ---------------------------------------------------------------------------
# Passo 2 - Localizar o arquivo ZIP
# ---------------------------------------------------------------------------
def localizar_zip():
    """Retorna o caminho do arquivo ZIP."""

    if not config.CAMINHO_ZIP.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {config.CAMINHO_ZIP}"
        )

    return config.CAMINHO_ZIP


# ---------------------------------------------------------------------------
# Passo 3 - Carregar um CSV em sua tabela RAW
# ---------------------------------------------------------------------------
def carregar_csv(conexao, zip_aberto, nome_csv, tabela):
    """Lê um CSV dentro do ZIP e insere seus dados na tabela RAW."""
    pass


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():

    print("=== FASE 1: EXTRACAO + CAMADA RAW ===")

    try:

        baixar_zip()

        caminho_zip = localizar_zip()

        print()
        print("Arquivo localizado com sucesso:")
        print(caminho_zip)

    except Exception as erro:

        print("[ERRO]", erro)
        raise


if __name__ == "__main__":
    main()