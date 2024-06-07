from flask import Flask, render_template, request, make_response, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__) 
  
@app.route("/") 
def index(): 
   return render_template("index.html") 

@app.route('/setcookie', methods=['POST', 'GET']) 
def setcookie(): 
   if request.method == 'POST': 
      user = request.form.get('name')
      email = request.form.get('email')

      if user is not None:
         resp = make_response(render_template('cookie.html')) 
         resp.set_cookie('userID', user) 
      elif email is not None:
         resp = make_response(render_template('cookie.html')) 
         resp.set_cookie('email', email)
      else:
         resp = make_response(render_template('cookie.html'))
         # Handle case when neither user nor email is provided

      return resp
   else:
      return render_template('index.html')

  
@app.route('/setcookie/getcookie')
def getcookie(): 
   name = request.cookies.get('userID')
   email = request.cookies.get('email')
   return render_template('getcookie.html', name=name, email=email)

# ---------------------------------------------------------------------

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload') 
def upload_form():
   return render_template('upload.html') 
      
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('display_file', filename=filename))

@app.route('/upload/<filename>')
def display_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.isfile(file_path):
        return f'<h1>Displaying file: {filename}</h1><br><img src="{url_for("uploaded_file", filename=filename)}" alt="Uploaded File">'
    else:
        return 'File not found.'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --------------------------------------------------------------------
   
@app.route('/student') 
def student(): 
   return render_template('student.html') 
  
@app.route('/result', methods = ['POST', 'GET'])
def result(): 
   if request.method == 'POST':
      result = request.form 
      return render_template("result.html", result = result)

# --------------------------------------------------------------------

app.secret_key = 'hassanqureshi'  # Required for flash messages

# /login display login form 
@app.route('/login', methods = ['GET', 'POST'])  
# login function verify username and password 
def login():      
   error = None
     
   if request.method == 'POST': 
      if request.form['username'] != 'admin' or request.form['password'] != 'admin': 
         error = 'Invalid username or password. Please try again !'
         flash(error, 'error')
      else: 
         # flashes on successful login 
         flash('You were successfully logged in', 'success')  
         return redirect(url_for('home')) 
   return render_template('login.html', error = error)

@app.route('/home', methods=['POST', 'GET'])
def home():
    welcome = "Welcome to the Home Page."
    return render_template('home.html', welcome=welcome)

# ------------------------------------------------------------------

@app.route('/number', methods=['GET'])
def squarenumber():
    # If method is GET, check if  number is entered 
    # or user has just requested the page.
    # Calculate the square of number and pass it to 
    # answermaths method
    if request.method == 'GET':
   # If 'num' is None, the user has requested page the first time
        if(request.args.get('num') == None):
            return render_template('squarenum.html')
          # If user clicks on Submit button without 
          # entering number display error
        elif(request.args.get('num') == ''):
            return "<html><body> <h1>Invalid number</h1></body></html>"
        else:
          # User has entered a number
          # Fetch the number from args attribute of 
          # request accessing its 'id' from HTML
            number = request.args.get('num')
            sq = int(number) * int(number)
            # pass the result to the answer HTML
            # page using Jinja2 template
            return render_template('answer.html', 
                                   squareofnum=sq, num=number)

# -------------------------------------------------------------------

@app.route('/hassan', methods=['GET'])
def hassan():
   name = "Hassan Mustafa"
   age = "23"
   city = "Karachi"
   return render_template('hassan.html', name=name, age=age, city=city)


@app.route('/mustafa', methods=['GET', 'POST'])
def mustafa():
   if request.method == 'POST':
      name = request.form.get('name')
      age = request.form.get('age')
      city = request.form.get('city')
      return render_template('mustafa_render.html', name=name, age=age, city=city)

   else:
      name = request.args.get('name')
      age = request.args.get('age')
      city = request.args.get('city')
      return render_template('mustafa.html', name=name, age=age, city=city)

# ---------------------------------------------------------------------
   
from flask_mail import Mail, Message 
   
mail = Mail(app) # instantiate the mail class 
   
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hassanqureshi700@gmail.com'
app.config['MAIL_PASSWORD'] = 'ytce cpjx fyzz pfoz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 
   
# message object mapped to a particular URL ‘/’ 
@app.route("/send") 
def send(): 
   msg = Message( 
                'Hello, This is flask testing.', 
                sender ='hassanqureshi700@gmail.com', 
                recipients = ['FAfridi047@gmail.com'] 
               ) 
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg) 
   return 'Sent'

# -------------------------------------------------------------------






if __name__ == '__main__': 
   app.run(debug = True) 