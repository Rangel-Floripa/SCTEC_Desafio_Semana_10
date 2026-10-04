from extract import extrair_vendas
from transform import transformar_vendas
from dimensoes import criar_dimensoes


def criar_fato_vendas(
    df,
    dim_cliente,
    dim_produto,
    dim_localidade,
    dim_data
):

    print()
    print("=== CRIANDO FATO_VENDAS ===")

    fato = df.copy()

    # Relacionar cliente
    fato = fato.merge(
        dim_cliente,
        on=["cliente", "email"],
        how="left"
    )

    # Relacionar produto
    fato = fato.merge(
        dim_produto,
        on=["produto", "categoria"],
        how="left"
    )

    # Relacionar localidade
    fato = fato.merge(
        dim_localidade,
        on=["cidade", "uf"],
        how="left"
    )

    # Relacionar data
    fato = fato.merge(
        dim_data[
            [
                "sk_data",
                "data_venda"
            ]
        ],
        on="data_venda",
        how="left"
    )

    # Selecionar apenas as colunas da fato
    fato = fato[
        [
            "id_venda",
            "sk_data",
            "sk_cliente",
            "sk_produto",
            "sk_localidade",
            "quantidade",
            "preco_unitario",
            "desconto_pct",
            "valor_bruto",
            "valor_desconto",
            "valor_liquido"
        ]
    ]

    print()
    print("Primeiras linhas da fato_vendas:")
    print(fato.head())

    print()
    print("Quantidade de registros:")
    print(len(fato))

    print()
    print("Chaves nulas encontradas:")
    print(
        fato[
            [
                "sk_data",
                "sk_cliente",
                "sk_produto",
                "sk_localidade"
            ]
        ].isnull().sum()
    )

    return fato


if __name__ == "__main__":

    df_vendas = extrair_vendas()

    df_transformado = transformar_vendas(df_vendas)

    (
        dim_cliente,
        dim_produto,
        dim_localidade,
        dim_data
    ) = criar_dimensoes(df_transformado)

    fato_vendas = criar_fato_vendas(
        df_transformado,
        dim_cliente,
        dim_produto,
        dim_localidade,
        dim_data
    )

    print()
    print("=== FATO_VENDAS CRIADA COM SUCESSO ===")