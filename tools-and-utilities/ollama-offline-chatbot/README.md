# 💬 Ollama Local Chat

A clean, minimal chat interface built with Streamlit for having conversations with local LLMs through [Ollama](https://ollama.com/) — no API keys, no cloud, no data leaving your machine.

---

## Problem Statement

Modern LLM-based coding assistants significantly improve developer productivity, particularly when working with unfamiliar syntax, libraries, or workflows. However, most commonly used models are cloud-based and optimized for high capability rather than efficiency, often exceeding the actual needs of everyday regular development tasks.

In practice, lightweight and fast models can already provide sufficient utility for many programming use cases, especially when the primary requirement is rapid natural-language guidance rather than deep reasoning. This raises a practical question: how far can model size be reduced while still maintaining a useful coding assistant experience?

This project explores that trade-off by building and experimenting with a fully local LLM chat interface using Ollama. The goal is to evaluate whether smaller, efficient models (e.g. 8B-class models) can deliver a responsive and effective developer experience comparable to larger hosted systems, while offering the benefits of local execution such as privacy, speed, and offline availability.

--

## Features

- **Auto model detection** — pulls your locally available Ollama models and lets you switch between them via the sidebar
- **Real-time streaming** — responses stream token-by-token with a live cursor, just like a hosted chat UI
- **Persistent context** — full conversation history is kept in session state and sent with every request
- **Offline-first** — runs entirely on your local machine

---

## Requirements

- Python **3.8+**
- [Ollama](https://ollama.com/download) installed and running
- At least one model pulled (e.g. `ollama pull llama3`)

---

## Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd <project-folder>

# Install dependencies
pip install streamlit ollama
```

---

## Running the App

**Option 1 — Streamlit CLI** *(recommended)*

```bash
# Start Ollama if it isn't already running
ollama serve

# Launch the app
streamlit run app.py
```

**Option 2 — Convenience launcher**

`run_app.py` starts Streamlit programmatically, which is handy when running from an IDE or packaging with PyInstaller.

```bash
python run_app.py
```

Either way, open **http://localhost:8501** in your browser once the app starts.

---

## Project Structure

```
.
├── app.py          # Main Streamlit chat application
└── run_app.py      # Programmatic launcher for IDEs / packaging
```

---

## How It Works

1. **Model discovery** — on startup, `ollama.list()` fetches all locally pulled models and populates the sidebar dropdown.
2. **Message history** — each user and assistant turn is stored in `st.session_state.messages`, which is passed as context on every request.
3. **Streaming** — `ollama.chat(..., stream=True)` yields tokens one at a time; the UI appends each chunk and shows a `▌` cursor until the response is complete.
4. **History update** — the finished response is appended to session state so future turns have full context.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| *"Could not fetch models. Is Ollama running?"* | Run `ollama serve` in a separate terminal before launching the app. |
| Empty model dropdown | You have no models pulled. Run `ollama pull <model>`, e.g. `ollama pull llama3`. |
| Error generating response | Confirm the selected model is fully downloaded with `ollama list` and that Ollama is still running. |

---

## License

[MIT](LICENSE)
