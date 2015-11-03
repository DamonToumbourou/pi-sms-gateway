from flask import Flask
from flask import request
import dicttoxml
import yweather
app = Flask(__name__)

@app.route("/pi", methods=['POST'])
def home():

    if 'temp' in request.form['Body'].lower(): 
        message = get_temp()
    
    if 'weather' in request.form['Body'].lower(): 
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


