# AI - Data Engineering - Portfolio 🚀

Welcome to my central workspace. This repository serves as a unified monorepo housing a diverse collection of data engineering architectures, AI-powered applications, and local productivity utilities.

Each application is self-contained with its own dependency environments and individual documentation.

---

## 📂 Repository Architecture

The workspace is organized into logical domains to separate core application architectures from lightweight utilities:

* **`core-apps/`**: Robust, flagship applications featuring advanced integrations.
* **`data-engineering/`**: End-to-end data pipelines, schemas, and optimized database architectures.
* **`tools-and-utilities/`**: Streamlined local helpers, productivity tools, and automation scripts.

---

## 🛠️ Project Portfolio

| Application Directory | Domain | Primary Tech Stack | Status |
| :--- | :--- | :--- | :--- |
| [**`core-apps/localcloud-llm`**](./core-apps/localcloud-llm) | Artificial Intelligence | Streamlit, Ollama, Google Gemini API, Python | 🌟 Active |
| [`data-engineering/advanced-database-architecture`](./data-engineering/advanced-database-architecture) | Data Engineering | ETL, MySQL, MongoDB, Parquet | Completed |
| [`tools-and-utilities/deutsch-vocabulary-assistant`](./tools-and-utilities/deutsch-vocabulary-assistant) | EdTech / Language | Streamlit, MongoDB, Python | Stable |
| [`tools-and-utilities/pdf-rag-bot`](./tools-and-utilities/pdf-rag-bot) | AI / Knowledge Base | Gemini API | Stable |
| [`tools-and-utilities/ollama-offline-chatbot`](./tools-and-utilities/ollama-offline-chatbot) | AI / Privacy | Streamlit, Local Ollama (Gemma/Llama) | Stable |
| [`tools-and-utilities/streamlit-time-tracker`](./tools-and-utilities/streamlit-time-tracker) | Productivity | Streamlit, Python | Lightweight |

---

## 💡 Highlighted Project: LocalCloud LLM

The flagship application in this suite is **LocalCloud LLM**, a hybrid interface providing unified access to both edge and cloud-based language models.

* **Smart Orchestration:** Dynamically toggles execution context between lightweight offline instances (via Ollama) and powerful remote processing (via Google's Gemini API).
* **Production Layout:** Outfitted with structural source separation (`/src`), environment configurations, and isolated operational logic.
* **Deep Dive:** For full deployment, architectural details, and configuration instructions, check out the dedicated [LocalCloud LLM Readme](./core-apps/localcloud-llm/README.md).

---

## ⚙️ Local Development & Setup

Since this is a monorepo, it is highly recommended to manage individual virtual environments per application rather than installing dependencies globally.

1. Navigate to the specific project directory:
   ```bash
   cd tools-and-utilities/deutsch-vocabulary-assistant

2. Initialize and activate an isolated environment (e.g., using venv or conda):
     ```
     python3 -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```

3. Install the specialized requirements:
     ```
     pip install -r requirements.txt
     ```

