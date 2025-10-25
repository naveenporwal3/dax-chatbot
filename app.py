import requests
import streamlit as st

# --- Hugging Face setup ---
HF_API_KEY = st.secrets.get("HF_API_KEY")  # read from Streamlit Secrets

if not HF_API_KEY:
    st.error("⚠️ Hugging Face API key missing in Streamlit Secrets.")
    st.stop()

HF_API_KEY = HF_API_KEY.strip()  # remove extra spaces
HF_MODEL = "microsoft/Phi-3-mini-4k-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
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
            try:
                response = requests.post(API_URL, headers=headers, json=payload)

                # --- Handle authentication error ---
                if response.status_code == 401:
                    st.error("❌ Hugging Face API Unauthorized (401). Check your API key.")
                elif response.status_code != 200:
                    st.error(f"❌ Hugging Face API error: {response.status_code}")
                else:
                    result = response.json()
                    # handle both new and legacy HF API response formats
                    generated_text = None
                    if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                        generated_text = result[0]["generated_text"]
                    elif isinstance(result, dict) and "error" in result:
                        st.error(f"❌ Hugging Face API returned an error: {result['error']}")
                    if generated_text:
                        st.code(generated_text, language="dax")
                    else:
                        st.error("⚠️ Unexpected response format. Try again.")
            except Exception as e:
                st.error(f"⚠️ An exception occurred: {str(e)}")
