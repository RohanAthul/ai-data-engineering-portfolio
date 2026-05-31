# sidebar.py
import streamlit as st
import os

def render_sidebar(backend):
    """
    Renders UI controls in the sidebar for selecting the AI backend.

    Returns:
        str: The selected backend provider ('Local models' or 'Google Gemini').
    """
    # Section Header - Backend Selection
    st.sidebar.markdown("### 🌐 Core Engine")
    provider = st.sidebar.radio(
        "Select Backend Provider", 
        ["Local models", "Google Gemini"],
        label_visibility="collapsed"
    )
    # Visual divider to separate core settings from future sidebar elements
    st.sidebar.write("---")

    # Hyperparameter Configuration Drawer
    st.sidebar.markdown("### ⚙️ Model Parameters")
    with st.sidebar.expander("Tune Generation Settings", expanded=False):
        temperature = st.slider(
            "🌡️ Temperature", 0.0, 2.0, 0.7, 0.1, 
            help="Temperature (The Creativity Knob) modifies the shape of the probability distribution before the model makes a choice. Mathematically, it scales the raw scores (logits) assigned to each potential token.\nLow Temperature (e.g., 0.1 to 0.4): Flattens the low probabilities and spikes the high probabilities. The model becomes highly confident and conservative, almost always choosing the absolute most likely next word.\nHigh Temperature (e.g., 0.7 to 1.2): Flattens the entire distribution, making the probabilities of all words more equal. This allows less likely, more unusual words a fighting chance to be picked."
        )
        top_p = st.slider(
            "🎯 Top-P", 0.0, 1.0, 0.9, 0.05,
             help="Top-P (Nucleus Sampling) The 'Pool Size' Filter. Instead of altering the probabilities themselves, Top-P dynamically cuts off the pool of options based on a cumulative probability threshold. The model sorts the potential words from highest probability to lowest, then starts adding them to a 'pool' until the total sum of their percentages hits the P value you set. Low Top-P (e.g., 0.3): The model only considers the top few words that make up the first 30% of the probability mass. Everything else is discarded. High Top-P (e.g., 0.9 or 1.0): The model keeps the pool wide open, considering a massive array of words that account for 90% to 100% of the possibilities, including the long tail of unusual words."
        )
        
        st.markdown("#### Output Limits")
        limit_tokens = st.checkbox("Limit Max Tokens", value=False)
        
        # Conditional UI evaluation: input renders only if token limiting is toggled on
        max_tokens = st.number_input("Max Output Tokens", 1, 8192, 2048) if limit_tokens else None
        
        st.markdown("#### Stream Preference")
        stream_output = st.checkbox("Stream Response Realtime", value=True)

    st.sidebar.write("---")

    selected_model = None

    # Dynamic Model Selection & Metadata Rendering
    # Layout branches depending on whether the user is processing locally or over the cloud
    if provider == "Local models":
        st.sidebar.markdown("### 🖥️ Local Model Selection")

        # Interrogate local Ollama instance for installed configurations
        model_names = backend.get_ollama_models()
        if not model_names:
            st.sidebar.error("❌ Could not connect to Ollama. Ensure your local server is running (`ollama serve`).")
        else:
            selected_model = st.sidebar.selectbox("Select Ollama Model", model_names, index=0, label_visibility="collapsed")

            if selected_model:
                # Retrieve and render structural hardware specs for the chosen local model
                model_details = backend.get_ollama_details(selected_model)
                if "error" not in model_details and 'details' in model_details:
                    st.sidebar.markdown("### 📋 Specifications")
                    details = model_details['details']
                    
                    with st.sidebar.container():
                        st.markdown(f"""
                        <div class="spec-card">
                            <b>🧬 Family:</b> {details.get('family', 'N/A').title()}<br>
                            <b>📦 Size:</b> {details.get('parameter_size', 'N/A')}<br>
                            <b>🔢 Quant:</b> {details.get('quantization_level', 'N/A')}<br>
                            <b>🗂️ Format:</b> {details.get('format', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.sidebar.error(f"Error fetching specifications.")
    else:
        st.sidebar.markdown("### ☁️ Cloud Model Selection")
        # Validate that credentials exist before rendering Gemini options
        if not os.getenv("GEMINI_API_KEY"):
            st.sidebar.error("🔑 `GEMINI_API_KEY` missing. Please check your system environment or setup your .env file.")
        else:
            gemini_models = ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-2.5-pro"]
            selected_model = st.sidebar.selectbox("Select Gemini Model", gemini_models, index=0, label_visibility="collapsed")
            
            if selected_model:
                st.sidebar.markdown("### 📋 Specifications")
                with st.sidebar.container():
                    # Categorize performance tier based on the naming convention string
                    tier = "Pro Tier (High Reasoning)" if "pro" in selected_model else "Flash Tier (Speed Optimized)"
                    st.markdown(f"""
                    <div class="spec-card">
                        <b>🏢 Provider:</b> Google AI Studio<br>
                        <b>⚡ Class:</b> Cloud Hosted API<br>
                        <b>🏷️ Tier:</b> {tier}
                    </div>
                    """, unsafe_allow_html=True)

    # Shipping the comprehensive configurations object back out to your orchestrator script
    return {
        "provider": provider,
        "selected_model": selected_model,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream_output": stream_output
    }
