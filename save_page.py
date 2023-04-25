from datetime import timedelta
import requests

BASE_URL = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-"

def save_page(url, date_object):
    page = requests.get(url)

    # Check link status
    if page.status_code != 200:
        # take yesterday date
        date_object = date_object - timedelta(days=1)
        take_page(date_object)

    return page.content




def take_page(date_object):
    # Extract day, month, and year from the datetime object
    d = date_object.day
    m = date_object.strftime('%B').lower()
    year = date_object.year

    date = f"{m}-{d}-{year}"
    url = f"{BASE_URL}{date}"

    # output_folder = 'prediction'
    page = save_page(url, date_object)
    return page