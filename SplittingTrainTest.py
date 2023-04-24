import pandas as pd
import numpy as np
from sklearn import preprocessing
from datetime import datetime

final_merged_set = pd.read_csv(f"path to set", sep = ";")

le = preprocessing.LabelEncoder()
le.fit(final_merged_set["hour_conditions"].unique())
final_merged_set["hour_conditions"] = le.transform(final_merged_set["hour_conditions"])

le2 = preprocessing.LabelEncoder()
le2.fit(final_merged_set["hour_preciptype"].unique())
final_merged_set["hour_preciptype"] = le2.transform(final_merged_set["hour_preciptype"])

final_merged_set["day_sunrise"] = final_merged_set["day_sunrise"].\
    apply(lambda x: datetime.strptime(x,"%H:%M:%S").hour*60+datetime.strptime(x,"%H:%M:%S").minute)
final_merged_set["day_sunset"] = final_merged_set["day_sunset"].\
    apply(lambda x: datetime.strptime(x,"%H:%M:%S").hour*60+datetime.strptime(x,"%H:%M:%S").minute)

###Splitting into test and train
train_percent = .8
time_between = final_merged_set.hour_datetimeEpoch.max() - final_merged_set.hour_datetimeEpoch.min()
train_cutoff = final_merged_set.hour_datetimeEpoch.min() + train_percent*time_between
train_df = final_merged_set[final_merged_set.hour_datetimeEpoch <= train_cutoff]
test_df = final_merged_set[final_merged_set.hour_datetimeEpoch > train_cutoff]
