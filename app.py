from flask import Flask
from flask import request
import json
import wit 
import dicttoxml
import yweather
import private
app = Flask(__name__)


@app.route("/") 
def home():
    return "Welcome"


@app.route("/pi", methods=['POST'])
def pi_router():

    wit.init()

    message = request.form['Body'] 
    
    response = wit.text_query(message, private.WIT_API_TOKEN)
    result = json.loads(response)
    
    intent = result['outcomes'][0]['intent'];
    
    if result['outcomes'] and 'entities' in result['outcomes'][0]:
        entity = result['outcomes'][0]['entities']    

    if 'get_weather' in intent:
        message = get_weather(entity)

    data = {'Response': {'Message': message}}
    xml = dicttoxml.dicttoxml(data, root=False)

    return xml, 200, {'content-type': 'text/xml'}


def get_temp():
    return "test: 45deg c"


def get_weather(entity):
        
    location = 'Melbourne'
    day = None;

    if 'day' in entity:
        day = entity['day'][0]['value']

    if 'location' in entity:
        location = entity['location'][0]['value']

    client = yweather.Client()
    id = client.fetch_woeid(location)
    
    weather = client.fetch_weather(id, metric=True)


    if day is None:
        desc = weather["condition"]["text"]
        temp = weather["condition"]["temp"]
        
        return "The weather is {}. Current temp is {}".format(desc, temp)

    
    if get_forecast(weather, day) is None:
        return "I can't get forecast for that day."

    high, low, text = get_forecast(weather, day)

    return "The weather for {} is: {}, max {}, min {}".format(day, text, high, low)


def get_forecast(weather, day):
    
    forecast = weather["forecast"]

    for f in forecast:
        if f['day'] in day:
            
            return f['high'], f['low'], f['text'] 


    return None



if __name__ == "__main__":
    app.run(debug=True)
