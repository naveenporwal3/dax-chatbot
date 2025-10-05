
import openai
import os
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY', '')

if openai.api_key == "":
    sys.stderr.write("""
    You haven't set up your API key yet.

    If you don't have an API key yet, visit:

    https://platform.openai.com/signup

    1. Make an account or sign in
    2. Click "View API Keys" from the top right menu.
    3. Click "Create new secret key"

    Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
    """)

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
        
        if not openai.api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Power BI and DAX (Data Analysis Expressions). Generate clear, efficient, and well-commented DAX formulas based on user descriptions. Explain what the formula does and provide usage tips."
                },
                {
                    "role": "user",
                    "content": f"Generate a DAX function for: {user_request}"
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        dax_code = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'dax_code': dax_code
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
