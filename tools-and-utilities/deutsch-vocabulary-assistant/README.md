# 🇩🇪 Deutsch Vocabulary Learning Assistant

A Streamlit app for building and quizzing yourself on a personal German vocabulary database, backed by MongoDB.

---

## Problem Statement
When learning German, I found myself writing down new verbs and words as I encountered them but the notes would pile up and actually revisiting them was a pain. There was no real mechanism forcing me to recall anything; I'd just passively re-read a list.  

For a while I managed this with a manual Excel sheet, which worked but was clunky and not exactly built for active recall. What I really wanted was something that would quiz me, pull a random word from my list and make me retrieve the translation from memory before revealing the answer.  
That kind of active recall, even if imperfect, keeps things fresher than passive review.  

Is this the most efficient way to learn a language? Probably not. But it's a genuine improvement over a static spreadsheet, and it scratches the itch perfectly. If you're in a similar situation, scribbling vocab into notes or spreadsheets and never really drilling it, give this a try. All you need is a free MongoDB account and you're good to go.

---

## Features

- **Add Vocabulary** — Save German words with translations, verb forms, example sentences, and dictionary links.
- **Quiz Mode** — Test yourself with randomly drawn words from your database and get instant feedback.
- **Three Collections** — Organise your vocabulary into verbs (`verben`), general words (`worte`), and nouns (`nomen`).

---

## Requirements

- Python 3
- A running MongoDB instance (local or hosted, e.g. MongoDB Atlas)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pymongo python-dotenv
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
   ```
   The app connects to a database named `deutsch` automatically.

---

## Running the App

```bash
streamlit run app.py
```

---

## Usage

### Add Vocabulary

1. Select **Add Vocabulary** from the sidebar.
2. Choose a target collection: `verben`, `worte`, or `nomen`.
3. Fill in all fields:

   | Field | Description |
   |---|---|
   | Word (German) | The German word |
   | English Translations | Comma-separated (e.g. `to go, to walk`) |
   | Example Sentence (DE) | A sentence using the word in German |
   | Dictionary Link | Link to Duden or similar |
   | Infinitiv | Base verb form |
   | Präteritum | Simple past form |
   | Partizip II | Past participle |
   | Hilfsverb (Perfekt) | `haben` or `sein` |

4. Click **Load to Database**. Duplicate words are rejected automatically.

### Quiz Mode

1. Select **Quiz Mode** from the sidebar.
2. Choose which collection to quiz from.
3. Click **Get Random Word / Skip** to draw a word.
4. Type your English translation and click **Check Answer** (or press Enter).
5. Feedback, all valid translations, and an example sentence are shown on correct answers.

---

## Data Structure

Each document stored in MongoDB follows this schema:

```json
{
  "word_id": 1,
  "word": "gehen",
  "translations": ["to go", "to walk"],
  "forms": {
    "infinitiv": "gehen",
    "partizip_II": "gegangen",
    "praeteritum": "ging"
  },
  "hilfsverben": {
    "perfekt": "sein"
  },
  "example": {
    "de": "Ich gehe jeden Tag spazieren."
  },
  "dictionary_link": "https://www.duden.de/rechtschreibung/gehen"
}
```

---

## Project Structure

```
.
├── app.py          # Main Streamlit application
├── run_app.py      # Programmatic launcher for IDEs / packaging
├── .env            # Environment variables (not committed to version control)
└── README.md
```

---

## Notes

- The `.env` file should be added to `.gitignore` to keep your credentials safe.
- Answer checking is case-insensitive, so `To Go`, `to go`, and `TO GO` are all accepted.
- `word_id` is auto-incremented based on the highest existing ID in each collection.
- This is a work in progress, I have uploaded to git to keep a backup
