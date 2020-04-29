import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.externals import joblib
from analysis import analyzer

analyzer=analyzer()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    text = request.form.values()
    output = analyzer.output(text)
    if output==0:
        return render_template('negative.html')
    if output ==1:
        render_template('positive.html')



if __name__ == "__main__":
    app.run(debug=True)