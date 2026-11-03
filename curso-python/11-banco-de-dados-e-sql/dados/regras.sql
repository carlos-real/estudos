-- Banco de regras do Validador de Certificados (o mesmo do projeto final, módulo 14).
--
-- linha          as linhas de produção (A, B, C, D)
-- especificacao  padrões de linha (coluna linha preenchida) e especificações de
--                cliente (coluna linha vazia: valem por cima do padrão da linha da OP)
-- tolerancia     uma linha por característica de cada especificação
--                tipo 'fixa'    -> usa minimo e/ou maximo
--                tipo 'nominal' -> usa percentual sobre o valor nominal da planilha

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS linha (
    codigo    TEXT PRIMARY KEY CHECK (codigo IN ('A', 'B', 'C', 'D')),
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS especificacao (
    titulo TEXT PRIMARY KEY,
    texto  TEXT NOT NULL DEFAULT '',
    linha  TEXT REFERENCES linha (codigo)
);

-- Cada linha tem no máximo UM padrão
CREATE UNIQUE INDEX IF NOT EXISTS um_padrao_por_linha
    ON especificacao (linha) WHERE linha IS NOT NULL;

CREATE TABLE IF NOT EXISTS tolerancia (
    titulo         TEXT NOT NULL REFERENCES especificacao (titulo),
    caracteristica TEXT NOT NULL,
    tipo           TEXT NOT NULL CHECK (tipo IN ('fixa', 'nominal')),
    minimo         REAL,
    maximo         REAL,
    percentual     REAL,
    PRIMARY KEY (titulo, caracteristica)
);

INSERT INTO linha (codigo, descricao) VALUES
    ('A', 'Extrusora 1 - filmes PE monocamada'),
    ('B', 'Extrusora 2 - filmes PE finos'),
    ('C', 'Coextrusora 3 camadas'),
    ('D', 'Laminadora - PET/PE e BOPP/PE');

INSERT INTO especificacao (titulo, texto, linha) VALUES
    ('PADRAO-A', 'Padrão da linha A (filmes PE monocamada).', 'A'),
    ('PADRAO-B', 'Padrão da linha B (filmes PE finos).', 'B'),
    ('PADRAO-C', 'Padrão da linha C (coextrusados 3 camadas).', 'C'),
    ('PADRAO-D', 'Padrão da linha D (laminados).', 'D'),
    ('ESP-0412', 'Torrefação Serra - embalagem de café 250 g. COF interno de 0,18 a 0,25; selagem mínima 12 N/15mm.', NULL),
    ('ESP-0533', 'Agro Campo - sacaria de ração 15 kg. Espessura nominal ± 5%; tração mínima 28 MPa.', NULL),
    ('ESP-0618', 'Biscoitos Aurora - filme para biscoito. COF de 0,12 a 0,22; gramatura ± 5%.', NULL);

INSERT INTO tolerancia (titulo, caracteristica, tipo, minimo, maximo, percentual) VALUES
    ('PADRAO-A', 'espessura', 'nominal', NULL, NULL, 10.0),
    ('PADRAO-A', 'gramatura', 'nominal', NULL, NULL, 10.0),
    ('PADRAO-A', 'cof', 'fixa', 0.15, 0.35, NULL),
    ('PADRAO-A', 'tracao', 'fixa', 20.0, NULL, NULL),
    ('PADRAO-A', 'selagem', 'fixa', 8.0, NULL, NULL),
    ('PADRAO-B', 'espessura', 'nominal', NULL, NULL, 10.0),
    ('PADRAO-B', 'gramatura', 'nominal', NULL, NULL, 10.0),
    ('PADRAO-B', 'cof', 'fixa', 0.20, 0.40, NULL),
    ('PADRAO-B', 'tracao', 'fixa', 18.0, NULL, NULL),
    ('PADRAO-B', 'selagem', 'fixa', 6.0, NULL, NULL),
    ('PADRAO-C', 'espessura', 'nominal', NULL, NULL, 8.0),
    ('PADRAO-C', 'gramatura', 'nominal', NULL, NULL, 8.0),
    ('PADRAO-C', 'cof', 'fixa', 0.10, 0.30, NULL),
    ('PADRAO-C', 'tracao', 'fixa', 25.0, NULL, NULL),
    ('PADRAO-C', 'selagem', 'fixa', 10.0, NULL, NULL),
    ('PADRAO-D', 'espessura', 'nominal', NULL, NULL, 7.0),
    ('PADRAO-D', 'gramatura', 'nominal', NULL, NULL, 7.0),
    ('PADRAO-D', 'cof', 'fixa', 0.15, 0.30, NULL),
    ('PADRAO-D', 'tracao', 'fixa', 30.0, NULL, NULL),
    ('PADRAO-D', 'selagem', 'fixa', 12.0, NULL, NULL),
    ('ESP-0412', 'cof', 'fixa', 0.18, 0.25, NULL),
    ('ESP-0412', 'selagem', 'fixa', 12.0, NULL, NULL),
    ('ESP-0533', 'espessura', 'nominal', NULL, NULL, 5.0),
    ('ESP-0533', 'tracao', 'fixa', 28.0, NULL, NULL),
    ('ESP-0618', 'cof', 'fixa', 0.12, 0.22, NULL),
    ('ESP-0618', 'gramatura', 'nominal', NULL, NULL, 5.0);
