import json

from flask import Flask, request
import pyowm
import wit
import dicttoxml

import private


app = Flask(__name__)


DEFAULT_MESSAGE = "I don't know."


@app.route("/")
def home():
    return "Welcome"


@app.route("/api", methods=['GET'])
def api():
    """Return a message from query."""
    text = request.args.get('query', '')
    return json.dumps({'message': handle_query(text)})


@app.route("/pi", methods=['POST'])
def pi_router():
    text = request.form['Body']
    message = handle_query(text)
    data = {'Response': {'Message': message}}
    xml = dicttoxml.dicttoxml(data, root=False)
    return xml, 200, {'content-type': 'text/xml'}


def handle_query(text):
    """Send a text-based query to Wit."""
    wit.init()

    message = DEFAULT_MESSAGE

    response = wit.text_query(text, private.WIT_API_TOKEN)
    result = json.loads(response)

    intent = result['outcomes'][0]['intent']

    if result['outcomes'] and 'entities' in result['outcomes'][0]:
        entity = result['outcomes'][0]['entities']

    if 'get_weather' in intent:
        message = get_weather(entity)

    return message


def get_weather(entity):
    location = 'Melbourne, Australia'
    day = None

    if 'location' in entity:
        location = entity['location'][0]['value']

    owm = pyowm.OWM(private.OWM_API_TOKEN)
    forecast = owm.weather_at_place(location)
    weather = forecast.get_weather()

    return "The weather is {0}. Current temp is {1}".format(
        weather.get_detailed_status(), weather.get_temperature('celsius')['temp'])


if __name__ == "__main__":
    app.run(debug=True)
