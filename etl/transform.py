import pandas as pd

from decimal import Decimal, ROUND_HALF_UP
from extract import extrair_vendas


def transformar_vendas(df):

    print()
    print("=== INICIANDO TRANSFORMAÇÃO ===")

    # Faz uma cópia para não alterar o DataFrame original
    df = df.copy()

    print()
    print("Quantidade inicial de linhas:")
    print(len(df))

    # 1. Remover registros duplicados
    df = df.drop_duplicates()

    print()
    print("Quantidade após remover duplicados:")
    print(len(df))

    # 2. Preencher descontos vazios com zero
    df["desconto_pct"] = df["desconto_pct"].fillna(0)

    print()
    print("Valores nulos em desconto_pct:")
    print(df["desconto_pct"].isnull().sum())

    # 3. Padronizar categorias
    df["categoria"] = (
        df["categoria"]
        .str.strip()
        .str.title()
    )

    # 4. Padronizar UF
    df["uf"] = (
        df["uf"]
        .str.strip()
        .str.upper()
    )

    print()
    print("Categorias após padronização:")
    print(df["categoria"].unique())

    print()
    print("UFs após padronização:")
    print(df["uf"].unique())

    # 5. Converter data_venda para data
    df["data_venda"] = pd.to_datetime(
        df["data_venda"],
        format="%d/%m/%Y"
    )

    # 6. Converter preco_unitario para número
    df["preco_unitario"] = (
        df["preco_unitario"]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    print()
    print("Tipos após conversão:")
    print(df[["data_venda", "preco_unitario"]].dtypes)

    # 7. Calcular valor bruto
    df["valor_bruto"] = (
        df["quantidade"] * df["preco_unitario"]
    )

    # 8. Calcular valor do desconto
    df["valor_desconto"] = (
        df["valor_bruto"] * df["desconto_pct"] / 100
    )

    # 9. Calcular valor líquido
    df["valor_liquido"] = (
        df["valor_bruto"] - df["valor_desconto"]
    )

    # 10. Arredondar valores monetários para 2 casas decimais
    def arredondar_moeda(valor):
        return float(
            Decimal(str(valor)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        )

    df["valor_bruto"] = df["valor_bruto"].apply(arredondar_moeda)

    df["valor_desconto"] = df["valor_desconto"].apply(arredondar_moeda)

    df["valor_liquido"] = df["valor_liquido"].apply(arredondar_moeda)

    print()
    print("Primeiras vendas com valores calculados:")
    print(
        df[
            [
                "id_venda",
                "quantidade",
                "preco_unitario",
                "desconto_pct",
                "valor_bruto",
                "valor_desconto",
                "valor_liquido"
            ]
        ].head()
    )

    print()
    print("=== TOTAIS PARA VALIDAÇÃO ===")

    print("Quantidade de vendas:")
    print(len(df))

    print()
    print("Quantidade total de itens vendidos:")
    print(df["quantidade"].sum())

    print()
    print("Valor bruto total:")
    print(round(df["valor_bruto"].sum(), 2))

    print()
    print("Valor total de descontos:")
    print(round(df["valor_desconto"].sum(), 2))

    print()
    print("Valor líquido total:")
    print(round(df["valor_liquido"].sum(), 2))

    return df


if __name__ == "__main__":

    df_vendas = extrair_vendas()

    df_transformado = transformar_vendas(df_vendas)

    print()
    print("=== TRANSFORMAÇÃO CONCLUÍDA ===")

    print()
    print("Quantidade final de linhas:")
    print(len(df_transformado))