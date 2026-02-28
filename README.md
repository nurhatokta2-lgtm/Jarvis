# Jarvis Ultra — Gemini + Ada Voice AI Assistant

Jarvis Ultra is a production-oriented AI assistant stack that combines a Gemini-backed reasoning engine, Ada-style voice synthesis, plugin extensibility, session memory, and analytics.

## 1) Feature Summary & Repository Comparison

> **Important environment note**: The execution environment blocks outbound access to GitHub (`CONNECT tunnel failed: 403`), so direct deep-clone analysis of `FatihMakes/Mark-X.1` and `nazirlouis/ada_v2` could not be completed here.

### Intended Merge Strategy
Given the user requirements and typical structures of these projects:

- **Mark-X.1-derived capabilities (assistant orchestration focus)**
  - Conversation management and context retention
  - API-first assistant backend
  - Error handling and observability
- **ada_v2-derived capabilities (voice focus)**
  - Voice synthesis and voice-oriented UX
  - Speech-centered interactions

### Implemented merged superset in this repo
- Gemini-based backend provider abstraction (`LLMProvider` + `GeminiProvider`)
- Ada voice synthesis service (`AdaTTSService`) using configurable Ada-compatible voice
- Text + voice interaction web UI
- Pluggable extension framework (`Plugin`, `PluginRegistry`)
- Built-in sentiment plugin example
- Durable analytics store (SQLite)
- Structured FastAPI routes for health/chat/analytics/audio
- Fallback mode when Gemini key is unavailable (for local reliability)

## 2) Merged Architecture

```text
[Browser UI: text+voice] --> [/api/chat FastAPI] --> [AssistantEngine]
                                              |--> [PluginRegistry]
                                              |--> [ConversationMemory]
                                              |--> [GeminiProvider]
                                              |--> [AdaTTSService]
                                              '--> [AnalyticsStore(SQLite)]
```

### Core Decisions
- **Provider abstraction first**: LLM/TTS are isolated services so new providers can be added without changing API routes.
- **Safe degradation**: Gemini key missing? assistant still runs in fallback mode for dev/test.
- **Plugin system**: Feature growth via `app/plugins` without touching orchestration core.
- **Operational readiness**: Logging + analytics + health checks included by default.

## 3) Project Structure

```bash
app/
  api/routes.py           # REST endpoints
  core/config.py          # settings/env
  core/errors.py          # domain exceptions
  core/logging.py         # logging setup
  models/schemas.py       # pydantic contracts
  plugins/base.py         # plugin interface
  plugins/registry.py     # plugin manager
  plugins/sentiment.py    # sample plugin
  services/ai_provider.py # Gemini provider abstraction
  services/assistant.py   # orchestration engine
  services/analytics.py   # sqlite analytics
  services/memory.py      # session memory
  services/tts.py         # Ada voice synthesis
  ui/index.html           # modular text+voice web UI
  main.py                 # FastAPI app entry
tests/
scripts/demo_chat.sh
```

## 4) Installation & Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
ADA_VOICE_NAME=en-US-AvaMultilingualNeural
APP_ENV=dev
LOG_LEVEL=INFO
```

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## 5) How to Use Ada Voice

1. Keep `use_voice=true` in `/api/chat` requests.
2. The backend synthesizes assistant replies using `AdaTTSService`.
3. Audio is served from `/api/audio/{file}` and auto-played by UI.
4. To swap voice variant, change `ADA_VOICE_NAME` in `.env`.

## 6) API Quick Reference

- `GET /api/health`
- `POST /api/chat`
- `GET /api/analytics`
- `GET /api/audio/{file_name}`

Sample request:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"demo","message":"Plan my week","use_voice":true}'
```

## 7) Testing

```bash
pytest -q
```

## 8) Extensibility

To add a plugin:
1. Create a class implementing `Plugin` in `app/plugins/`.
2. Register it in `app/main_state.py`.
3. Its output appears in `plugin_data` in `/api/chat` response.

---

If outbound GitHub/network access is restored, this README can be expanded with a line-by-line repository feature matrix and exact provenance mapping of each merged module.
