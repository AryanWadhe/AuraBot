from flask import Flask, render_template, request, session, jsonify
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def generate_gemini_response(user_query):
    api_key = "your_secret_key"  
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_query}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  

        response_data = response.json()
        text = response_data["candidates"][0]["content"]["parts"][0]["text"]

        
        return text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"  # Handle HTTP errors
    except Exception as err:
        return f"An error occurred: {err}"  # Handle other types of exceptions

@app.route("/", methods=["GET", "POST"])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        user_query = request.form["query"]
        bot_response = generate_gemini_response(user_query)
        
        session['history'].append({'user': user_query, 'bot': bot_response})

        return jsonify({"bot_response": bot_response})  

    return render_template("index.html", history=session['history'])

if __name__ == "__main__":
    app.run(debug=True)
