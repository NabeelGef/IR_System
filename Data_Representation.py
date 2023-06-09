import re
from sklearn.feature_extraction.text import CountVectorizer

class Data_Representation:
    def data_representation(self, documents):
        # Define a custom preprocessor to remove numbers
        def remove_numbers(text):
            return re.sub(r'\d+', '', text)

        # Create the CountVectorizer object with the custom preprocessor and binary=True to get a boolean matrix
        vectorizer = CountVectorizer(preprocessor=remove_numbers, binary=True)

        # Fit the vectorizer to the documents
        count_matrix = vectorizer.fit_transform([doc[1] for doc in documents])
        vocabulary = vectorizer.get_feature_names_out()

        # Print the length of the vocabulary
        print("Length of vocabulary:", len(vocabulary))

        return count_matrix, vocabulary, vectorizer