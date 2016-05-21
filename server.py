from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    category = request.form["category"]
    distance = request.form["distance"]
    start   = request.form["start"]
    return "Category is %s, Distance is %s, Start is %s." % (category, distance, start)

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
