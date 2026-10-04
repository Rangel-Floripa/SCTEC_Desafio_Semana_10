from extract import extrair_vendas
from transform import transformar_vendas


def criar_dimensoes(df):

    print()
    print("=== CRIANDO DIMENSÕES ===")

    # -----------------------------
    # DIMENSÃO CLIENTE
    # -----------------------------
    dim_cliente = (
        df[
            [
                "cliente",
                "email"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_cliente.insert(
        0,
        "sk_cliente",
        range(1, len(dim_cliente) + 1)
    )

    print()
    print("dim_cliente:")
    print(dim_cliente.head())
    print("Quantidade:", len(dim_cliente))

    # -----------------------------
    # DIMENSÃO PRODUTO
    # -----------------------------
    dim_produto = (
        df[
            [
                "produto",
                "categoria"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_produto.insert(
        0,
        "sk_produto",
        range(1, len(dim_produto) + 1)
    )

    print()
    print("dim_produto:")
    print(dim_produto.head())
    print("Quantidade:", len(dim_produto))

    # -----------------------------
    # DIMENSÃO LOCALIDADE
    # -----------------------------
    dim_localidade = (
        df[
            [
                "cidade",
                "uf"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_localidade.insert(
        0,
        "sk_localidade",
        range(1, len(dim_localidade) + 1)
    )

    print()
    print("dim_localidade:")
    print(dim_localidade.head())
    print("Quantidade:", len(dim_localidade))

    # -----------------------------
    # DIMENSÃO DATA
    # -----------------------------
    dim_data = (
        df[
            [
                "data_venda"
            ]
        ]
        .drop_duplicates()
        .sort_values("data_venda")
        .reset_index(drop=True)
    )

    dim_data["dia"] = dim_data["data_venda"].dt.day
    dim_data["mes"] = dim_data["data_venda"].dt.month
    dim_data["ano"] = dim_data["data_venda"].dt.year
    dim_data["trimestre"] = dim_data["data_venda"].dt.quarter

    dim_data.insert(
        0,
        "sk_data",
        range(1, len(dim_data) + 1)
    )

    print()
    print("dim_data:")
    print(dim_data.head())
    print("Quantidade:", len(dim_data))

    return (
        dim_cliente,
        dim_produto,
        dim_localidade,
        dim_data
    )


if __name__ == "__main__":

    df_vendas = extrair_vendas()

    df_transformado = transformar_vendas(df_vendas)

    criar_dimensoes(df_transformado)