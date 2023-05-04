import pickle
import pandas as pd
import json
import numpy as np
import logging
from datetime import datetime
from os.path import exists
import MergingVectorAndWeather

PATH_TO_MODEL = "models/5__decision_tree_classifier__v2.pkl"
PATH_TO_REGIONS = "data/regions.csv"
OUTPUT_FOLDER = "data"
OUTPUT_CSV = "predictedAlarms.csv"
OUTPUT_LOG = "timestamps.log"

#checking if the log file is present, logging first run of the script
if not exists(f"{OUTPUT_FOLDER}/{OUTPUT_LOG}"):
    logging.basicConfig(filename=f"{OUTPUT_FOLDER}/{OUTPUT_LOG}", format='%(asctime)s %(message)s')
    logging.warning('')

#loading model
file = open(f"{PATH_TO_MODEL}", 'rb')
clf = pickle.load(file)
file.close()

#creading dataframe for today 
df = makingMergedForEachHour.createDataSet(datetime.today().strftime("%d.%m.%Y"))

#making prediction in model
pred = clf.predict(df)
received = pd.DataFrame(pred, columns=["prediction"])

#editing received information
regions_df = pd.read_csv(f"{PATH_TO_REGIONS}", sep=",")
received["region_id"] = df["region_id"]
received["hour_datetimeEpoch"] = df["hour_datetimeEpoch"]
received["hour_datetimeEpoch"] = received["hour_datetimeEpoch"].apply(
    lambda x: datetime.fromtimestamp(x).strftime("%H:%M:%S"))
received = received.rename(columns={"hour_datetimeEpoch": "time"})
received = received.merge(regions_df[["center_city_en", "region_id"]], how="left", left_on=["region_id"],
                          right_on=["region_id"])

#exporting to the csv file
received.to_csv(f"{OUTPUT_FOLDER}/{OUTPUT_CSV}", mode='a', sep=";", index=False)

#adding log
logging.basicConfig(filename=f"{OUTPUT_FOLDER}/{OUTPUT_LOG}", format='%(asctime)s %(message)s')
logging.warning('')
