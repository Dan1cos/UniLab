import pandas as pd
import IswPrediction_1
import IswPrediction_2
import IswPrediction_3
from datetime import datetime, date

#data after first step
INPUT_FOLDER = "prediction"
DATA_FILE = "pred_isw_v1.csv"

#dictionary from documents
INPUT_FOLDER_2 = "data"
DATA_FILE_2 = "parsed_isw.csv"

def take_vector_from_isw(date_input):
    # Convert the string date into a datetime object using strptime()
    date_object = datetime.strptime(date_input, '%d.%m.%Y')

    # Get today's date
    today = date.today()

    # Check if input date is tomorrow or later
    if date_object.date() >= today:
        # Set data_object to today's date
        date_object = today

    # Check if the page is already download and save it if nessesary. Then save dataframe with html body
    IswPrediction_1.firstSt(date_object, INPUT_FOLDER, DATA_FILE)

    df = pd.read_csv(f"{INPUT_FOLDER}/{DATA_FILE}", sep=";").fillna(" ")
    df_for_dict = pd.read_csv(f"{INPUT_FOLDER_2}/{DATA_FILE_2}", sep=";").fillna(" ")

    # Clean text
    df_st2 = IswPrediction_2.secondSt(df)

    # Creat vector from text
    keywords = IswPrediction_3.thirdSt(df_st2, df_for_dict)

    return keywords

#test
#date_input = "23.04.2023"
#vector = take_vector_from_isw(date_input)
#for i in vector:
#    print(i)
