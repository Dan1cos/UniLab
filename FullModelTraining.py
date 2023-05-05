import SelectHtmlBody
import RemovingUnnecessaryData
import Vectorize
import pandas as pd
import json
import numpy as np
from sklearn import preprocessing
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

#function from ConvertingVectorToDF
def clearDic(dict):
    for i in dict.keys():
        dict[i] = 0
    return dict

##function from ConvertingVectorToDF
def createWordsDF(vector):
    dic = {}
    for i in vector:
        for j in i:
            if j in dic:
                dic[j] += i[j]
            else:
                dic[j] = i[j]

    dataFrameIsw_v2 = pd.DataFrame(columns=[dic.keys()])

    dic2 = dic

    for i in vector:
        clear_dict = clearDic(dic2)
        for j in i:
            clear_dict[j] = i[j]
        df_temp = pd.DataFrame(clear_dict, index=[0])
        dataFrameIsw_v2 = pd.concat([dataFrameIsw_v2, df_temp], ignore_index=True)

    df_tfidf_v2 = dataFrameIsw_v2.drop(dataFrameIsw_v2.columns[6116:], axis=1)

    return df_tfidf_v2

#script from MergingData
def mergeAllData(folderWithWeatherEventsRegions, df_words):
    df_events = pd.read_csv(f"{folderWithWeatherEventsRegions}/events.csv", sep=";")
    df_events_v2 = df_events.drop(["id", "region_id"], axis=1)

    def isNaN(num):
        return num != num

    # converting datetime values
    df_events_v2["start_time"] = pd.to_datetime(df_events_v2["start"])
    df_events_v2["end_time"] = pd.to_datetime(df_events_v2["end"])
    df_events_v2["start_hour"] = df_events_v2['start_time'].dt.floor('H')
    df_events_v2["end_hour"] = df_events_v2['end_time'].dt.ceil('H')
    df_events_v2["start_hour"] = df_events_v2.apply(
        lambda x: x["start_hour"] if not isNaN(x["start_hour"]) else x["event_hour"], axis=1)
    df_events_v2["end_hour"] = df_events_v2.apply(
        lambda x: x["end_hour"] if not isNaN(x["end_hour"]) else x["event_hour"], axis=1)
    df_events_v2["day_date"] = df_events_v2["start_time"].dt.date

    df_events_v2["start_hour_datetimeEpoch"] = df_events_v2['start_hour'].apply(
        lambda x: int(x.strftime('%s')) if not isNaN(x) else None)
    df_events_v2["end_hour_datetimeEpoch"] = df_events_v2['end_hour'].apply(
        lambda x: int(x.strftime('%s')) if not isNaN(x) else None)

    # importing csv with weather
    df_weather = pd.read_csv(f"{folderWithWeatherEventsRegions}/weather.csv")

    # editing weather data
    # columns to delete
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

    # deleting columns mentioned above
    df_weather_v2 = df_weather.drop(weather_exclude, axis=1)

    # editing city column, changing name of one region
    df_weather_v2["city"] = df_weather_v2["city_resolvedAddress"].apply(lambda x: x.split(",")[0])
    df_weather_v2["city"] = df_weather_v2["city"].replace('Хмельницька область', "Хмельницький")

    # importing csv with regions
    df_regions = pd.read_csv(f"{folderWithWeatherEventsRegions}/regions.csv")

    # merging regions with weather
    df_weather_reg = pd.merge(df_weather_v2, df_regions, left_on="city", right_on="center_city_ua")

    events_dict = df_events_v2.to_dict('records')
    events_by_hour = []

    for event in events_dict:
        for d in pd.date_range(start=event["start_hour"], end=event["end_hour"], freq='1H'):
            et = event.copy()
            et["hour_level_event_time"] = d
            events_by_hour.append(et)

    df_events_v3 = pd.DataFrame.from_dict(events_by_hour)

    df_events_v3["hour_level_event_datetimeEpoch"] = df_events_v3["hour_level_event_time"].apply(
        lambda x: int(x.strftime('%s')) if not isNaN(x) else None)
    df_events_v4 = df_events_v3.copy().add_prefix('event_')

    # merging edited weather and events
    df_weather_v4 = df_weather_reg.merge(df_events_v4,
                                         how="left",
                                         left_on=["region_alt", "hour_datetimeEpoch"],
                                         right_on=["event_region_title", "event_hour_level_event_datetimeEpoch"])

    # exporting to csv
    df_weather_v4.to_csv(f"pathToSaveIt", sep=";", index=False)

    ######Merging tfidf to that dataframe

    # importing tfidf
    df_tfidf = df_words

    # editing tfidf
    days = pd.date_range(start='2022-02-24', end='2023-01-25', freq="D")
    only_days = days.to_pydatetime()
    only_days_v2 = list(map(lambda x: x.strftime('%Y-%m-%d'), only_days))
    only_days_v3 = np.concatenate(
        (only_days_v2[:273], only_days_v2[274:304], only_days_v2[305:311], only_days_v2[312:]), axis=None)

    df_tfidf['date'] = only_days_v3

    # merging all dataframes
    final_merged_set = df_weather_v4.merge(df_tfidf,
                                           how="left",
                                           left_on=["day_datetime"],
                                           right_on=["date"])

    return final_merged_set

