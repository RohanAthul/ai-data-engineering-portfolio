# ⚡ LocalCloud LLM

A lightweight Streamlit chat interface that lets you switch seamlessly between **private local models** (via Ollama) and **cloud-based inference** (Google Gemini) — all from a single UI.

---

## ✨ Features

- 🔀 **Dual-mode inference** — toggle between locally-hosted models and Google Gemini without leaving the app
- 🌊 **Streaming responses** — typewriter-style token streaming with a live cursor indicator
- 📊 **Performance diagnostics** — per-response metrics including inference time, token speed (t/s), and prompt/response token counts
- 🧠 **Persistent chat history** — conversation memory survives Streamlit page re-runs via `st.session_state`
- 🎛️ **Configurable generation parameters** — control temperature, top-p, and max tokens cap from the sidebar
- 🎨 **Custom theming** — gradient title, styled metric cards, and minimal dark-mode-friendly UI overrides

---

## 🗂️ Project Structure

```
LocalCloud LLM/
├── README.md
├── app.py            # Main Streamlit application — UI, routing, chat loop
├── backend.py        # AI backend — Ollama and Gemini API integrations
├── requirements.txt  # Python dependencies
├── sidebar.py        # Sidebar component — model selection and parameter controls
└── run_app.py        # Entry point script to launch the app
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally (for local model support)
- A Google Gemini API key (for cloud mode)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/LocalCloud-LLM.git
cd LocalCloud-LLM

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running the App

```bash
python run_app.py
# or directly:
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## ⚙️ Configuration

All runtime parameters are controlled from the sidebar:

| Parameter | Description |
|---|---|
| **Provider** | `Local models` (Ollama) or `Google Gemini` |
| **Model** | Auto-populated based on provider selection |
| **Temperature** | Sampling temperature — controls response creativity |
| **Top-p** | Nucleus sampling threshold |
| **Max tokens** | Maximum response length |
| **Stream output** | Enable/disable token-by-token streaming |

---

## 🧩 How It Works

### Inference Routing

`app.py` acts as the orchestration layer. After the user submits a prompt, the app routes to one of two inference branches:

**Local Engine (Ollama)**
- Calls `backend.generate_local_response()` with the selected model and parameters
- In streaming mode, iterates over token chunks and updates the UI in real time
- Extracts hardware performance metrics from the final chunk (`eval_duration`, `eval_count`, `prompt_eval_count`)
- Displays tokens-per-second, total inference time, and prompt/response token counts

**Cloud Engine (Google Gemini)**
- Calls `backend.generate_gemini_response()` against the Gemini API
- Supports streaming via the Gemini SDK's chunk iterator
- Displays API round-trip latency and inference node info

### Chat Memory

Conversation history is stored in `st.session_state.messages` as a list of `{"role": ..., "content": ...}` dicts. This list is passed in full to the backend on every turn, providing multi-turn context to both local and cloud models.

---

## 📊 Performance Diagnostics

Each response expands an optional **Performance Diagnostics** panel:

**Local Engine metrics:**
- ⏱️ Total inference time (wall clock)
- ⚡ Token generation speed (tokens/second)
- 🪙 Prompt tokens in / response tokens out

**Cloud Engine metrics:**
- ⏱️ API round-trip latency
- ☁️ Inference node identifier

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 📦 Dependencies

See `requirements.txt` for the full list. Key packages include:

- `streamlit` — UI framework
- `ollama` — local model inference client
- `google-generativeai` — Google Gemini SDK

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT
