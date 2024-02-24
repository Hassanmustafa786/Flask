from flask import Flask, render_template, request, jsonify, Response, session
import os
import secrets

app = Flask(__name__)

# Set a secret key for the application
app.secret_key = secrets.token_hex(16)

questions = [
    ("What is your name?", 1, "آپ کا نام کيا ہے?", "¿Cómo te llamas?", "আপনার নাম কি?", "ما اسمك؟"),
    ("What is your age?", 2, "آپ کی عمر کیا ہے؟", "¿Cuántos años tienes?", "আপনার বয়স কত?", "ما هو عمرك؟"),
    ("What is your address?", 3, "آپ کا پتہ کیا ہے؟", "¿Cuál es su dirección?", "আপনার ঠিকানা কি?", "ما هو عنوانك؟"),
    ("Are you taking any Medications? If yes, then please tell name of the medication.", 4, "کیا آپ کوئی دوا لے رہے ہیں؟اگر ہاں. پھر دوا کا نام بتائیں ", "¿Está tomando algún medicamento? En caso afirmativo, indique el nombre del medicamento.", "আপনি কি কোনো ওষুধ খাচ্ছেন? যদি হ্যাঁ, তাহলে ওষুধের নাম বলুন।", "هل أنت مع أي أدوية؟ إذا كانت الإجابة بنعم، يرجى ذكر اسم الدواء."),
    ("Can you name the medicines?", 5, "کیا آپ ادویات کے نام بتا سکتے ہیں؟ ", "¿Puedes nombrar los medicamentos?", "ওষুধের নাম বলতে পারবেন?", "هل يمكنك تسمية الأدوية؟"),
    ("What other medicine have you taken in the past?", 6, "آپ نے ماضی میں اور کون سی دوا لی ہے؟ ", "¿Qué otro medicamento ha tomado en el pasado?", "অতীতে আপনি অন্য কোন ওষুধ খেয়েছেন?", "ما هي الأدوية الأخرى التي تناولتها في الماضي؟"),
    ("What is your major complaint?", 7, "آپ کی سب سے بڑی شکایت کیا ہے؟ ", "¿Cuál es su principal queja?", "আপনার প্রধান অভিযোগ কি?", "ما هي شكواك الرئيسية؟"),
    ("Have you previously suffered from this complaint?", 8, "کیا آپ کو پہلے بھی اس شکایت کا سامنا کرنا پڑا ہے؟", "¿Ha sufrido anteriormente esta dolencia?", "আপনি কি আগে এই অভিযোগ থেকে ভুগছেন?", "هل عانيت من قبل من هذه الشكوى؟"),
    ("What previous therapists have you seen?", 9, "آپ نے پچھلے کون سے تھراپسٹ کو دیکھا ہے؟", "¿A qué terapeuta has visto anteriormente?", "আপনি কি আগের থেরাপিস্ট দেখেছেন?", "ما المعالجين السابقين الذين رأيتهم؟"),
    ("Can you describe the treatment?", 10, "کیا آپ علاج کی وضاحت کر سکتے ہیں؟", "¿Puede describir el tratamiento?", "আপনি চিকিত্সা বর্ণনা করতে পারেন?", "هل يمكنك وصف العلاج؟"),
    ("What is your family history?", 11, "کیا آپ مجھے اپنے خاندان کی تاریخ کے بارے میں بتا سکتے ہیں؟", "¿Cuál es su historia familiar?", "আপনার পারিবারিক ইতিহাস কি?", "ما هو تاريخ عائلتك؟"),
    ("Are you adopted?", 12, "کیا آپ کو گود لیا گیا تھا؟", "¿Eres adoptado?", "আপনি কি দত্তক?", "هل أنت متبنى؟"),
    ("If yes, at what age were you adopted?", 13, "اگر ہاں، تو آپ کو کس عمر میں گود لیا گیا تھا؟", "En caso afirmativo, ¿a qué edad fue adoptado?", "যদি হ্যাঁ, কোন বয়সে আপনাকে দত্তক নেওয়া হয়েছিল?", "إذا كانت الإجابة بنعم، في أي عمر تم تبنيك؟"),
    ("How is your relationship with your mother?", 14, "ماں کے ساتھ آپ کا رشتہ کیسا ہے؟", "¿Cómo es tu relación con tu madre?", "আপনার মায়ের সাথে আপনার সম্পর্ক কেমন?", "كيف هي علاقتك مع والدتك؟"),
    ("Where did you grow up?", 15, "آپ کہاں بڑے ہوئے؟", "¿Dónde creciste?", "আপনি কোথায় বড় হয়েছেন?", "أين نشأت؟"),
    ("Are you married?", 16, "کيا آپ شادی شدہ ہيں", "¿Estás casado?", "আপনি কি বিবাহিত?", "هل أنت متزوج؟"),
    ("If yes, specify the date of marriage?", 17, "اگر ہاں، تو شادی کی تاریخ بتائیں؟", "En caso afirmativo, especifique la fecha del matrimonio.", "যদি হ্যাঁ, বিয়ের তারিখ উল্লেখ করবেন?", "إذا كانت الإجابة بنعم، حدد تاريخ الزواج؟"),
    ("Do you have children?", 18, "کیا آپ کے بچے ہیں؟", "¿Tienes hijos?", "আপনার কি সন্তান আছে?", "هل لديك أطفال؟"),
    ("If yes, how is your relationship with your children?", 19, "کیا آپ کے بچے ہیں؟", "En caso afirmativo, ¿cómo es su relación con sus hijos?", "যদি হ্যাঁ, আপনার সন্তানদের সাথে আপনার সম্পর্ক কেমন?", "إذا نعم كيف هي علاقتك مع أطفالك؟"),
]

@app.route("/")
def initial_message():
    global question_index
    question_index = 0
    language = request.args.get('language-select')
    initial_message = f"Select the language first."
    
    session['language'] = language
    if language == '0':
        initial_message = "Hi! I am an AI Assistant representing the ICNA Relief Organization."
        # initial_message = "Hi!"
    elif language == '2':
        initial_message = "!سلام"
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
