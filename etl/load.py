import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from extract import extrair_vendas
from transform import transformar_vendas
from dimensoes import criar_dimensoes
from fato import criar_fato_vendas


def criar_conexao():

    load_dotenv()

    usuario = os.getenv("POSTGRES_USER")
    senha = os.getenv("POSTGRES_PASSWORD")
    banco = os.getenv("POSTGRES_DB")
    porta = os.getenv("POSTGRES_PORT")

    host = os.getenv("DB_HOST", "localhost")

    url_conexao = (
        f"postgresql+psycopg2://"
        f"{usuario}:{senha}@{host}:{porta}/{banco}"
    )

    engine = create_engine(url_conexao)

    return engine


def limpar_tabelas(engine):

    print()
    print("Limpando tabelas existentes...")

    with engine.begin() as conexao:

        conexao.execute(
            text("TRUNCATE TABLE fato_vendas RESTART IDENTITY CASCADE;")
        )

        conexao.execute(
            text("TRUNCATE TABLE dim_cliente RESTART IDENTITY CASCADE;")
        )

        conexao.execute(
            text("TRUNCATE TABLE dim_produto RESTART IDENTITY CASCADE;")
        )

        conexao.execute(
            text("TRUNCATE TABLE dim_localidade RESTART IDENTITY CASCADE;")
        )

        conexao.execute(
            text("TRUNCATE TABLE dim_data RESTART IDENTITY CASCADE;")
        )

    print("Tabelas limpas com sucesso!")


def carregar_dados():

    print()
    print("=== INICIANDO LOAD ===")

    # 1. Extrair
    df_vendas = extrair_vendas()

    # 2. Transformar
    df_transformado = transformar_vendas(df_vendas)

    # 3. Criar dimensões
    (
        dim_cliente,
        dim_produto,
        dim_localidade,
        dim_data
    ) = criar_dimensoes(df_transformado)

    # 4. Criar fato
    fato_vendas = criar_fato_vendas(
        df_transformado,
        dim_cliente,
        dim_produto,
        dim_localidade,
        dim_data
    )

    # 5. Criar conexão
    engine = criar_conexao()

    print()
    print("Conexão com PostgreSQL criada com sucesso!")

    # 6. Limpar tabelas antes da nova carga
    limpar_tabelas(engine)

    # 7. Carregar dimensões
    dim_cliente.to_sql(
        "dim_cliente",
        engine,
        if_exists="append",
        index=False
    )

    dim_produto.to_sql(
        "dim_produto",
        engine,
        if_exists="append",
        index=False
    )

    dim_localidade.to_sql(
        "dim_localidade",
        engine,
        if_exists="append",
        index=False
    )

    dim_data.to_sql(
        "dim_data",
        engine,
        if_exists="append",
        index=False
    )

    print()
    print("Dimensões carregadas com sucesso!")

    # 8. Carregar fato
    fato_vendas.to_sql(
        "fato_vendas",
        engine,
        if_exists="append",
        index=False
    )

    print("fato_vendas carregada com sucesso!")

    print()
    print("=== LOAD CONCLUÍDO ===")


if __name__ == "__main__":
    carregar_dados()