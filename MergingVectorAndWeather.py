import pandas as pd
import json
import IswPrediction_final
import CollectForecast
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
#import plotly as plotly

def isNaN(num):
    return num != num

def update_df_vector(df, keywords):
    # Split the first row into a list of keys
    keys = df.iloc[0].str.split(';', expand=True).values[0]

    # Replace the values in the second row with those from the keywords vector
    for key, value in keywords.items():
        if key in keys:
            index = keys.tolist().index(key)
            df.iloc[1, index] = value

    return df


date = date_input = "23.04.2023"
vector2 = IswPrediction_final.take_vector_from_isw(date_input)
vector1 = pd.read_csv('D:/PythonLab/UniLab/data/vector_v2_dates.csv', sep=';')

#print(vector1)

updated_vector_df = update_df_vector(vector1, vector2)
#print(updated_df)

df_weather = CollectForecast.getNewForecast()
#print(df_weather.columns)
#print(updated_vector_df.columns)
 
final_merged_set = df_weather.merge(updated_vector_df,
                                    how="left",
                                    left_on=["datetime"],
                                     right_on=["date"])


final_merged_set = final_merged_set.replace(np.nan,0)
final_merged_set.to_csv(f"D:/PythonLab/UniLab/data/final_merged_set.csv", sep=";", index=False)
