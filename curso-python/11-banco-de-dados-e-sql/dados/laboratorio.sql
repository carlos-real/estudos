-- Banco de exemplo do módulo 11: o laboratório de qualidade (dados fictícios).
--
-- linha      as linhas de produção (A, B, C, D)
-- cliente    quem compra
-- op         ordens de produção (cada OP é de uma linha e de um cliente)
-- ensaio     cada medição feita numa bobina de uma OP
-- expedicao  cargas que saíram (OP, nota fiscal e peso), como nos e-mails da expedição
--
-- Datas ficam como TEXTO no formato ISO 'AAAA-MM-DD': ordena certo e compara certo.

PRAGMA foreign_keys = ON;

CREATE TABLE linha (
    codigo    TEXT PRIMARY KEY,
    descricao TEXT NOT NULL
);

CREATE TABLE cliente (
    id     INTEGER PRIMARY KEY,
    nome   TEXT NOT NULL UNIQUE,
    cidade TEXT,
    uf     TEXT
);

CREATE TABLE op (
    numero        INTEGER PRIMARY KEY,
    linha         TEXT    NOT NULL REFERENCES linha (codigo),
    cliente_id    INTEGER NOT NULL REFERENCES cliente (id),
    produto       TEXT    NOT NULL,
    especificacao TEXT,                          -- NULL = usa o padrão da linha
    emissao       TEXT    NOT NULL,              -- 'AAAA-MM-DD'
    quantidade_kg REAL    NOT NULL CHECK (quantidade_kg > 0),
    status        TEXT    NOT NULL DEFAULT 'ABERTA'
                  CHECK (status IN ('ABERTA', 'LIBERADA', 'BLOQUEADA', 'CERTIFICADA'))
);

CREATE TABLE ensaio (
    id             INTEGER PRIMARY KEY,
    op             INTEGER NOT NULL REFERENCES op (numero),
    bobina         INTEGER NOT NULL,
    caracteristica TEXT    NOT NULL,             -- espessura, gramatura, cof
    valor          REAL,                         -- NULL = ainda não medido
    resultado      TEXT CHECK (resultado IN ('OK', 'FORA')),
    data           TEXT    NOT NULL
);

CREATE TABLE expedicao (
    id      INTEGER PRIMARY KEY,
    op      INTEGER NOT NULL REFERENCES op (numero),
    nf      TEXT    NOT NULL,
    peso_kg REAL    NOT NULL CHECK (peso_kg > 0),
    data    TEXT    NOT NULL
);

INSERT INTO linha (codigo, descricao) VALUES
    ('A', 'Extrusora 1 - filmes PE monocamada'),
    ('B', 'Extrusora 2 - filmes PE finos'),
    ('C', 'Coextrusora 3 camadas'),
    ('D', 'Laminadora - PET/PE e BOPP/PE');

INSERT INTO cliente (id, nome, cidade, uf) VALUES
    (1, 'Torrefação Serra Ltda', 'Franca', 'SP'),
    (2, 'Agro Campo S.A.', 'Rio Verde', 'GO'),
    (3, 'Biscoitos Aurora', 'Marília', 'SP'),
    (4, 'Laticínios Serra Azul', 'Juiz de Fora', 'MG'),
    (5, 'Higiene Bem-Estar S.A.', 'Joinville', 'SC'),
    (6, 'Café do Vale', 'Varginha', 'MG');

INSERT INTO op (numero, linha, cliente_id, produto, especificacao, emissao, quantidade_kg, status) VALUES
    (24518, 'A', 1, 'Filme PE 40 µm transparente', NULL,       '2026-10-20', 4500, 'LIBERADA'),
    (24519, 'A', 3, 'Filme PE 40 µm transparente', NULL,       '2026-10-20', 3000, 'BLOQUEADA'),
    (24520, 'A', 2, 'Filme PE 50 µm branco',       NULL,       '2026-10-21', 5200, 'LIBERADA'),
    (24521, 'A', 2, 'Filme PE 60 µm sacaria',      'ESP-0533', '2026-10-21', 6000, 'LIBERADA'),
    (24527, 'B', 4, 'Filme PE 35 µm',              NULL,       '2026-10-21', 2500, 'BLOQUEADA'),
    (24528, 'B', 5, 'Filme PE 35 µm',              NULL,       '2026-10-22', 2800, 'CERTIFICADA'),
    (24533, 'C', 3, 'Coextrusado 70 µm',           'ESP-0618', '2026-10-22', 3500, 'BLOQUEADA'),
    (24534, 'C', 1, 'Coextrusado 70 µm',           NULL,       '2026-10-23', 3200, 'ABERTA'),
    (24541, 'D', 1, 'Laminado PET/PE 62 µm',       'ESP-0412', '2026-10-23', 4000, 'LIBERADA'),
    (24546, 'D', 4, 'Laminado BOPP/PE 55 µm',      NULL,       '2026-10-24', 3800, 'BLOQUEADA'),
    (24550, 'B', 5, 'Filme PE 35 µm',              NULL,       '2026-10-26', 2600, 'ABERTA'),
    (24551, 'D', 2, 'Laminado PET/PE 62 µm',       NULL,       '2026-10-27', 4100, 'ABERTA');

