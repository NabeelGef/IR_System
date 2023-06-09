import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Prepro_Query import Prepro_Query
from Query_Representation import Query_Representation
class Query_Matching_Evaluation:
        def matching_query_documents(self, query, corpus, input_posting_list, documents,dfr):
            # Preprocess the query
            cor = dfr['text'].fillna('default_value')

            preprocessed_query = Prepro_Query().preprocess_query(query)

            # Find the matching documents
            matching_docs = set()
            for term in preprocessed_query:
                if term in input_posting_list:
                    postings_list = input_posting_list[term]
                    matching_docs.update(postings_list)

            # Compute the TF-IDF vectors for the matching documents
            vectorizer = TfidfVectorizer()
            matched_docs_with_scores = []

            for doc_idx in matching_docs:
                c = corpus[doc_idx]
                if len( c) > 0:
                    # Compute the TF-IDF vector for the matching documents
                    tfidf_matrix = vectorizer.fit_transform([c for doc_idx in matching_docs ])

                    # Compute the TF-IDF vector for the query
                    query_tfidf = vectorizer.transform([query])

                    # Compute the cosine similarity between the query vector and the matching document vectors
                    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix)

                    # Create a list of tuples with document ID, document text, and cosine similarity score


            # Create a list of tuples with document ID, document text, and cosine similarity score
                    matched_docs_with_scores = [(doc_id, documents[doc_id], score) for doc_id, score in
                                        zip(matching_docs, cosine_similarities[0])]

            return matched_docs_with_scores
