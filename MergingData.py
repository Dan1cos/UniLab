import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly as plotly

#######Merging Events and Weather
#importing csv with events
df_events = pd.read_csv(f"pathToEventsDF", sep = ";")

#editing events data
#deleting columns id and region_id
df_events_v2 = df_events.drop(["id","region_id"],axis=1)

def isNaN(num):
    return num != num

#converting datetime values
df_events_v2["start_time"] = pd.to_datetime(df_events_v2["start"])
df_events_v2["end_time"] = pd.to_datetime(df_events_v2["end"])
df_events_v2["start_hour"] = df_events_v2['start_time'].dt.floor('H')
df_events_v2["end_hour"] = df_events_v2['end_time'].dt.ceil('H')
df_events_v2["start_hour"] = df_events_v2.apply(lambda x: x["start_hour"] if not isNaN(x["start_hour"]) else x["event_hour"] , axis=1)
df_events_v2["end_hour"] = df_events_v2.apply(lambda x: x["end_hour"] if not isNaN(x["end_hour"]) else x["event_hour"] , axis=1)
df_events_v2["day_date"] = df_events_v2["start_time"].dt.date

df_events_v2["start_hour_datetimeEpoch"] = df_events_v2['start_hour'].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)
df_events_v2["end_hour_datetimeEpoch"] = df_events_v2['end_hour'].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)

#importing csv with weather
df_weather = pd.read_csv(f"pathToWeatherDF")

#editing weather data
#columns to delete
weather_exclude = [
"day_feelslikemax",
"day_feelslikemin",
"day_sunriseEpoch",
"day_sunsetEpoch",
"day_description",
"city_latitude",
"city_longitude",
"city_address",
"city_timezone",
"city_tzoffset",
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
"hour_icon",
"hour_source",
"hour_stations",
"hour_feelslike"
]

#deleting columns mentioned above
df_weather_v2 = df_weather.drop(weather_exclude, axis=1)

#editing city column, changing name of one region
df_weather_v2["city"] = df_weather_v2["city_resolvedAddress"].apply(lambda x: x.split(",")[0])
df_weather_v2["city"] = df_weather_v2["city"].replace('Хмельницька область', "Хмельницький")

#importing csv with regions
df_regions = pd.read_csv(f"{INPUT_FOLDER}/{DATA_REGIONS_FILE}")

#merging regions with weather
df_weather_reg = pd.merge(df_weather_v2, df_regions, left_on="city",right_on="center_city_ua")

events_dict = df_events_v2.to_dict('records')
events_by_hour = []

for event in events_dict:
    for d in pd.date_range(start=event["start_hour"], end=event["end_hour"], freq='1H'):
        et = event.copy()
        et["hour_level_event_time"] = d
        events_by_hour.append(et)

df_events_v3 = pd.DataFrame.from_dict(events_by_hour)

df_events_v3["hour_level_event_datetimeEpoch"] = df_events_v3["hour_level_event_time"].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)
df_events_v4 = df_events_v3.copy().add_prefix('event_')

#merging edited weather and events
df_weather_v4 = df_weather_reg.merge(df_events_v4,
                                     how="left",
                                     left_on=["region_alt","hour_datetimeEpoch"],
                                     right_on=["event_region_title","event_hour_level_event_datetimeEpoch"])

#exporting to csv
df_weather_v4.to_csv(f"pathToSaveIt", sep=";", index=False)

######Merging tfidf to that dataframe

#importing tfidf
df_tfidf = pd.read_csv(f"pathToTFIDFdataframe", sep = ";")

#editing tfidf
days = pd.date_range(start='2022-02-24', end='2023-01-25', freq="D")
only_days = days.to_pydatetime()
only_days_v2 = list(map(lambda x: x.strftime('%Y-%m-%d'), only_days))
only_days_v3 = np.concatenate((only_days_v2[:273], only_days_v2[274:304], only_days_v2[305:311], only_days_v2[312:]), axis=None)

df_tfidf['date'] = only_days_v3

#merging all dataframes
final_merged_set = df_weather_v4.merge(df_tfidf,
                                     how="left",
                                     left_on=["day_datetime"],
                                     right_on=["date"])

#exporting to csv
final_merged_set.to_csv(f"pathToSaveFinalSet", sep=";", index=False)
