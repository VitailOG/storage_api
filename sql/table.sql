CREATE TABLE IF NOT EXISTS file_info (
    id bigserial PRIMARY KEY,
    filename VARCHAR(255),
    content_type VARCHAR(255),
    size BIGINT,
    content BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_id ON file_info (id);
