from flask import Flask, render_template, request, jsonify, Response, session
import os
import secrets

app = Flask(__name__)

# Set a secret key for the application
app.secret_key = secrets.token_hex(16)

questions = [
    ("What is your name?", 1, "آپ کا نام کيا ہے؟", "¿Cómo te llamas?", "আপনার নাম কি?", "ما اسمك؟"),
    ("What is your age?", 2, "آپ کی عمر کیا ہے؟", "¿Cuántos años tienes?", "আপনার বয়স কত?", "ما هو عمرك؟"),
    ("What is your address?", 3, "آپ کا پتہ کیا ہے؟", "¿Cuál es su dirección?", "আপনার ঠিকানা কি?", "ما هو عنوانك؟"),
]

@app.route("/")
def initial_message():
    global question_index
    question_index = 0
    language = request.args.get('language-select')
    
    session['language'] = language
    initial_message = "Hi! I am an AI Assistant representing the ICNA Relief Organization."
    if language == '2':
        initial_message = "!السلام علیکم"
    elif language == '3':
        initial_message = "Hola!"
    elif language == '4':
        initial_message = "হাই!"
    elif language == '5':
        initial_message = "!مرحبا"
    return render_template("index.html", initial_message=initial_message)

question_index = 0
user_responses = []
@app.route("/chat", methods=["POST", "GET"])
def chat():
    global question_index
    global user_responses
    
    if request.method == 'POST':
        user_input = request.form["user_input"]
        user_responses.append(user_input)
        language = session.get('language', '')
        
        if question_index < len(questions):
            if language.isdigit() and 0 <= int(language) < len(questions[question_index]):
                current_question = questions[question_index][int(language)]
                question_index += 1
                return jsonify({"response": current_question})
            else:
                return jsonify({"response": "Invalid language selection."})
        else:
            return jsonify({"response": "Thank you for answering the questions. Have a good day! Bye.", "user_responses": user_responses})

if __name__ == "__main__":
    app.run(debug=True)
