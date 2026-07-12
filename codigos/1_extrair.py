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
    pass


# ---------------------------------------------------------------------------
# Passo 2 - Localizar o arquivo ZIP
# ---------------------------------------------------------------------------
def localizar_zip():
    """Localiza e retorna o caminho do arquivo ZIP na pasta data."""
    pass


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
    """Executa o processo de extração e carga da camada RAW."""
    pass


if __name__ == "__main__":
    main()