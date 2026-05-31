# app.py
import streamlit as st
import time
from backend import AIBackend  # Import backend logic class
from sidebar import render_sidebar  # Import sidebar configuration component

# Initialize Backend Layer
backend = AIBackend()

# Page Configuration
st.set_page_config(
    page_title="LocalCloud AI", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS to override Streamlit's default component styling
# Enforces a custom theme by passing raw HTML/CSS into st.markdown.
# Note: 'unsafe_allow_html=True' is required to bypass Streamlit's script escaping.
st.markdown("""
    <style>
        /* Title text */
        .main-title {
            font-size: 2.5rem !important;
            font-weight: 700;
            background: linear-gradient(45deg, #FF4B4B, #4A90E2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        /* Custom container cards */
        .spec-card {
            background-color: rgba(128, 128, 128, 0.05);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #4A90E2;
            margin-bottom: 8px;
        }
        
        /* Background and borders for st.metric widgets */
        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.03);
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid rgba(128, 128, 128, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Render the main application header using custom HTML for CSS styling
st.markdown('<h1 class="main-title">⚡ LocalCloud AI</h1>', unsafe_allow_html=True)
st.caption("Switch seamlessly between cloud intelligence and private offline local models.")
st.write("---")

# Initialize persistent chat history so it survives Streamlit's page re-runs
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR CONFIG
# Render the sidebar UI and extract user-selected LLM configurations
config = render_sidebar(backend)
provider = config["provider"]
selected_model = config["selected_model"]
temperature = config["temperature"]
top_p = config["top_p"]
max_tokens = config["max_tokens"]
stream_output = config["stream_output"]

# Grouping the chat history in a dedicated container allows for isolated re-rendering
chat_container = st.container()

with chat_container:
    # Iterate through and render historical messages persisted in session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# USER INPUT & CHAT UI INITIALIZATION
if prompt := st.chat_input("Ask LocalCloud AI anything..."):
    # Append user message to persistent session state memory
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message immediately in UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initialize Assistant UI components
    with st.chat_message("assistant"):
        response_container = st.empty()       # Dynamic UI slot for streaming text
        metrics_container = st.empty()        # Dynamic UI slot for performance cards
        full_response = ""
        
        try:
            start_time = time.time()
            
            # BRANCH A: LOCAL INFERENCE ENGINE (Ollama / Llama.cpp)
            if provider == "Local models":
                stream = backend.generate_local_response(
                    selected_model, st.session_state.messages, temperature, top_p, max_tokens, stream_output
                )
                if stream_output:
                    final_chunk = None
                    for chunk in stream:
                        final_chunk = chunk 
                        full_response += chunk['message']['content']
                        response_container.markdown(full_response + " ▌")     # Dynamic typewriter effect
                else:
                    full_response = stream['message']['content']
                    final_chunk = stream
                
                end_time = time.time()
                total_duration = end_time - start_time
                
                # Parse and render specific local hardware metrics
                if stream_output and final_chunk:
                    eval_time = final_chunk.get('eval_duration', 0) / 1e9     # Convert ns to seconds
                    prompt_tokens = final_chunk.get('prompt_eval_count', 0)
                    response_tokens = final_chunk.get('eval_count', 0)
                    tps = response_tokens / eval_time if eval_time > 0 else 0
                    
                    with metrics_container.expander("📊 Performance Diagnostics (Local Engine)", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("⏱️ Inference Time", f"{total_duration:.2f}s")
                        col2.metric("⚡ Token Speed", f"{tps:.1f} t/s")
                        col3.metric("🪙 Tokens (In / Out)", f"{prompt_tokens} / {response_tokens}")
            
            # BRANCH B: CLOUD API ENGINE (Google Gemini)
            else:
                response = backend.generate_gemini_response(
                    selected_model, st.session_state.messages, temperature, top_p, max_tokens, stream_output
                )
                if stream_output:
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_container.markdown(full_response + " ▌")
                else:
                    full_response = response.text
                
                end_time = time.time()
                total_duration = end_time - start_time
                
                with metrics_container.expander("📊 Performance Diagnostics (Cloud API)", expanded=False):
                    col1, col2 = st.columns(2)
                    col1.metric("⏱️ API Round-trip Latency", f"{total_duration:.2f}s")
                    col2.metric("☁️ Inference Node", "Google Edge Infrastructure")

            # STATE PERSISTENCE & CLEANUP
            # Remove trailing cursor element from final UI state
            response_container.markdown(full_response)

            # Commit the assistant's response to conversation memory
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Error generating response: {e}")
