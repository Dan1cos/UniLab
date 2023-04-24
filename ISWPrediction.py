import pandas as pd
import save_page
import IswPrediction_2
import IswPrediction_3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date

#dictionary from documents
INPUT_FOLDER_2 = "data"
DATA_FILE_2 = "parsed_isw.csv"
df_for_dict = pd.read_csv(f"{INPUT_FOLDER_2}/{DATA_FILE_2}", sep=";").fillna(" ")

def take_vector_from_isw(date_input):
    # Convert the string date into a datetime object using strptime()
    date_object = datetime.strptime(date_input, '%d.%m.%Y')

    # Get today's date
    today = date.today()

    # Check if input date is tomorrow or later
    if date_object.date() >= today:
        # Set data_object to today's date
        date_object = today

    # Take date for yesterday
    date_object = date_object - timedelta(days=1)

    # Take content from page
    content = save_page.take_page(date_object)

    all_data = []
    # Extract main text from ISW report
    parsed_html = BeautifulSoup(content)
    text_main = parsed_html.body.find("div", attrs={
        'class': "field field-name-body field-type-text-with-summary field-label-hidden"})
    d = {
        "date": date_object,
        "main_text": str(text_main)
    }
    # Create data frame with date and main text for future processing
    all_data.append(d)
    df = pd.DataFrame.from_dict(all_data)

    # Clean text
    df_st2 = IswPrediction_2.secondSt(df)

    # Creat vector from text
    keywords = IswPrediction_3.thirdSt(df_st2, df_for_dict)
    return keywords

#test
#date_input = "28.04.2023"
#keywords = take_vector_from_isw(date_input)
#for i in keywords:
#    print(i)
