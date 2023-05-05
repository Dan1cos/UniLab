import pandas as pd
import json
import ISWPrediction
import CollectForecast
import numpy as np
from datetime import datetime

#path to emptyVector
VECTOR_PATH = 'data/emptyVector.csv'

#merging our weather and ISW report data 
#to create a dataset that will be further used for prediction
def createDataSet(date_input):

    #creating and converting our ISW dictionary into suitable form
    vector1 = ISWPrediction.take_vector_from_isw(date_input)
    vector1 = {k: v for d in vector1.values() for k, v in d.items()}

    
    vector2 = pd.read_csv(VECTOR_PATH, sep=';')
    vector2.loc[0] = {}
    for i in vector2.columns:
        if i in vector1:
            vector2[i] = vector1[i]
    vector2 = vector2.fillna(0)

    #creating df woth relevant weather data 
    df_weather = CollectForecast.getNewForecast()
    #filler column for merging purposes
    df_weather['just_to_join'] = "1"
    vector2["just_to_join"] = "1"
    #merging
    final_merged_set = df_weather.merge(vector2, how="left", left_on="just_to_join", right_on="just_to_join")
    final_merged_set = final_merged_set.drop(["just_to_join", "Unnamed: 0", "date"], axis=1)
    final_merged_set = final_merged_set.rename(columns = {"city":"city_y", "region":"region_y"})

    #return
    return final_merged_set
