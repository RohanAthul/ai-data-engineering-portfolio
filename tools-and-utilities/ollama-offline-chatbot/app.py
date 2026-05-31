import streamlit as st
import ollama

# Page Configuration
st.set_page_config(page_title="Ollama Chat", page_icon="💬", layout="wide")
st.title("💬 Ollama Local Chat")

# Sidebar for Model Selection
try:
    models_info = ollama.list()
    # Adjust based on how ollama.list() returns data (sometimes objects, sometimes dicts)
    # This handles the common return format
    model_names = [m['model'] for m in models_info['models']]
except Exception as e:
    st.warning("Could not fetch models. Is Ollama running?")
    model_names = []

selected_model = st.sidebar.selectbox("Select a Model", model_names, index=0 if model_names else None)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Handling
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response (Streaming)
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        try:
            # Stream the response from Ollama
            for chunk in ollama.chat(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True
            ):
                token = chunk['message']['content']
                full_response += token
                response_container.markdown(full_response + "▌")
                
            # Final update without cursor
            response_container.markdown(full_response)
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
            