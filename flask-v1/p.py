from flask import Flask, Response, render_template, request

app = Flask(__name__)

@app.route("/mp3")
def stream_mp3():
    def generate():
        with open('Answers/English/A1.mp3', "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)
    return Response(generate(), mimetype="audio/mp3")

@app.route("/")
def index():
    return render_template("p.html")

@app.route('/process', methods=['POST'])
def process():
    selected_value = request.form.get('dropdown')
    return f'Selected value: {selected_value}'

if __name__ == "__main__":
    app.run(debug=True)
