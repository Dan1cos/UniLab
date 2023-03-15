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

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

INPUT_FOLDER = "isw_parsed"
DATA_FILE = "records.csv"

OUTPUT_FOLDER = "isw_parsed_2"
OUTPUT_DATA_FILE = "parsed_isw.csv"

df = pd.read_csv(f"{INPUT_FOLDER}/{DATA_FILE}", sep=";").fillna(" ")


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

def remove_one_letter_words(data):
    words = word_tokenize(str(data))

    new_text = ""
    for w in words:
        if len(w) > 1:
            new_text = new_text + " " + w

    return new_text


def convert_to_lower_case(data):
    return np.char.lower(data)


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


def remove_punctuation(data):
    return np.char.replace(data, string.punctuation, '')


def lemmatizing(data):
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text+" "+lemmatizer.lemmatize(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        if w.isdigit():
            w = num2words(w)
        new_text = new_text+" "+w

    return new_text.replace("-"," ")


def preprocess(data):
    deta = remove_one_letter_words(data)
    data = convert_to_lower_case(data)
    data = remove_stop_words(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = lemmatizing(data)
    data = remove_stop_words(data)
    data = remove_punctuation(data)

    return data

df['main_html_v2'] = df['main_text'].apply(lambda x: remove_names_and_date(x))
df['main_html_v2.1'] = df['main_html_v2'].apply(lambda x: remove_links_maps(x))

df['main_html_v2.2'] = df['main_html_v2.1'].apply(lambda x: re.sub(r"http(\S+.*\s)", "", x))

pattern = "\[(\d+)\]"

df['main_html_v2.3'] = df['main_html_v2.2'].apply(lambda x: re.sub(pattern, "", x))

df['main_html_v3'] = df['main_html_v2.3'].apply(lambda x: re.sub(r"(2022|2023|©2022|©2023)", "", x))

df['main_html_v4'] = df['main_html_v3'].apply(lambda x: BeautifulSoup(x, "html.parser").text)

df["report_text"] = df['main_html_v4'].apply(lambda x:preprocess(x))

df.to_csv(f"{OUTPUT_FOLDER}/{OUTPUT_DATA_FILE}", sep=";", index=False)
