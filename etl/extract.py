import pandas as pd


def extrair_vendas():
    caminho_arquivo = "dados/vendas.csv"

    df = pd.read_csv(
        caminho_arquivo,
        sep=";",
        encoding="utf-8"
    )

    print("Arquivo lido com sucesso!")
    print()
    print("Quantidade de linhas e colunas:")
    print(df.shape)

    print()
    print("Primeiras linhas:")
    print(df.head())

    print()
    print("Nomes das colunas:")
    print(df.columns.tolist())


    print()
    print("Tipos das colunas:")
    print(df.dtypes)

    print()
    print("Valores nulos por coluna:")
    print(df.isnull().sum())

    print()
    print("Quantidade de linhas duplicadas:")
    print(df.duplicated().sum())

    print()
    print("Categorias encontradas:")
    print(df["categoria"].unique())

    print()
    print("UFs encontradas:")
    print(df["uf"].unique())

    return df


if __name__ == "__main__":
    extrair_vendas()