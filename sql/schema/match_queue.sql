CREATE TABLE IF NOT EXISTS match_queue (
    match_id TEXT PRIMARY KEY,

    discovered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    fetched_at TIMESTAMP,

    -- pending | processing | done | error
    status TEXT NOT NULL DEFAULT 'pending',

    discovered_from_puuid TEXT,

    -- Optional FK if you want strict integrity
    FOREIGN KEY (discovered_from_puuid)
        REFERENCES accounts(puuid)
        ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_match_queue_status
    ON match_queue(status);