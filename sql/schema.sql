CREATE TABLE IF NOT EXISTS dim_cliente (
    sk_cliente INTEGER PRIMARY KEY,
    cliente VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_produto (
    sk_produto INTEGER PRIMARY KEY,
    produto VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_localidade (
    sk_localidade INTEGER PRIMARY KEY,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_data (
    sk_data INTEGER PRIMARY KEY,
    data_venda DATE NOT NULL,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    trimestre INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS fato_vendas (
    id_venda INTEGER PRIMARY KEY,

    sk_data INTEGER NOT NULL,
    sk_cliente INTEGER NOT NULL,
    sk_produto INTEGER NOT NULL,
    sk_localidade INTEGER NOT NULL,

    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(12,2) NOT NULL,
    desconto_pct NUMERIC(5,2) NOT NULL,

    valor_bruto NUMERIC(12,2) NOT NULL,
    valor_desconto NUMERIC(12,2) NOT NULL,
    valor_liquido NUMERIC(12,2) NOT NULL,

    CONSTRAINT fk_fato_data
        FOREIGN KEY (sk_data)
        REFERENCES dim_data(sk_data),

    CONSTRAINT fk_fato_cliente
        FOREIGN KEY (sk_cliente)
        REFERENCES dim_cliente(sk_cliente),

    CONSTRAINT fk_fato_produto
        FOREIGN KEY (sk_produto)
        REFERENCES dim_produto(sk_produto),

    CONSTRAINT fk_fato_localidade
        FOREIGN KEY (sk_localidade)
        REFERENCES dim_localidade(sk_localidade)
);