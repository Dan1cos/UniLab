from datetime import datetime, timedelta
import requests
import sys
import json

API_TOKEN = ""


def generate_weather(city: str, date: str):
    url_base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    if city:
        url_city = city + "/"
    if date:
        url_date = date + "/"
    else:
        url_date = datetime.now().strftime("%Y-%m-%d") + "/"

    url_fin = f"{url_base}/{url_city}{url_date}?unitGroup=metric&include=hours&key={API_TOKEN}&contentType=json"
    response = requests.request("GET", url_fin)

    if response.status_code != 200:
        print('Unexpected Status code: ', response.status_code)
        raise ConnectionRefusedError(response.status_code)

    return json.loads(response.text)


# By entering date it will get info about weather for the full day
# If the date was not entered, it will get info for the next 12 hours
def getWeatherHours (city: str, date: str):
    json = generate_weather(city, date)['days'][0]['hours']
    hours = []
    if date:
        for hour in json:
            hours.append(hour)
    else:
        hour_now = datetime.now().hour
        diff = 0
        if 0 < 24 - hour_now < 12:
            diff = 12 - (24 - hour_now)
            json2 = generate_weather(city, (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"))['days'][0][
                'hours']
        for hour in json:
            if datetime.strptime(hour['datetime'], "%H:%M:%S").hour >= hour_now:
                hours.append(hour)
        if diff:
            for hour in json2:
                if datetime.strptime(hour['datetime'], "%H:%M:%S").hour < diff:
                    hours.append(hour)
                else:
                    break
    return hours