-- Banco de regras do Validador de Certificados (SQLite)
--
-- linha          : as linhas de produção (A, B, C, D)
-- especificacao  : padrões de linha (coluna linha preenchida) e especificações de
--                  cliente (coluna linha vazia: valem em cima do padrão da linha da OP)
-- tolerancia     : uma linha por característica de cada especificação
--                  tipo 'fixa'    -> usa minimo e/ou maximo
--                  tipo 'nominal' -> usa percentual sobre o valor nominal da planilha

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
