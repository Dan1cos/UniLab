from datetime import datetime

import requests

BASE_URL = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-"


def save_page(url, file_name, output_folder):
    page = requests.get(url)

    url_name = url.split("/")[-1].replace("-", "_")

    with open(f"{output_folder}/{file_name}__{url_name}.html", 'wb+') as f:
        f.write(page.content)


def take_page(date_input):
    # Convert the string date into a datetime object using strptime()
    date_object = datetime.strptime(date_input, '%d.%m.%Y')

    # Extract day, month, and year from the datetime object
    d = date_object.day
    mon_ind = date_object.month
    m = date_object.strftime('%B').lower()
    year = date_object.year

    # Print the results
    # print(d, m, year)

    date = f"{m}-{d}-{year}"
    file_name = f"{year}_{mon_ind}_{d}"
    url = f"{BASE_URL}{date}"

    output_folder = 'prediction'
    save_page(url, file_name, output_folder)
