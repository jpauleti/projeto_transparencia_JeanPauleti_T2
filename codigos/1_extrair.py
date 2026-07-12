"""
1_extrair.py - FASE 1: Extração e Camada RAW
--------------------------------------------

Passos:
    1. Baixar o arquivo ZIP do Google Drive, caso ainda não exista.
    2. Ler os quatro CSVs diretamente de dentro do ZIP.
    3. Inserir os dados sem transformação nas tabelas RAW do MySQL.

A camada RAW preserva os dados originais como texto.
"""

# Bibliotecas da linguagem
import zipfile

# Bibliotecas de terceiros
import gdown
import pandas as pd

# Módulos do projeto
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

    gdown.download(
    id=config.DRIVE_FILE_ID,
    output=str(config.CAMINHO_ZIP),
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
    """
    Lê um CSV diretamente de dentro do ZIP e insere todas as linhas
    na tabela RAW correspondente.

    As colunas do CSV devem estar na mesma ordem das colunas definidas
    na tabela RAW do arquivo 0_criar_banco.sql.
    """
    print("      Carregando", tabela, "...")

    # Garante idempotência: uma nova execução não duplica os registros.
    banco.executar(conexao, f"TRUNCATE TABLE {tabela}")

    total = 0

    with zip_aberto.open(nome_csv) as arquivo:
        pedacos = pd.read_csv(
            arquivo,
            sep=config.CSV_SEPARADOR,
            encoding=config.CSV_ENCODING,
            dtype=str,
            keep_default_na=False,
            chunksize=config.TAMANHO_BLOCO,
        )

        for pedaco in pedacos:
            linhas = pedaco.values.tolist()

            marcadores = ", ".join(
                ["%s"] * len(pedaco.columns)
            )

            comando = (
                f"INSERT INTO {tabela} "
                f"VALUES ({marcadores})"
            )

            banco.inserir_em_lote(
                conexao,
                comando,
                linhas,
            )

            total += len(linhas)

    print("      ->", total, "linhas em", tabela)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    """Executa o download e a carga das quatro tabelas RAW."""
    print("=== FASE 1: EXTRACAO + CAMADA RAW ===")

    conexao = None

    try:
        baixar_zip()
        caminho_zip = localizar_zip()

        print("[2/4] Conectando ao MySQL...")
        conexao = banco.conectar()

        print("[3/4] Abrindo o arquivo ZIP...")

        with zipfile.ZipFile(caminho_zip) as zip_aberto:
            arquivos_zip = zip_aberto.namelist()

            print("[4/4] Carregando as 4 tabelas RAW...")

            for arquivo in config.ARQUIVOS.values():
                nome_csv = arquivo["csv"]
                tabela_raw = arquivo["tabela_raw"]

                if nome_csv not in arquivos_zip:
                    raise FileNotFoundError(
                        f"O arquivo '{nome_csv}' não foi encontrado "
                        f"dentro de '{config.NOME_ZIP}'."
                    )

                carregar_csv(
                    conexao,
                    zip_aberto,
                    nome_csv,
                    tabela_raw,
                )

        print("=== Camada RAW concluida com sucesso! ===")

    except zipfile.BadZipFile as erro:
        print("[ERRO] O arquivo baixado não é um ZIP válido.")
        raise erro

    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise

    finally:
        if conexao is not None:
            conexao.close()
            print("Conexão com o MySQL encerrada.")

if __name__ == "__main__":
    main()