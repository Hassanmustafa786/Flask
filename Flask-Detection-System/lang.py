from flask import Flask, redirect, url_for 

app = Flask(__name__) 
  
# @app.route('/admin')  #decorator for route(argument) function 
# def hello_admin():     #binding to hello_admin call 
#    return 'Hello Admin! <br> Function 1 is working'    
  
# @app.route('/guest/<guest>') 
# def hello_guest(guest):    #binding to hello_guest call 
#    return 'Hello %s ! <br> Function 2 is working' % guest 
  
# @app.route('/user/<name>') 
# def hello_user(name):     
#    if name =='admin':  #dynamic binding of URL to function 
#       return redirect(url_for('hello_admin'))
#    else: 
#       return redirect(url_for('hello_guest', guest = name)) 
   
languages = ['en', 'ur', 'es', 'bn', 'ar']
not_languages = ['fr', 'ru', 'de']

@app.route('/<language_select>')
def language(language_select):   
    return f'Yes! This selected language "{language_select}" is supported.'

@app.route('/ask_language') 
def ask_language():    #binding to ask_language call 
   return f'Please! Select the language first. <br> Following are the supported languages: {languages}'

@app.route('/chat/<language>') 
def selected_language(language):
   if language in languages:
      return redirect(url_for('language', language_select = language))
   elif language in not_languages:
      return redirect(url_for('ask_language'))
   else:
      return f'The language "{language}" is not supported.'

if __name__ == '__main__': 
   app.run(debug = True)