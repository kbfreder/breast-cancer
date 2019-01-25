from flask import Flask, abort, render_template, jsonify, request
from api import prediction

app = Flask('BreastCancerSurvivial')

@app.route('/survival', methods=['GET','POST'])
def get_prediction():
    # alert("Page loaded")
    print("Page loaded")
    # console.log("Page loaded")
    if not request.json:
        abort(400)
    # console.log("Page loaded")
    data = request.json
    response = prediction(data)
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

# if __name__ == '__main__':
    # app.run()

app.run(debug=True)
