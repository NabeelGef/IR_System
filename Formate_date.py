from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import csv
import re
from dateutil import parser
def format_date(date_string):
    try:
        date_obj = parser.parse(date_string)
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        return date_string


def format_text(text):
    date_strings = re.findall(r"\d{1,4}[/\-]\d{1,2}[/\-]\d{1,4}", text)
    for date_string in date_strings:
        formatted_date = format_date(date_string)
        text = text.replace(date_string, formatted_date)
    return text


with open('C:/Users/Mohammed/orginal.csv', 'r', encoding='utf-8') as csvfile, open(
        'C:/Users/Mohammed/orginal_date.csv', 'w', newline='', encoding='utf-8') as writer:
    reader = csvfile.read()
    # writer = csv.writer(writer)
    text = format_text(reader)
    writer.write(text)
