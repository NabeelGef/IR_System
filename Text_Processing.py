from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import csv



class TextProcessing:
    def preprocess_input_file(self, input_file_path, output_file_path):
        stop_words = set(stopwords.words('english'))
        stemmer = SnowballStemmer("english")
        lemmatizer = WordNetLemmatizer()

        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            reader = csv.reader(input_file, delimiter='\t') # \t 
            writer = csv.writer(output_file)

            for row in reader:
                # Tokenize, filter, stem, and lemmatize the text field
                tokens = word_tokenize(row[1])
                filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
                stemmed_and_lemmatized_tokens = [lemmatizer.lemmatize(stemmer.stem(token), pos="v") for token in filtered_tokens]
                stemmed_and_lemmatized_field = ' '.join(stemmed_and_lemmatized_tokens)

                # Write the cleaned row to the output file
                writer.writerow([row[0], stemmed_and_lemmatized_field])




