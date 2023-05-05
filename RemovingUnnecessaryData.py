import pandas as pd
import re
from bs4 import BeautifulSoup
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from num2words import num2words
import ssl

import nltk
#downloading nltk content(can cause an exception)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#downloading nltk content(can cause an exception)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def secondSt(df):
    #removing first rows with names and dates of the report
    def remove_names_and_date(page_html_text):
        min_num_of_words = 13
        p_index = 0
        parsed_html = BeautifulSoup(page_html_text, "html.parser")
        p_lines = parsed_html.findAll("p")

        for p_line in p_lines:
            strong_lines = p_line.findAll("strong")
            if not strong_lines:
                continue

            for s in strong_lines:
                if len(s.text.split(" ")) >= min_num_of_words:
                    break
                else:
                    p_index += 1
                    continue
            for i in range(0, p_index):
                page_html_text = page_html_text.replace(str(p_lines[i]), "")

        return page_html_text

    #removing links(<a> tags) from text
    def remove_links_maps(page_html_text):
        parsed_html = BeautifulSoup(page_html_text, "html.parser")
        p_lines = parsed_html.findAll("p")
        p_index = -1

        for p_line in p_lines:
            p_index += 1
            a_lines = p_line.findAll("a")
            if not a_lines:
                continue
            else:
                page_html_text = page_html_text.replace(str(p_lines[p_index]), "")

        div_lines = parsed_html.findAll("div")
        div_index = -1

        for div_line in div_lines:
            div_index += 1
            a_lines = div_line.findAll("a")
            if not a_lines:
                continue
            else:
                page_html_text = page_html_text.replace(str(div_lines[div_index]), "")

        return page_html_text

    #removing different unique strings 
    def remove_unique(page_html_text):
        page_html_text = re.sub(r"http(\S+.*\s)", "", page_html_text)
        page_html_text = re.sub(r"ttp(\S+.*\s)", "", page_html_text)
        page_html_text = re.sub(r"\[(\d+)\]", "", page_html_text)
        page_html_text = re.sub(r"(2022|2023|©2022|©2023)", "", page_html_text)
        page_html_text = re.sub(r"[0-9]", "", page_html_text)
        page_html_text = re.sub(r"^\[Source.*\]$","", page_html_text)
        page_html_text = re.sub(r"^Russian.*org\)$","", page_html_text)
        page_html_text = page_html_text.replace("Key Takeaways", "")
        page_html_text = page_html_text.replace("Satellite image  Maxar Technologies.", "")
        page_html_text = page_html_text.replace("Note: ISW does not receive any classified material from any source, uses only publicly available information, and draws extensively on Russian, Ukrainian, and Western reporting and social media as well as commercially available satellite imagery and other geospatial data as the basis for these reports. References to all sources used are provided in the endnotes of each update.", "")
        page_html_text = page_html_text.replace("Appendix A – Satellite Imagery", "")
        page_html_text = page_html_text.replace("glava_lnr_info", "")
        page_html_text = page_html_text.replace("kremlin dot ru/events/president/news/70367", "")
        page_html_text = page_html_text.replace("10 U.S. Code § 885 - Art. 85. Desertion | U.S. Code | US Law | LII / Legal Information Institute (cornell.edu)", "")
        page_html_text = page_html_text.replace("https//denis-pushilin  dot ru/doc/ukazy/Ukaz_15_23012023 dot pdf", "")
        page_html_text = page_html_text.replace("Who is Russia's 'butcher of Syria,' now leading the invasion of Ukraine? : NPR Russian General Officer Guide ISW May 11 .pdf (understandingwar.org)", "")
        page_html_text = page_html_text.replace("Russian Units Severely Undermanned as They Prepare for Kherson Defense—U.K. (newsweek.com)", "")

        return page_html_text

    #removing words with one letter
    def remove_one_letter_words(data):
        words = word_tokenize(str(data))

        new_text = ""
        for w in words:
            if len(w) > 1:
                new_text = new_text + " " + w

        return new_text

    #converting to lower case
    def convert_to_lower_case(data):
        return np.char.lower(data)

    #removing words from nltk.stopwords
    def remove_stop_words(data):
        stop_words = set(stopwords.words("english"))
        not_stop_words = {"no", "not"}
        stop_words = stop_words - not_stop_words

        words = word_tokenize(str(data))

        new_text = ""

        for w in words:
            if w not in stop_words:
                new_text = new_text + " " + w

        return new_text

    #removing punctuation marks
    def remove_punctuation(data):
        return re.sub(r'[^\w\s]', '', data)

    #lemmatizing function
    def lemmatizing(data):
        lemmatizer = WordNetLemmatizer()

        tokens = word_tokenize(str(data))
        new_text = ""
        for w in tokens:
            new_text = new_text+" "+lemmatizer.lemmatize(w)
        return new_text

    #removing months, pm_am, th
    def remove_months_pm_am_th(data):
        data = re.sub(r"(january|february|march|april|may|june|july|august|september|october|november|december)", "", data)
        data = re.sub(r"(\bpm\b|\bam\b)","",data)
        data = re.sub(r"\bth\b","",data)
        return data


    def preprocess(data):
        deta = remove_one_letter_words(data)
        data = convert_to_lower_case(data)
        data = remove_stop_words(data)
        data = remove_punctuation(data)
        data = lemmatizing(data)
        data = remove_stop_words(data)
        data = remove_punctuation(data)
        data = remove_months_pm_am_th(data)

        return data



    df['main_html_v2'] = df['main_text'].apply(lambda x: remove_names_and_date(x))
    df['main_html_v2.1'] = df['main_html_v2'].apply(lambda x: remove_links_maps(x))
    df['main_html_v3'] = df['main_html_v2.1'].apply(lambda x: remove_unique(x))
    df['main_html_v4'] = df['main_html_v3'].apply(lambda x: BeautifulSoup(x, "html.parser").text)
    df["report_text"] = df['main_html_v4'].apply(lambda x: preprocess(x))

    return df
