import save_page
import pandas as pd
import glob
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

BASE_URL = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-"

def firstSt(date_object, INPUT_DATA_FOLDER, OUTPUT_DATA_FILE):
    OUTPUT_FOLDER = INPUT_DATA_FOLDER

    saved = False
    #take yesterday date
    date_object = date_object - timedelta(days=1)

    # open folder with html files for prediction
    files_by_days = glob.glob(f"{INPUT_DATA_FOLDER}/*.html")

    # check if the page already saved
    for file in files_by_days:
        file_name = file.split("\\")[-1].split("__")
        date = datetime.strptime(file_name[0], "%Y_%m_%d")

        if (date == date_object):
            saved = True
            break;

    if not saved:
        save_page.take_page(date_object)

    # Extract day, month, and year from the datetime object
    d = date_object.day
    mon_ind = date_object.month
    m = date_object.strftime('%B').lower()
    year = date_object.year

    date = f"{m}-{d}-{year}"
    file_name = f"{year}_{mon_ind}_{d}"
    url = f"{BASE_URL}{date}"
    url_name = url.split("/")[-1].replace("-", "_")

    file = glob.glob(f"{INPUT_DATA_FOLDER}/{file_name}__{url_name}.html")

    # open html file
    all_data = []
    with open(file[0], "r") as cfile:
        parsed_html = BeautifulSoup(cfile.read())
        text_main = parsed_html.body.find("div", attrs={
            'class': "field field-name-body field-type-text-with-summary field-label-hidden"})

        d = {
            "date": date_object,
            "url": url_name,
            "main_text": text_main
        }

        all_data.append(d)

    # add data to csv
    df = pd.DataFrame.from_dict(all_data)

    df.to_csv(f"{OUTPUT_FOLDER}/{OUTPUT_DATA_FILE}", sep=";", index=False)