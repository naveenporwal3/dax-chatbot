import os
import sys
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Get Hugging Face API key from environment
HF_API_KEY = os.environ.get('HF_API_KEY', '')

if HF_API_KEY == "":
    sys.stderr.write("""
    ⚠️ You haven't set your Hugging Face API key yet.

    1️⃣ Go to https://huggingface.co/settings/tokens
    2️⃣ Create a new token (read access)
    3️⃣ In your GitHub repo or deployment platform, add an environment variable:
        HF_API_KEY = your_token_here
    """)

# Use a free model from Hugging Face
HF_MODEL = "microsoft/Phi-3-mini-4k-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-dax', methods=['POST'])
def generate_dax():
    try:
        data = request.json
        user_request = data.get('request', '')
        
        if not user_request:
            return jsonify({'error': 'Please provide a description'}), 400
        
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {
            "inputs": f"You are an expert in Power BI and DAX. Write a clear and efficient DAX formula for: {user_request}",
            "parameters": {"max_new_tokens": 400}
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return jsonify({'error': f'Hugging Face API error: {response.status_code}', 'details': response.text}), 500
        
        result = response.json()

        # Hugging Face API returns a list of dicts with 'generated_text'
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            dax_code = result[0]["generated_text"]
        else:
            dax_code = "⚠️ Unexpected response format. Try again."

        return jsonify({'success': True, 'dax_code': dax_code})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
