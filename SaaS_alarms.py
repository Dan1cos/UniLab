import datetime as dt
import json
import pandas as pd
import requests
from flask import Flask, jsonify, request

FOLDER = "data"
CSV = "predictedAlarms.csv"
LOG = "timestamps.log"

app = Flask(__name__)

#script that takes data out of file and makes it in json format
def get_alarms(city: str = None):
    alarmsFile = pd.read_csv(f"{FOLDER}/{CSV}", sep=";")
    print()
    info = "{"
    if city is None or city.lower() == "all":
        for reg in alarmsFile["center_city_en"].unique():
            info+="\""+str(reg)+"\":{"
            for index, val in alarmsFile[alarmsFile["center_city_en"]==reg].tail(12).iterrows():
                info+="\""+val["time"]+"\":\""+str(val["prediction"])+"\","
            info = info[:-1]
            info+="},"
        info = info[:-2]
    elif city in alarmsFile["center_city_en"].unique():
        info+="\""+str(city)+"\":{"
        for index, val in alarmsFile[alarmsFile["center_city_en"]==city].tail(12).iterrows():
            info += "\"" + val["time"] + "\":\"" + str(val["prediction"]) + "\","
        info = info[:-1]
    else:
        info += "\"" + str(city) + "\":{"
    info += "}}"
    return json.loads(info)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Practice 4. Python Saas. Alarms API</h2></p>"


@app.route(
    "/content/api/info",
    methods=["POST"],
)
def weather_endpoint():
    json_data = request.get_json()

    location = json_data.get("location")

    alarms = get_alarms(location)

    ts = dt.datetime.now()

    with open(f"{FOLDER}/{LOG}") as f:
        f = f.readlines()

    result = {
        "last_model_train_time": f[0][:f[0].rindex(' ')],
        "last_prediction_time": f[len(f)-1][:f[len(f)-1].rindex(' ')],
        "timestamp": ts.isoformat(),
        "regions_forecast": alarms,
    }

    return result