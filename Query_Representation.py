import csv
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from Prepro_Query import Prepro_Query


class Query_Representation:
    def get_query_vector(self,input_query_str, input_vectorizer):
        preprocessed_query = Prepro_Query().preprocess_query(input_query_str)

        # Compute the TF-IDF vector for the query
        query_vector = input_vectorizer.transform([' '.join(preprocessed_query)]).toarray()

        return query_vector