def isNaN_v2(num):
    return pd.notna(num)

#scripts from SplittingTrainTest and TrainModel
def trainModel(final_merged_set):
    # making label encoder for hour conditions
    le = preprocessing.LabelEncoder()
    le.fit(final_merged_set["hour_conditions"].unique())
    final_merged_set["hour_conditions"] = le.transform(final_merged_set["hour_conditions"])

    # making label encoder for hour percitype
    le2 = preprocessing.LabelEncoder()
    le2.fit(final_merged_set["hour_preciptype"].unique())
    final_merged_set["hour_preciptype"] = le2.transform(final_merged_set["hour_preciptype"])

    # converting datetime to timestamp
    final_merged_set["day_sunrise"] = final_merged_set["day_sunrise"]. \
        apply(lambda x: datetime.strptime(x, "%H:%M:%S").hour * 60 + datetime.strptime(x, "%H:%M:%S").minute)
    final_merged_set["day_sunset"] = final_merged_set["day_sunset"]. \
        apply(lambda x: datetime.strptime(x, "%H:%M:%S").hour * 60 + datetime.strptime(x, "%H:%M:%S").minute)

    ###Splitting into test and train
    train_percent = .8
    time_between = final_merged_set.hour_datetimeEpoch.max() - final_merged_set.hour_datetimeEpoch.min()
    train_cutoff = final_merged_set.hour_datetimeEpoch.min() + train_percent * time_between
    train_df = final_merged_set[final_merged_set.hour_datetimeEpoch <= train_cutoff]
    test_df = final_merged_set[final_merged_set.hour_datetimeEpoch > train_cutoff]

    ###deleteing columns for model training
    events_exclude = [
        "event_region_title",
        "event_region_city",
        "event_all_region",
        "event_start",
        "event_end",
        "event_clean_end",
        "event_intersection_alarm_id",
        "event_start_time",
        "event_end_time",
        "event_start_hour",
        "event_end_hour",
        "event_day_date",
        "event_start_hour_datetimeEpoch",
        "event_end_hour_datetimeEpoch",
        "event_hour_level_event_time",
        "event_hour_level_event_datetimeEpoch",
        "city_resolvedAddress",
        "city_x",
        "region_x",
        "center_city_ua",
        "center_city_en",
        "region_alt",
        "day_datetime",
        "hour_datetime",
        "date"
    ]


    train_target = train_df["event_start"]
    train_target = train_target.apply(lambda x: isNaN_v2(x))

    train_df = train_df.drop(events_exclude, axis=1)
    train_df = train_df.fillna(0)

    ################Some model training
    clf = ModelNameHere

    test_target = test_df["event_start"]
    test_target = test_target.apply(lambda x: isNaN_v2(x))
    test_df = test_df.drop(events_exclude, axis=1)
    test_df = test_df.fillna(0)

    received_data = clf.predict(test_df)

    print("Accuracy:", accuracy_score(test_target, received_data))
    print("Precision:", precision_score(test_target, received_data))
    print("Recall:", recall_score(test_target, received_data))
    print("F1 score:", f1_score(test_target, received_data))
    print(confusion_matrix(test_target, received_data))

    return clf

#input folder with regions, events, weather, htmls
INPUT_FOLDER = "input folder"

#Selecting html body
selectedHtml = SelectHtmlBody.firstSt(INPUT_FOLDER)
#Removing unnececcary text
removedUnnecDataDF = RemovingUnnecessaryData.secondSt(selectedHtml)
#Making tfidf
tfidf_vec = Vectorize.thirdSt(removedUnnecDataDF,removedUnnecDataDF)
#Creating datframe from tfidf
tfidfDF = createWordsDF(tfidf_vec)
#Creating merged dataset
final_merged_set = mergeAllData(INPUT_FOLDER, tfidfDF)
#Training model
finalModel = trainModel(final_merged_set)
