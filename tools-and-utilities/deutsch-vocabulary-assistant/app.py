import streamlit as st
import pymongo
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

@st.cache_resource
def init_connection():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        st.error("MONGODB_URI not found in .env file")
        st.stop()
    return pymongo.MongoClient(uri)

client = init_connection()
db = client["deutsch"]

# --- STATE MANAGEMENT ---
# Initialize session state variables for the quiz
if "quiz_word" not in st.session_state:
    st.session_state.quiz_word = None
if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = None

def fetch_new_word(collection_name):
    """Fetches a random word using MongoDB's $sample aggregation."""
    col = db[collection_name]
    cursor = col.aggregate([{"$sample": {"size": 1}}])
    docs = list(cursor)
    
    if docs:
        st.session_state.quiz_word = docs[0]
        st.session_state.quiz_feedback = None # Reset feedback for the new word
    else:
        st.session_state.quiz_word = None
        st.error(f"No words found in the '{collection_name}' collection.")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose Mode:", ["Add Vocabulary", "Quiz Mode"])

# ==========================================
# MODE 1: ADD VOCABULARY
# ==========================================
if app_mode == "Add Vocabulary":
    st.title("Deutsch Vocabulary Manager")

    collection_name = st.radio(
        "Target Collection:",
        options=["verben", "worte", "nomen"],
        horizontal=True,
        key="col_selector",
        index=None
    )

    if collection_name is None:
        st.info("Please select a target collection to start adding vocabulary.")
    else:
        collection = db[collection_name]

        with st.form("vocab_form", clear_on_submit=True):
            st.subheader(f"General Information ({collection_name})")
            word_val = st.text_input("Word (German)", key="input_word")
            translation_raw = st.text_input("English Translations (separate with commas)", key="input_trans")
            example_de = st.text_input("Example Sentence (DE)", key="input_ex")
            duden_link = st.text_input("Dictionary Link", key="input_link")

            st.divider()
            
            st.subheader("Forms & Auxiliary")
            f1, f2, f3, f4 = st.columns(4)
            infinitiv = f1.text_input("Infinitiv", key="input_inf")
            praeteritum = f2.text_input("Präteritum", key="input_praet")
            partizip_ii = f3.text_input("Partizip II", key="input_p2")
            perfekt_aux = f4.selectbox("Hilfsverb (Perfekt)", ["haben", "sein"], key="input_aux")

            submitted = st.form_submit_button("Load to Database")

            if submitted:
                fields = [word_val, translation_raw, example_de, infinitiv, 
                          praeteritum, partizip_ii, duden_link]
                
                if not all(f.strip() for f in fields):
                    st.error("All fields are required.")
                else:
                    if collection.find_one({"word": word_val.strip()}):
                        st.warning(f"'{word_val}' already exists in {collection_name}.")
                    else:
                        last_entry = collection.find_one(sort=[("word_id", -1)])
                        new_id = (last_entry["word_id"] + 1) if last_entry else 1

                        translation_list = [t.strip() for t in translation_raw.split(",") if t.strip()]

                        doc = {
                            "word_id": new_id,
                            "word": word_val.strip(),
                            "translations": translation_list,
                            "forms": {
                                "infinitiv": infinitiv.strip(),
                                "partizip_II": partizip_ii.strip(),
                                "praeteritum": praeteritum.strip()
                            },
                            "hilfsverben": { "perfekt": perfekt_aux },
                            "example": { "de": example_de.strip() },
                            "dictionary_link": duden_link.strip()
                        }

                        collection.insert_one(doc)
                        st.success(f"Added '{word_val}' (ID: {new_id}) to {collection_name}!")

# ==========================================
# MODE 2: QUIZ MODE
# ==========================================
elif app_mode == "Quiz Mode":
    st.title("Vocabulary Quiz")

    quiz_collection = st.radio(
        "Select Collection to Quiz:",
        options=["verben", "worte", "nomen"],
        horizontal=True,
        key="quiz_col_selector"
    )

    # Button to fetch a new random word
    if st.button("Get Random Word / Skip"):
        fetch_new_word(quiz_collection)

    st.divider()

    # If a word is currently loaded in session state, display the quiz interface
    if st.session_state.quiz_word:
        word_doc = st.session_state.quiz_word
        
        st.subheader(f"Translate: **{word_doc['word']}**")
        
        # Use a form so the user can hit 'Enter' to submit
        with st.form("answer_form", clear_on_submit=True):
            user_guess = st.text_input("Your English Translation:")
            submitted_guess = st.form_submit_button("Check Answer")
            
            if submitted_guess:
                if not user_guess.strip():
                    st.warning("Please type an answer before checking.")
                else:
                    # Convert both the guess and valid answers to lowercase for a fair comparison
                    guess_clean = user_guess.strip().lower()
                    valid_answers = [t.lower() for t in word_doc['translations']]
                    
                    if guess_clean in valid_answers:
                        st.session_state.quiz_feedback = "correct"
                    else:
                        st.session_state.quiz_feedback = "incorrect"

        # Display feedback outside the form so it persists until the next word
        if st.session_state.quiz_feedback == "correct":
            st.success("Richtig! (Correct!) 🎉")
            st.write(f"**All valid translations:** {', '.join(word_doc['translations'])}")
            
            # Safely get the example sentence if it exists
            example = word_doc.get("example", {}).get("de", "")
            if example:
                st.info(f"**Example:** {example}")
                
        elif st.session_state.quiz_feedback == "incorrect":
            st.error("Falsch! (Incorrect). Try again!")
    else:
        st.info("Click 'Get Random Word' to start the quiz!")
        