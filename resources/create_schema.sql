CREATE TABLE IF NOT EXISTS modelo_urna
(
    id     INT PRIMARY KEY NOT NULL,
    modelo VARCHAR(6),
    UNIQUE (modelo)
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

CREATE TABLE IF NOT EXISTS votacao_secao_urna
(
    id                  INT PRIMARY KEY       NOT NULL GENERATED ALWAYS AS IDENTITY,
    cd_municipio        INT                   NOT NULL,
    nr_zona             INT                   NOT NULL,
    nr_secao            INT                   NOT NULL,
    nr_local_votacao    INT                   NOT NULL,
    nome_arquivo_fonte  TEXT                  NOT NULL,
    id_modelo_urna      INT                   NULL,
    modelo_urna_incerto BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (id_modelo_urna) REFERENCES modelo_urna (id),
    UNIQUE (cd_municipio, nr_zona, nr_secao, nr_local_votacao)
);

CREATE TABLE votacao_secao_cargo
(
    id        INT PRIMARY KEY NOT NULL,
    descricao TEXT            NOT NULL
);

INSERT INTO votacao_secao_cargo (id, descricao)
VALUES (1, 'PRESIDENTE');

CREATE TABLE votacao_secao_candidato
(
    id           INT PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY,
    nr_votavel   INT             NOT NULL,
    nm_votavel   TEXT            NOT NULL,
    sq_candidato REAL            NOT NULL,
    unique (nr_votavel)
);

INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (12, 'CIRO FERREIRA GOMES', 280001612393)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (22, 'JAIR MESSIAS BOLSONARO', 280001618036)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (27, 'JOSE MARIA EYMAEL', 280001677435)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (14, 'KELMON LUIS DA SILVA SOUZA', 280001734029)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (80, 'LEONARDO PÉRICLES VIEIRA ROQUE', 280001602702)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (30, 'LUIZ FELIPE CHAVES D AVILA', 280001603612)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (13, 'LUIZ INÁCIO LULA DA SILVA', 280001607829)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (15, 'SIMONE NASSAR TEBET', 280001607833)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (21, 'SOFIA PADUA MANZANO', 280001600167)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (44, 'SORAYA VIEIRA THRONICKE', 280001644128)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (16, 'VERA LUCIA PEREIRA DA SILVA SALGADO', 280001607831)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (95, 'VOTO BRANCO', -1)
ON CONFLICT DO NOTHING;
INSERT INTO votacao_secao_candidato (nr_votavel, nm_votavel, sq_candidato)
VALUES (96, 'VOTO NULO', -1)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS votacao_secao
(
    id                         INT PRIMARY KEY             NOT NULL GENERATED ALWAYS AS IDENTITY,
    dt_hh_geracao              TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    ano_eleicao                INT                         NOT NULL,
    nr_turno                   INT                         NOT NULL,
    dt_eleicao                 DATE                        NOT NULL,
    sg_uf                      TEXT,
    sg_ue                      TEXT,
    nm_ue                      TEXT,
    cd_municipio               INTEGER,
    nm_municipio               TEXT,
    nr_zona                    INTEGER,
    nr_secao                   INTEGER,
    id_votacao_secao_cargo     INT                         NOT NULL,
    id_votacao_secao_candidato INT                         NOT NULL,
    qt_votos                   INTEGER,
    nr_local_votacao           INTEGER,
    nm_local_votacao           TEXT,
    ds_local_votacao_endereco  TEXT,
    id_votacao_secao_urna      INT DEFAULT NULL,
    FOREIGN KEY (id_votacao_secao_cargo) REFERENCES votacao_secao_cargo (id),
    FOREIGN KEY (id_votacao_secao_candidato) REFERENCES votacao_secao_candidato (id),
    FOREIGN KEY (id_votacao_secao_urna) REFERENCES votacao_secao_urna (id),
    UNIQUE (nr_turno, cd_municipio, nr_zona, nr_secao, nr_local_votacao, id_votacao_secao_candidato)
);

CREATE TABLE IF NOT EXISTS votacao_secao_controle
(
    id        INT PRIMARY KEY                     NOT NULL GENERATED ALWAYS AS IDENTITY,
    status    TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS votacao_secao_urna_controle
(
    id                 INT PRIMARY KEY                     NOT NULL GENERATED ALWAYS AS IDENTITY,
    status             TEXT,
    nome_arquivo_fonte TEXT,
    timestamp          TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);