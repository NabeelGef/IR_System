import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import re
class Prepro_Query:
    def preprocess_query(self,text):
        # Convert text to lowercase
        text = text.lower()

        # Remove commas
        text = re.sub(r',', '', text)

        # Remove non-alphabetic characters
        text = re.sub(r'[^\w\s]', '', text)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        filtered_text = [word for word in text.split() if word not in stop_words]

        # Lemmatize the remaining words
        lemmatizer = WordNetLemmatizer()
        preprocessed_text = [lemmatizer.lemmatize(word) for word in filtered_text if word.isalpha()]

        return preprocessed_text


