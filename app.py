import os
import requests
import streamlit as st

# --- Hugging Face setup ---
HF_API_KEY = st.secrets.get("HF_API_KEY")  # will use Streamlit Secrets
HF_MODEL = "microsoft/Phi-3-mini-4k-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

if not HF_API_KEY:
    st.error("⚠️ Please set your Hugging Face API key in Streamlit secrets.")
    st.stop()

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# --- Streamlit UI ---
st.title("DAX Chatbot (Free - Hugging Face)")
st.write("Ask anything in plain English and get a DAX formula.")

user_input = st.text_area("Enter your request:", height=80)

if st.button("Generate DAX"):
    if not user_input.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("⏳ Generating DAX..."):
            payload = {
                "inputs": f"You are an expert in Power BI and DAX. Write a clear and efficient DAX formula for: {user_input}",
                "parameters": {"max_new_tokens": 400}
            }
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code != 200:
                st.error(f"Hugging Face API error: {response.status_code}")
            else:
                result = response.json()
                if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                    st.code(result[0]["generated_text"], language="dax")
                else:
                    st.error("⚠️ Unexpected response format. Try again.")
