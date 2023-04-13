##### Merging data
import pandas as pd
import numpy as np
#from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler


df_weather_v5 = pd.read_csv(f"D:/PythonLab/UniLab/df_weather_v5.csv", sep = ";")
vector_v2_dates = pd.read_csv(f"D:/PythonLab/UniLab/vector_v2_dates.csv", sep = ";")

###If you want to change 0 to NaN
#df_tfidf_v2 = df_tfidf.replace(0, np.nan)

final_merged_set = df_weather_v5.merge(vector_v2_dates,
                                     how="left",
                                     left_on=["day_datetime"],
                                     right_on=["date"])

###Splitting into test and train
train_percent = .8
time_between = final_merged_set.hour_datetimeEpoch.max() - final_merged_set.hour_datetimeEpoch.min()
train_cutoff = final_merged_set.hour_datetimeEpoch.min() + train_percent*time_between
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
"day_sunrise", #convert to epoch
"day_sunset", #convert to eppch
"hour_datetime",
"date"
]

def isNaN_v2(num):
    return pd.notna(num)



train_target = train_df["event_start"]
train_target = train_target.apply(lambda x: isNaN_v2(x))
train_df = train_df.drop(events_exclude, axis=1)
train_df = train_df.fillna(0)

test_target = test_df["event_start"]
test_target = test_target.apply(lambda x: isNaN_v2(x))
test_df = test_df.drop(events_exclude, axis=1)
test_df = test_df.fillna(0)

scaler = StandardScaler()
train_df = scaler.fit_transform(train_df)
test_df = scaler.transform(test_df)



# Create an instance of the logistic regression model


model = SGDClassifier()
model.fit(train_df, train_target)

y_pred = model.predict(test_df)

# Evaluate the model's performance

accuracy = accuracy_score(test_target, y_pred)
precision = precision_score(test_target, y_pred)
confusionmatrix = confusion_matrix(test_target, y_pred)
recall = recall_score(test_target, y_pred)
f1 = f1_score(test_target, y_pred)

# Print the evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Vonfusionmatrix:", confusionmatrix)
print("Recall:", recall)
print("F1 score:", f1)

# Save the trained model as a pickle file

import pickle

# Save the model to disk
filename = '5__StochasticGradientDescent__v1'
with open('5__StochasticGradientDescent__v1.pkl', 'wb') as file:pickle.dump(model, file)


