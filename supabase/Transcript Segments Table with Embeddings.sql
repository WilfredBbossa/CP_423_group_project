CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE transcript_segments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    speaker TEXT NOT NULL,
    role TEXT NOT NULL,
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT NOW()
);
