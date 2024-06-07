# importing libraries 
import smtplib
from flask import Flask 
from flask_mail import Mail, Message 

app = Flask(__name__) 
mail = Mail(app) # instantiate the mail class 

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hassanmustafa2753@gmail.com'
app.config['MAIL_PASSWORD'] = 'hassanmustafa123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 
   
# message object mapped to a particular URL ‘/’ 
@app.route("/") 
def index(): 
   msg = Message( 
                'Hello, This is flask testing.', 
                sender ='hassanmustafa2753@gmail.com', 
                recipients = ['hassanqureshi700@gmail.com'] 
               ) 
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg) 
   return 'Sent'

if __name__ == '__main__': 
    app.run(debug = True) 
