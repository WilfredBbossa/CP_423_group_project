# CP_423_group_project
End-to-end conversational IR system for clinical interviews with speaker-aware indexing, retrieval, and evaluation. Uses Pyannote diarization, Whisper ASR, and n8n orchestration. CP423 W26 project.

# Clinical Interview IR System
Intelligent Clinical Interview Analysis, Summarization & Retrieval System with Speaker Separation

CP423 — Information Retrieval & Search Engines | Winter 2026

> ⚠️ This system is for educational purposes only. It must not be used for real medical diagnosis or treatment decisions.

---

## System Overview

This system processes spoken clinical interviews and enables structured summarization, symptom-based question answering, and automated interview analysis. It supports two modes:

- **Offline mode** — processes a pre-recorded audio file using Pyannote diarization and Whisper transcription
- **Live mode** — processes real-time audio streams using LiveKit speaker separation

The full offline pipeline flow:
```
User uploads audio → Flask API → Pyannote diarization → Whisper transcription
→ Alignment + role detection → Supabase indexing → MedGemma analysis → Frontend display
```

---

## Folder Structure
```
tbh
```
---

## Requirements

- Python 3.11
- Apple Silicon Mac (M1/M2/M3) for MedGemma local inference via MLX
- Docker (for n8n)
- ffmpeg (for audio conversion)

Install ffmpeg:
```bash
brew install ffmpeg
```

Install Docker from docker.com if you don't have it.

---

## API Keys Required

You need four API keys before running the system. All are free tier.

### Hugging Face
1. Create a free account at huggingface.co
2. Go to Settings → Access Tokens → New token (read access is enough)
3. Visit these pages and click "Agree and access repository" on each:
   - huggingface.co/pyannote/speaker-diarization-3.1
   - huggingface.co/pyannote/segmentation-3.0
4. Visit huggingface.co/google/medgemma-4b-it and accept the Health AI Developer Foundations terms

### Groq
1. Create a free account at console.groq.com
2. Go to API Keys and generate a new key

### Supabase
1. Create a free account at supabase.com
2. Create a new project
3. Go to Settings → API and copy the Project URL and anon public key

---

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd clinical-ir
```

### 2. Create and activate a virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install PyTorch first
```bash
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

### 4. Install remaining dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure your .env file
```bash
cp .env.example .env
```

Open `.env` and fill in your keys:
```
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_public_key
```

### 6. Set up the Supabase database

Go to your Supabase project → SQL Editor and run the following queries one at a time:

**Create the table:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE transcript_segments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT,
    speaker TEXT NOT NULL,
    role TEXT NOT NULL,
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE transcript_segments
ADD CONSTRAINT unique_segment
UNIQUE (session_id, start_time, end_time, text);
```

**Create the retrieval functions:**
```sql
CREATE OR REPLACE FUNCTION match_segments(
    query_embedding VECTOR(384),
    match_count INT,
    p_session_id TEXT
)
RETURNS TABLE (
    id UUID, speaker TEXT, role TEXT,
    start_time FLOAT, end_time FLOAT,
    text TEXT, similarity FLOAT
)
LANGUAGE SQL STABLE AS $$
    SELECT id, speaker, role, start_time, end_time, text,
           1 - (embedding <=> query_embedding) AS similarity
    FROM transcript_segments
    WHERE session_id = p_session_id
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
```
```sql
CREATE OR REPLACE FUNCTION match_patient_segments(
    query_embedding VECTOR(384),
    match_count INT,
    p_session_id TEXT
)
RETURNS TABLE (
    id UUID, speaker TEXT, role TEXT,
    start_time FLOAT, end_time FLOAT,
    text TEXT, similarity FLOAT
)
LANGUAGE SQL STABLE AS $$
    SELECT id, speaker, role, start_time, end_time, text,
           1 - (embedding <=> query_embedding) AS similarity
    FROM transcript_segments
    WHERE role = 'PATIENT'
    AND session_id = p_session_id
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
```
```sql
CREATE OR REPLACE FUNCTION match_clinician_segments(
    query_embedding VECTOR(384),
    match_count INT,
    p_session_id TEXT
)
RETURNS TABLE (
    id UUID, speaker TEXT, role TEXT,
    start_time FLOAT, end_time FLOAT,
    text TEXT, similarity FLOAT
)
LANGUAGE SQL STABLE AS $$
    SELECT id, speaker, role, start_time, end_time, text,
           1 - (embedding <=> query_embedding) AS similarity
    FROM transcript_segments
    WHERE role = 'CLINICIAN'
    AND session_id = p_session_id
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
```

### 7. Set up n8n

Start n8n in Docker:
```bash
docker start n8n
```

Go to `http://localhost:5678`, log in, and import the Clinical IR offline pipeline workflow. Make sure the workflow is activated — the toggle in the top right should be green.

---

## Running the System

### Start the Flask API
```bash
source venv/bin/activate
python app.py
```

### Open the frontend
Go to `http://localhost:5001` in your browser.

### Upload and process an interview
1. Click **Offline Mode**
2. Upload a `.wav`, `.mp3`, or `.m4a` audio file
3. Click **Process Interview**
4. Wait for the pipeline to complete — this takes 2-3 minutes
5. View the labeled transcript, MedGemma analysis, and search results

### Run the pipeline manually from terminal
```bash
python -m speaker_separation.offline.pipeline "audio/interview.wav"
```

### Run retrieval manually
```bash
python -m ir.retrieve "what symptoms does the patient have?" patient
```

### Run evaluation
```bash
python -m ir.evaluate
```

---