INSERT INTO ensaio (op, bobina, caracteristica, valor, resultado, data) VALUES
    (24518, 1, 'espessura', 38.8, 'OK', '2026-10-21'),
    (24518, 1, 'gramatura', 37.3, 'OK', '2026-10-21'),
    (24518, 1, 'cof', 0.31, 'OK', '2026-10-21'),
    (24518, 2, 'espessura', 38.8, 'OK', '2026-10-21'),
    (24518, 2, 'gramatura', 37.2, 'OK', '2026-10-21'),
    (24518, 2, 'cof', 0.26, 'OK', '2026-10-21'),
    (24519, 1, 'espessura', 40.5, 'OK', '2026-10-21'),
    (24519, 1, 'gramatura', 38.0, 'OK', '2026-10-21'),
    (24519, 1, 'cof', 0.26, 'OK', '2026-10-21'),
    (24519, 2, 'espessura', 44.8, 'FORA', '2026-10-21'),
    (24519, 2, 'gramatura', 36.6, 'OK', '2026-10-21'),
    (24519, 2, 'cof', 0.22, 'OK', '2026-10-21'),
    (24520, 1, 'espessura', 51.9, 'OK', '2026-10-22'),
    (24520, 1, 'gramatura', 47.4, 'OK', '2026-10-22'),
    (24520, 1, 'cof', 0.27, 'OK', '2026-10-22'),
    (24520, 2, 'espessura', 53.4, 'OK', '2026-10-22'),
    (24520, 2, 'gramatura', 47.2, 'OK', '2026-10-22'),
    (24520, 2, 'cof', 0.31, 'OK', '2026-10-22'),
    (24521, 1, 'espessura', 58.8, 'OK', '2026-10-22'),
    (24521, 1, 'gramatura', 53.9, 'OK', '2026-10-22'),
    (24521, 1, 'cof', 0.19, 'OK', '2026-10-22'),
    (24521, 2, 'espessura', 61.8, 'OK', '2026-10-22'),
    (24521, 2, 'gramatura', 55.7, 'OK', '2026-10-22'),
    (24521, 2, 'cof', 0.18, 'OK', '2026-10-22'),
    (24527, 1, 'espessura', 35.2, 'OK', '2026-10-22'),
    (24527, 1, 'gramatura', 33.0, 'OK', '2026-10-22'),
    (24527, 1, 'cof', 0.43, 'FORA', '2026-10-22'),
    (24527, 2, 'espessura', 34.1, 'OK', '2026-10-22'),
    (24527, 2, 'gramatura', 32.6, 'OK', '2026-10-22'),
    (24527, 2, 'cof', 0.35, 'OK', '2026-10-22'),
    (24528, 1, 'espessura', 33.8, 'OK', '2026-10-23'),
    (24528, 1, 'gramatura', 32.3, 'OK', '2026-10-23'),
    (24528, 1, 'cof', 0.29, 'OK', '2026-10-23'),
    (24528, 2, 'espessura', 34.5, 'OK', '2026-10-23'),
    (24528, 2, 'gramatura', 31.6, 'OK', '2026-10-23'),
    (24528, 2, 'cof', 0.26, 'OK', '2026-10-23'),
    (24533, 1, 'espessura', 75.8, 'FORA', '2026-10-23'),
    (24533, 1, 'gramatura', 64.9, 'OK', '2026-10-23'),
    (24533, 1, 'cof', 0.24, 'FORA', '2026-10-23'),
    (24533, 2, 'espessura', 69.6, 'OK', '2026-10-23'),
    (24533, 2, 'gramatura', 63.6, 'OK', '2026-10-23'),
    (24533, 2, 'cof', 0.15, 'OK', '2026-10-23'),
    (24534, 1, 'espessura', 69.8, 'OK', '2026-10-24'),
    (24534, 1, 'gramatura', 65.6, 'OK', '2026-10-24'),
    (24534, 1, 'cof', 0.23, 'OK', '2026-10-24'),
    (24534, 2, 'espessura', 67.3, 'OK', '2026-10-24'),
    (24534, 2, 'gramatura', 66.8, 'OK', '2026-10-24'),
    (24534, 2, 'cof', NULL, NULL, '2026-10-24'),
    (24541, 1, 'espessura', 64.9, 'OK', '2026-10-24'),
    (24541, 1, 'gramatura', 61.9, 'OK', '2026-10-24'),
    (24541, 1, 'cof', 0.20, 'OK', '2026-10-24'),
    (24541, 2, 'espessura', 62.9, 'OK', '2026-10-24'),
    (24541, 2, 'gramatura', 66.0, 'OK', '2026-10-24'),
    (24541, 2, 'cof', 0.21, 'OK', '2026-10-24'),
    (24546, 1, 'espessura', 51.0, 'FORA', '2026-10-26'),
    (24546, 1, 'gramatura', 50.8, 'OK', '2026-10-26'),
    (24546, 1, 'cof', 0.18, 'OK', '2026-10-26'),
    (24546, 2, 'espessura', 53.4, 'OK', '2026-10-26'),
    (24546, 2, 'gramatura', 55.1, 'FORA', '2026-10-26'),
    (24546, 2, 'cof', 0.20, 'OK', '2026-10-26');

INSERT INTO expedicao (op, nf, peso_kg, data) VALUES
    (24518, '123456', 1250.5, '2026-10-27'),
    (24518, '123470', 1830.0, '2026-10-28'),
    (24520, '123458', 2400.0, '2026-10-27'),
    (24521, '123459', 2950.0, '2026-10-28'),
    (24528, '123452', 1300.0, '2026-10-25'),
    (24528, '123453', 1450.5, '2026-10-26'),
    (24541, '123465', 2000.25, '2026-10-29'),
    (24541, '123466', 1750.0, '2026-10-29');
