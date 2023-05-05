import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pickle

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

def isNaN_v2(num):
    return pd.notna(num)

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

with open("models/modelName.pkl", "wb") as f:
    pickle.dump(clf, f)
