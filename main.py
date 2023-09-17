from flask import Flask, render_template, request
import requests
import json
import pickle
import numpy as np

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
API_KEY = '916f5690565d77df405165cc158fee08'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
model_weather = pickle.load(open('rainfall.pkl', 'rb'))


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None

    if request.method == 'POST':
        city = request.form['city']
        if city:
            # Make an API request to OpenWeatherMap
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            response = requests.get(BASE_URL, params=params)
            weather_data = json.loads(response.text)

    return render_template('index.html', weather_data=weather_data)


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model_weather.predict(final_features)

    output = round(prediction[0], 2)
    return render_template('index.html',
                           prediction_text='Predicted Rainfall for 6 hours in advance: {} mm'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
