from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app = application

# Install ridge model and StandardScaler
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))

## Route for home page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predictdata", methods = ["GET", "POST"])
def predict_datapoint():
    if request.method == "POST":
        # Read all the inputs
        Temperature=float(request.form.get('Temperature'))
        RH = float(request.form.get('RH')) 
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain')) 
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC')) 
        ISI= float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))

        # Data transformation
        new_scaled_data = standard_scaler.transform([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
        result = ridge_model.predict(new_scaled_data)

        return render_template('home.html', result = result[0])

    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")


