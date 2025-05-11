from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv, find_dotenv
from vercel_wsgi import handle_request
import requests
import re
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

def generate_gemini_response(user_query):
    load_dotenv("./.env")
    api_key = os.getenv("Google_Api_key")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_query}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  

        response_data = response.json()
        text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Bold text inside ** using regular expressions
        bold_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        return bold_text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"  
    except Exception as err:
        return f"An error occurred: {err}"  

@app.route("/", methods=["GET", "POST"])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        user_query = request.form["query"]
        bot_response = generate_gemini_response(user_query)
        
        # Store the question and response in session history
        session['history'].append({'user': user_query, 'bot': bot_response})

        # Return a JSON response with only the bot's response
        return jsonify({"bot_response": bot_response})  # Return only the bot response as JSON

    return render_template("index.html", history=session['history'])

def handler(environ, start_response):
    return handle_request(app, environ, start_response)

if __name__ == "__main__":
    app.run(debug=True)