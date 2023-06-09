import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Prepro_Query import Prepro_Query
from Query_Representation import Query_Representation
class Query_Matching:
    def matching_query_documents(self, query, corpus, input_posting_list, documents,df):
           # Preprocess the query
           cor = df['text'].fillna('default_value')
           preprocessed_query = Prepro_Query().preprocess_query(query)

           # Find the matching documents
           matching_docs = set()
           for term in preprocessed_query:
               if term in input_posting_list:
                   postings_list = input_posting_list[term]
                   matching_docs.update(postings_list)

           # Compute the TF-IDF vectors for the matching documents
           vectorizer = TfidfVectorizer()
           tfidf_matrix = vectorizer.fit_transform(cor)
           tfidf_matrix_doc = tfidf_matrix[list (matching_docs)]
           # Compute the TF-IDF vector for the query
           query_tfidf = vectorizer.transform([query])

           # Compute the cosine similarity between the query vector and the matching document vectors
           cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix_doc)

           # Create a list of tuples with document ID, document text, and cosine similarity score
           matched_docs_with_scores = [(doc_id, documents[doc_id], score) for doc_id, score in
                                       zip(matching_docs, cosine_similarities[0])]
           matched_docs_with_scores = sorted(matched_docs_with_scores, key=lambda x: x[2], reverse=True)

           # Return the top 20 matching documents
           top_20_matching_docs = matched_docs_with_scores[:20]

           return top_20_matching_docs    
        
        #return matched_docs_with_scores
        # Compute the cosine similarity between the query vector and the matching document vectors
        #cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix)

        # Sort the matching documents by their cosine similarity score
        
        #matched_docs_with_scores = [(documents[doc_idx], score) for doc_idx, score in
        #                            zip(matching_docs, cosine_similarities[0][0])]
        
        #matched_docs_with_scores = sorted(matched_docs_with_scores, key=lambda x: x[1], reverse=True)

        
