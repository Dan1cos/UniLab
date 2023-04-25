import pickle
import numpy as np
import pandas as pd
from WeatherScript import *

# ENTER INPUT TO regions.csv HERE
PATH_TO_REGIONS_ID = ""
# ENTER INPUT TO .pkl of hour_conditions encoder HERE
PATH_TO_HOUR_CONDITIONS_ENCODER = ""

regions = pd.read_csv(f"{PATH_TO_REGIONS_ID}", sep=",")


def encode_precip_type(precip):
    types = [
        ['freezingrain'],
        ['ice'],
        ['rain', 'snow'],
        ['rain'],
        ['snow'],
        np.nan
    ]
    for type in types:
        if precip == type:
            return types.index(type)
    return types.index(np.nan)


# Function returns a dataframe with hourly forecast for the weather in all regions
def getNewForecast():
    weather_df = pd.DataFrame()
    region_df = pd.DataFrame()
    for region_id in regions["region_id"]:
        try:
            region_hours = getWeatherHours(regions["center_city_en"][region_id - 1], "")
        except ConnectionRefusedError as e:
            if e.args[0] != 400:
                return None
            # API did not find city of Lviv
            if region_id == 13:
                region_hours = getWeatherHours("Lemberg", "")
            # API did not find city of Sumy
            elif region_id == 18:
                region_hours = getWeatherHours("Sumy Oblast", "")
            # Generic unknown region
            else:
                region_hours = getWeatherHours("Ukraine", "")

        region_df = pd.DataFrame.from_dict(region_hours)
        region_df["region_id"] = regions["region_id"][region_id - 1]
        weather_df = pd.concat([weather_df, region_df])

    weather_exclude = [
        "day_datetime",
        "day_feelslikemax",
        "day_feelslikemin",
        "day_sunriseEpoch",
        "day_sunsetEpoch",
        "day_description",
        "day_feelslike",
        "day_precipprob",
        "day_snow",
        "day_snowdepth",
        "day_windgust",
        "day_windspeed",
        "day_winddir",
        "day_pressure",
        "day_cloudcover",
        "day_visibility",
        "day_severerisk",
        "day_conditions",
        "day_icon",
        "day_source",
        "day_preciptype",
        "day_stations",
        "hour_datetime",
        "hour_icon",
        "hour_source",
        "hour_stations",
        "hour_feelslike"
    ]
    weather_df = weather_df.drop(weather_exclude, axis=1)
    with open(f"{PATH_TO_HOUR_CONDITIONS_ENCODER}", "rb") as encoder_reader:
        label_encoder = pickle.load(encoder_reader)
        weather_df["hour_conditions"] = label_encoder.transform(weather_df["hour_conditions"])

    weather_df["hour_preciptype"].fillna(value=np.nan, inplace=True)
    weather_df["hour_preciptype"] = weather_df["hour_preciptype"]\
        .apply(lambda x: encode_precip_type(x))

    weather_df["hour_solarenergy"] = weather_df["hour_solarenergy"] \
        .apply(lambda x: 0 if x != x else x)
    weather_df["day_sunrise"] = weather_df["day_sunrise"]. \
        apply(lambda x: datetime.strptime(x, "%H:%M:%S").hour * 60 + datetime.strptime(x, "%H:%M:%S").minute)
    weather_df["day_sunset"] = weather_df["day_sunset"]. \
        apply(lambda x: datetime.strptime(x, "%H:%M:%S").hour * 60 + datetime.strptime(x, "%H:%M:%S").minute)
    return weather_df


if __name__ == "__main__":
    forecast = getNewForecast()
    print(forecast)
