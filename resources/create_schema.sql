CREATE TABLE IF NOT EXISTS modelo_urna
(
    id     INT PRIMARY KEY NOT NULL,
    modelo VARCHAR(6),
    UNIQUE (modelo)
);

CREATE TABLE IF NOT EXISTS votacao_secao_urna
(
    id                 INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    cd_municipio       INT             NOT NULL,
    nr_zona            INT             NOT NULL,
    nr_secao           INT             NOT NULL,
    nr_local_votacao   INT             NOT NULL,
    nome_arquivo_fonte TEXT            NOT NULL,
    id_modelo_urna     INT             NULL,
    modelo_urna_incerto BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (id_modelo_urna) REFERENCES modelo_urna (id),
    UNIQUE (cd_municipio, nr_zona, nr_secao, nr_local_votacao)
);

INSERT INTO modelo_urna (id, modelo)
VALUES (1, 'UE2009')
ON CONFLICT DO NOTHING;
INSERT INTO modelo_urna (id, modelo)
VALUES (2, 'UE2010')
ON CONFLICT DO NOTHING;
INSERT INTO modelo_urna (id, modelo)
VALUES (3, 'UE2011')
ON CONFLICT DO NOTHING;
INSERT INTO modelo_urna (id, modelo)
VALUES (4, 'UE2013')
ON CONFLICT DO NOTHING;
INSERT INTO modelo_urna (id, modelo)
VALUES (5, 'UE2015')
ON CONFLICT DO NOTHING;
INSERT INTO modelo_urna (id, modelo)
VALUES (6, 'UE2020')
ON CONFLICT DO NOTHING;