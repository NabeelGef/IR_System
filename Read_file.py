import pandas as pd
from dateutil import parser
from datetime import datetime
import re

class Read_file:
    def format_text(text):
        date_strings = re.findall(r"\d{1,4}[/\-]\d{1,2}[/\-]\d{1,4}", text)  
        for date_string in date_strings:
            formatted_date =Read_file.format_date(date_string)
            text = text.replace(date_string, formatted_date)
        return text
    def format_date(date_string):
        try:
            date_obj = parser.parse(date_string)
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            return date_string    
    def remove_numbers(text):
        return re.sub(r'\d+', '', text)
    def remove_one_chracter(text):
        return re.sub(r'\b\w{1}\b', '', text)
    def remove_spaces(text):
        return re.sub(r'\s+', ' ', text)
    def remove_words_with_repeated_chars(text):
        pattern = r"\b\w*(\w)\1\w*\b"  # Matches words with repeated characters
        return re.sub(pattern, "", text)
    def read_file(self, file_path):
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, header=None, names=['doc_id', 'text']) # doc_id

        # Limit the number of documents to 3000
        #df = df.iloc[:3000]

        # Fill missing values with a default value
        #df['text'] = df['text'].fillna('default_value')

        # Preprocess the text in each document
        corpus = {}
        for i, row in df.iterrows():
            doc_id = row['doc_id'] #doc_id
            text = row['text']
            #text = Read_file.format_text(text)
            #text = Read_file.remove_numbers(text)
            #text = Read_file.remove_one_chracter(text)
            #text = Read_file.remove_spaces(text)
            #text = Read_file.remove_words_with_repeated_chars(text)
            
            words = re.sub(r'[^\w\s]', '', str(text)).split()
            words =  [word for word in words if len(word) > 2]
            cleaned_text = ' '.join(words)
            corpus[doc_id] = cleaned_text

        # Convert the corpus to a list of (doc_id, preprocessed_text) tuples
        documents = list(corpus.items())

        # Print out the preprocessed text for each document
        # for doc_id, preprocessed_text in corpus.items():
        #     print("Document", doc_id, ":", preprocessed_text)

        return documents,df

