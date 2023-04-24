import pandas as pd
import json
import IswPrediction_final
import CollectForecast
import numpy as np


VECTOR_PATH = 'D:/PythonLab/UniLab/data/vector_v2_dates.csv'

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
    final_merged_set = df_weather.merge(vector2)
    
    return final_merged_set