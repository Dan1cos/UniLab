import pandas as pd
import json
import IswPrediction_final
import CollectForecast
import numpy as np
from datetime import datetime

VECTOR_PATH = 'data/emptyVector.csv'


def createDataSet(date_input):
    vector1 = IswPrediction_final.take_vector_from_isw(date_input)
    vector1 = {k: v for d in vector1.values() for k, v in d.items()}

    vector2 = pd.read_csv(VECTOR_PATH, sep=';')
    vector2.loc[0] = {}
    for i in vector2.columns:
        if i in vector1:
            vector2[i] = vector1[i]
    vector2 = vector2.fillna(0)

    df_weather = CollectForecast.getNewForecast()
    df_weather['just_to_join'] = "1"
    vector2["just_to_join"] = "1"
    final_merged_set = df_weather.merge(vector2, how="left", left_on="just_to_join", right_on="just_to_join")
    final_merged_set = final_merged_set.drop(["just_to_join", "Unnamed: 0", "date"], axis=1)
    final_merged_set = final_merged_set.rename(columns = {"city":"city_y", "region":"region_y"})


    return final_merged_set