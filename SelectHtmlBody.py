from datetime import datetime
import pandas as pd
import glob
from bs4 import BeautifulSoup

INPUT_DATA_FOLDER = "isw"

OUTPUT_FOLDER = "isw_parsed"
OUTPUT_DATA_FILE = "records.csv"

files_by_days = glob.glob(f"{INPUT_DATA_FOLDER}/*.html")

all_data = []

for file in files_by_days:
    d = {}

    file_name = file.split("/")[-1].split("__")
    date = datetime.strptime(file_name[0],"%Y_%m_%d")
    url = file_name[1].split(".")[0]

    with open(file, "r") as cfile:
        parsed_html = BeautifulSoup(cfile.read())
        text_main = parsed_html.body.find("div", attrs={'class':"field field-name-body field-type-text-with-summary field-label-hidden"})

        d = {
            "date": date,
            "url": url,
            "main_text": text_main
        }

        all_data.append(d)

df = pd.DataFrame.from_dict(all_data)
df = df.sort_values(by=['date'])
df.to_csv(f"{OUTPUT_FOLDER}/{OUTPUT_DATA_FILE}",sep=";", index=False)