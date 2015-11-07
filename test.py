import app

def test_get_forecast():
    weather = {'forecast': [{'code': '33',
        'date': '7 Nov 2015',
        'day': 'Sat',
        'high': '62',
        'low': '47',
        'text': 'Mostly Clear'},
       {'code': '30',
        'date': '8 Nov 2015',
        'day': 'Sun',
        'high': '78',
        'low': '54',
        'text': 'Partly Cloudy'}]}      

    assert app.get_forecast(weather, 'Sunday') == ('78', '54', 'Partly Cloudy')
    
    assert app.get_forecast(weather, 'Saturday') == ('62', '47', 'Mostly Clear') 

    assert app.get_forecast(weather, 'Hacks') == None 
