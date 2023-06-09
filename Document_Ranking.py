import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Query_Matching import Query_Matching


class Document_Ranking:
    def documents_Ranking(self,query_str,Corpus,posting_list,documents,df):
        print("======================  I'm in Top_matching_documents   ===================")
        top_matching_docs = Query_Matching().matching_query_documents(query_str,Corpus, posting_list, documents,df)
    #top_10_matching_docs = sorted(top_matching_docs, key=lambda x: x[2], reverse=True)[:20]

        for doc_id, doc_text, score in top_matching_docs:
          print("Document ID:", doc_id)
          print("Document text:", doc_text)
          print("Cosine similarity:", score)
        return top_matching_docs

 # Ask the user for feedback on the results
