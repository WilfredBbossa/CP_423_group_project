# 🩺 Clinical Interview Analysis & Retrieval System

An end-to-end conversational medical interview IR system with speaker separation, diarization, and speaker-aware retrieval.

> ⚠️ **Educational use only.** This system does **not** provide medical diagnoses or treatment recommendations.

---

## 📖 Overview

Clinical interviews are conversational, multi-speaker, and unstructured. This project builds a full **conversational Information Retrieval system** that:

1. Ingests spoken clinical interviews (offline audio or real-time streams)
2. Separates speakers using **Pyannote** (offline) or **LiveKit** (real-time)
3. Transcribes audio with **Whisper** (via Groq API)
4. Indexes transcript segments with **speaker metadata**
5. Retrieves and ranks relevant segments
6. Generates grounded **LLM explanations** for summarization, Q&A, and interview analysis

Supports **offline** and **real-time** modes, evaluated with **Precision@K** and **Recall@K**.

---

## ✨ Features

- 🎙️ Speaker diarization with Pyannote (offline)
- 📡 Real-time speaker separation with LiveKit
- 📝 Speech-to-text via Whisper (Groq API)
- 🔍 Speaker-aware indexing (patient / clinician / combined)
- 🤖 Three retrieval modules: summarization, symptom Q&A, interview analyzer
- 📊 Retrieval evaluation with Precision@K & Recall@K
- 🌐 Web frontend for uploads, live chat, and LLM output
- 🧩 n8n workflows for orchestration

---

## 🏗️ Architecture

**Offline Mode**
```
Audio → Pyannote Diarization → Whisper Transcription → Indexing → Retrieval → LLM Analysis
```

**Live Mode**
```
LiveKit Streams → Speaker-Separated Audio → Whisper → Indexing → Retrieval → LLM Analysis
```

---

## 🧰 Tech Stack

| Component | Tool |
|---|---|
| Workflow orchestration | n8n (self-hosted) |
| Speech-to-text | Whisper via Groq API |
| Speaker diarization | Pyannote.audio |
| Real-time audio | LiveKit |
| Embeddings / LLMs | Hugging Face open-source models |
| Database / vector store | Supabase |
| Frontend | HTML / CSS / JavaScript |

> 🚫 Only **free-tier** tools and APIs are used.

---


## 🔐 Environment Setup

```bash
cp .env.example .env
```

**`.env.example`**
```env
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_TOKEN=your_hf_token_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
LIVEKIT_URL=wss://your-livekit-instance.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
N8N_WEBHOOK_URL=http://localhost:5678/webhook
```

> 🔒 Never commit `.env` or expose keys in videos/screenshots.

---

## 🔑 Free-Tier API Setup

| Service | Where to get it |
|---|---|
| Groq (Whisper) | [console.groq.com](https://console.groq.com) → API Keys |
| Hugging Face | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| Pyannote | Accept terms on [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) |
| Supabase | [supabase.com](https://supabase.com) → Settings → API |
| LiveKit Cloud | [cloud.livekit.io](https://cloud.livekit.io) → Settings → Keys |
| n8n | Self-host with `npx n8n` |

---

## 🚀 Running

**Offline pipeline**
```bash
python -m src.ingestion.audio_loader --input data/raw_audio/interview_01.wav
python -m src.diarization.pyannote_pipeline --audio data/raw_audio/interview_01.wav
python -m src.transcription.whisper_groq --audio data/raw_audio/interview_01.wav
python -m src.indexing.speaker_indexer --transcript data/transcripts/interview_01.json
```

**Frontend**
```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000
```

**Live mode**
```bash
python -m src.ingestion.livekit_consumer
```

**Evaluation**
```bash
python -m src.evaluation.evaluate --labels data/relevance_labels/labels.json --k 1 3 5 10
```

---

## 🎙️ Speaker Separation

**Pyannote (offline)**
- Input: single mixed audio file
- Output: speaker-labeled time segments
- Whisper segments aligned to diarized intervals
- Labels `SPEAKER_0` / `SPEAKER_1` → mapped to `PATIENT` / `CLINICIAN`

**LiveKit (real-time)**
- Each participant gets an isolated audio track (no diarization needed)
- Tracks forwarded to n8n via webhooks / egress
- Each track transcribed independently with Whisper

---

## 🔍 Retrieval & Evaluation

**Indexes:** patient-only, clinician-only, combined (optional speaker-conditioned embeddings)

**Modules:**
1. Clinical Interview Summarization
2. Symptom-Based Question Answering
3. Automated Interview Analyzer

**Metrics:** Precision@K and Recall@K reported for **overall**, **patient-only**, and **clinician-only** retrieval.

Example output:
```
K=5 | Overall P@5=0.82 R@5=0.74 | Patient P@5=0.88 R@5=0.79 | Clinician P@5=0.76 R@5=0.69
```


## ⚖️ Ethics & Limitations

- Educational use only
- No medical diagnoses or treatment recommendations
- All outputs explainable, traceable, and ethically framed
- Free-tier tools only — no paid/commercial medical systems

---

## 📚 References

- [Pyannote.audio](https://github.com/pyannote/pyannote-audio)
- [Groq Whisper API](https://console.groq.com/docs/speech-to-text)
- [LiveKit Docs](https://docs.livekit.io/)
- [n8n Docs](https://docs.n8n.io/)
- [Supabase Docs](https://supabase.com/docs)
- [Hugging Face Models](https://huggingface.co/models)

---


**Course:** CP423 – Information Retrieval & Search Engines (W26)

---

## 📄 License

Released for educational purposes only as part of the CP423 course. Not for clinical or commercial use.
