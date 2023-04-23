import pandas as pd
from WeatherScript import *

# ENTER INPUT TO regions.csv HERE
PATH_TO_REGIONS_ID = ""

regions = pd.read_csv(f"{PATH_TO_REGIONS_ID}", sep=",")


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
        region_df["region"] = regions["region"][region_id - 1]
        weather_df = pd.concat([weather_df, region_df])
    return weather_df


if __name__ == "__main__":
    forecast = getNewForecast()
    print(forecast)
