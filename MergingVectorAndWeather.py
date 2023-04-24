import pandas as pd
import json
import IswPrediction_final
import CollectForecast
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
#import plotly as plotly

#vector1 = {'soldier': 0.294, 'km': 0.247, 'claimed': 0.177, 'znpp': 0.174, 'oblast': 0.121, 'ownership': 0.12, 'effort': 0.114, 'milblogger': 0.103, 'bakhmut': 0.101, 'not': 0.1, 'patronage': 0.099, 'occupation': 0.098, 'road': 0.093, 'pmcs': 0.092, 'authority': 0.091, 'grossi': 0.091, 'conducted': 0.088, 'near': 0.087, 'likely': 0.085, 'belarusian': 0.084, 'military': 0.082, 'milbloggers': 0.081, 'donetsk': 0.079, 'project': 0.079, 'ukraine': 0.079, 'avdiivka': 0.078, 'wagner': 0.078, 'pmc': 0.077, 'group': 0.076, 'attack': 0.076, 'turbine': 0.076, 'ivanivske': 0.076, 'headway': 0.076, 'news': 0.074, 'subsidy': 0.073, 'wounded': 0.072, 'network': 0.071, 'territory': 0.071, 'provisioning': 0.07, 'block': 0.068, 'simferopol': 0.068, 'hall': 0.068, 'occupied': 0.067, 'component': 0.066, 'compel': 0.064, 'aggregator': 0.064, 'continued': 0.064, 'reported': 0.064, 'belarus': 0.064, 'maintenance': 0.063, 'official': 0.062, 'turning': 0.06, 'recognition': 0.06, 'contributed': 0.06, 'area': 0.059, 'southwest': 0.059, 'russia': 0.059, 'myrne': 0.058, 'evacuation': 0.058, 'railway': 0.058, 'operation': 0.057, 'perform': 0.057, 'injury': 0.057, 'billion': 0.057, 'offensive': 0.057, 'defense': 0.056, 'along': 0.056, 'girkin': 0.055, 'prigozhin': 0.054, 'damage': 0.054, 'medical': 0.053, 'uav': 0.053, 'putin': 0.053, 'main': 0.052, 'mobilization': 0.051, 'henichesk': 0.051, 'west': 0.051, 'veteran': 0.05, 'weapon': 0.05, 'although': 0.05, 'pasechnik': 0.049, 'northwest': 0.049, 'hulyaipole': 0.049, 'prevent': 0.049, 'vehicle': 0.048, 'company': 0.048, 'combat': 0.047, 'ministry': 0.047, 'appeal': 0.047, 'kreminna': 0.046, 'positional': 0.046, 'international': 0.046, 'struggling': 0.045, 'observed': 0.045, 'death': 0.045, 'source': 0.044, 'field': 0.044, 'completed': 0.044, 'no': 0.044, 'made': 0.044}
#print(vector1)


def createDataSet(date_input):
    vector1 = IswPrediction_final.take_vector_from_isw(date_input)
    vector1 = {k: v for d in vector1.values() for k, v in d.items()}
    
    vector2 = pd.read_csv('D:/PythonLab/UniLab/data/vector_v2_dates.csv', sep=';')
    vector2.loc[0] = {}
    for i in vector2.columns:
        if i in vector1:
            vector2[i] = vector1[i]
    vector2 = vector2.fillna(0)
    
    df_weather = CollectForecast.getNewForecast()
    final_merged_set = df_weather.merge(vector2)
    
    return final_merged_set