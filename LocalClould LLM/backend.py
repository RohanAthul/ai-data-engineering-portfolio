# backend.py
import os
import ollama
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables immediately
load_dotenv()

class AIBackend:
    def __init__(self):
        self.client = genai.Client() if os.getenv("GEMINI_API_KEY") else None

    def get_ollama_models(self):
        try:
            models_info = ollama.list()
            return [m['model'] for m in models_info['models']]
        except Exception:
            return []

    def get_ollama_details(self, model_name):
        try:
            return ollama.show(model_name)
        except Exception as e:
            return {"error": str(e)}

    def generate_local_response(self, model, messages, temperature, top_p, max_tokens, stream_output):
        options = {"temperature": temperature, "top_p": top_p}
        if max_tokens is not None:
            options["num_predict"] = max_tokens
            
        return ollama.chat(
            model=model,
            messages=messages,
            stream=stream_output,
            options=options
        )

    def generate_gemini_response(self, model, messages, temperature, top_p, max_tokens, stream_output):
        if not self.client:
            self.client = genai.Client()
            
        config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_tokens
        )
        
        # Convert format to Gemini SDK standard
        formatted_contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
            
        if stream_output:
            return self.client.models.generate_content_stream(model=model, contents=formatted_contents, config=config)
        else:
            return self.client.models.generate_content(model=model, contents=formatted_contents, config=config)


