import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
import json
class Indexing:

    def build_inverted_index(self,data):
        docs = data['text'].fillna('default_value')
        
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(docs)
        # Get vocabulary
        vocabulary = vectorizer.get_feature_names_out()
        print(len(vocabulary))
        # Build inverted index
        inverted_index = defaultdict(set)
        for i, doc in enumerate(X):
            for j, count in zip(doc.indices, doc.data):
                inverted_index[vocabulary[j]].add(i)
        return inverted_index,vectorizer,docs
    def store_inverted_index(self,inverted_index, file_path):
             # Convert set objects to lists in the inverted index
             inverted_index_lists = {term: list(docs) for term, docs in inverted_index.items()}

             # Convert inverted index to JSON string
             inverted_index_json = json.dumps(inverted_index_lists)
             # Write JSON string to file
             with open(file_path, 'w') as file:
                  file.write(inverted_index_json)

    def load_inverted_index(file_path):
            # Read the contents of the file
            with open(file_path, 'r') as file:
                inverted_index_json = file.read()

                # Deserialize the JSON string into a Python dictionary
            inverted_index = json.loads(inverted_index_json)

            return inverted_index

    def print_inverted_index(inverted_index):
            x = 0
            for term, document_ids in inverted_index.items():
                print(f'Term: {term}')
                print(f'Document IDs: {document_ids}')
                x = x + 1
                print('---')
            print(x)