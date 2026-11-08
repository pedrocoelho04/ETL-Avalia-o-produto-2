-- Tabela que guarda as leituras dos sensores enviadas pelo NiFi
CREATE TABLE IF NOT EXISTS leituras_sensor (
    id          BIGSERIAL PRIMARY KEY,
    id_sensor   INTEGER NOT NULL CHECK (id_sensor BETWEEN 100 AND 105),
    localizacao VARCHAR(100) NOT NULL,
    latitude    NUMERIC(9,6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude   NUMERIC(9,6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    data        DATE NOT NULL,
    hora        TIME NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'active',
    recebido_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_leituras_sensor_data ON leituras_sensor (id_sensor, data);
CREATE INDEX IF NOT EXISTS idx_leituras_status ON leituras_sensor (status);
