from flask import Flask, render_template, request, jsonify
import openai 
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input):
    intro_message = """You are an AI Assistant, here to guide and assist people with their technical questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone. Your answer should be complete and precise."""
    client = OpenAI(
        api_key=openai.api_key,
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": intro_message},
            {"role": "user", "content": user_input},
        ],
        temperature=0.5,
        max_tokens=10,
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    initial_message = "Hi! I'm an AI Assistant. Can you tell me your name?"
    return render_template("index.html", initial_message=initial_message)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    response = generate_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
