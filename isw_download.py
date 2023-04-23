import requests
from calendar import monthrange

OUTPUT_FOLDER = "isw"
BASE_URL = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-"

def save_page(url, file_name):
    page = requests.get(url)
    
    url_name = url.split("/")[-1].replace("-","_")
    
    with open(f"{OUTPUT_FOLDER}/{file_name}__{url_name}.html", 'wb+') as f:
        f.write(page.content)


# # 2022 February24 - December31

months = ['january', 'february' ,'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
Year = 2022
mon_ind = 1

for m in months[1:]:
    mon_ind += 1
    
    if m == 'february':
        first_day = 24
        day_count = monthrange(Year, mon_ind)
        
        for d in range(first_day, day_count[1]+1):
            date = f"{m}-{d}"
            file_name = f"{Year}_{mon_ind}_{d}"
            
            feb_urls = {
                24: "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment",
                25: "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022",
                26: "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26",
                27: "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-27",
                28: "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-28-2022"
            }
            
            url = feb_urls.get(d);
            save_page(url, file_name)
    
    else:
        first_day = 1
        day_count = monthrange(Year, mon_ind)
        
        for d in range(first_day, day_count[1]+1):
            date = f"{m}-{d}"
            file_name = f"{Year}_{mon_ind}_{d}"
            url = f"{BASE_URL}{date}"
            
            save_page(url, file_name)


# # 2023 January 2 - 25

m = 'january'
mon_ind = 1
Year = 2023
first_day = 2 #no data about 1 January

for d in range(first_day, 26):
    date = f"{m}-{d}-{Year}"
    file_name = f"{Year}_{mon_ind}_{d}"
    url = f"{BASE_URL}{date}"
    
    save_page(url, file_name)