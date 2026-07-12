"""
banco.py
--------
Funções de conexão e execução de comandos no MySQL.
"""

import pymysql

from config import MYSQL_CONFIG


def conectar():
    """
    Abre e retorna uma conexão com o banco MySQL configurado no arquivo .env.
    """
    try:
        return pymysql.connect(
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=MYSQL_CONFIG["database"],
            charset="utf8mb4",
            autocommit=False,
        )

    except pymysql.MySQLError as erro:
        raise RuntimeError(
            "Não foi possível conectar ao MySQL em "
            f"{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']} "
            f"no banco '{MYSQL_CONFIG['database']}'. "
            "Verifique o arquivo .env, o servidor MySQL e se o script "
            f"'0_criar_banco.sql' já foi executado. Detalhe: {erro}"
        ) from erro


def executar(conexao, sql, parametros=None):
    """
    Executa um comando SQL e confirma a transação.

    Exemplos:
        CREATE TABLE
        TRUNCATE TABLE
        INSERT ... SELECT
        UPDATE
        DELETE
    """
    cursor = conexao.cursor()

    try:
        cursor.execute(sql, parametros)
        conexao.commit()
        return cursor.rowcount

    except pymysql.MySQLError:
        conexao.rollback()
        raise

    finally:
        cursor.close()


def inserir_em_lote(conexao, sql_insert, linhas):
    """
    Insere várias linhas por meio do executemany.
    """
    if not linhas:
        return 0

    cursor = conexao.cursor()

    try:
        total = cursor.executemany(sql_insert, linhas)
        conexao.commit()
        return total

    except pymysql.MySQLError:
        conexao.rollback()
        raise

    finally:
        cursor.close()


def consultar(conexao, sql, parametros=None):
    """
    Executa uma consulta SELECT e retorna todas as linhas.
    """
    cursor = conexao.cursor()

    try:
        cursor.execute(sql, parametros)
        return cursor.fetchall()

    finally:
        cursor.close()