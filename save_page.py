from datetime import datetime, timedelta
import requests

BASE_URL = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-"

def save_page(url, file_name, output_folder, date_object):
    page = requests.get(url)

    url_name = url.split("/")[-1].replace("-", "_")
    # Check link status
    if page.status_code == 200:
        with open(f"{output_folder}/{file_name}__{url_name}.html", 'wb+') as f:
            f.write(page.content)
    else:
        # take yesterday date
        date_object = date_object - timedelta(days=1)
        take_page(date_object)



def take_page(date_object):
    # Extract day, month, and year from the datetime object
    d = date_object.day
    mon_ind = date_object.month
    m = date_object.strftime('%B').lower()
    year = date_object.year

    date = f"{m}-{d}-{year}"
    file_name = f"{year}_{mon_ind}_{d}"
    url = f"{BASE_URL}{date}"

    output_folder = 'D:/PythonLab/UniLab/prediction'
    save_page(url, file_name, output_folder, date_object)
