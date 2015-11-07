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

    result = wit.text_query(message, private.WIT_API_TOKEN)
    result = json.loads(result)
    result = result['outcomes'][0]['intent'];
   
    if 'get_weather' in result:
        message = get_weather()

    data = {'Response': {'Message': message}}
    xml = dicttoxml.dicttoxml(data, root=False)

    return xml, 200, {'content-type': 'text/xml'}


def get_temp():
    return "test: 45deg c"


def get_weather():
    client = yweather.Client()
    id = client.fetch_woeid("Melbourne, Australia")
    weather = client.fetch_weather(id, metric=True)

    return "The weather is {}. Current temp is {}".format(weather["condition"]["text"], 
                                            weather["condition"]["temp"])

if __name__ == "__main__":
    app.run(debug=True)


