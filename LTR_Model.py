# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:48:23 2023

@author: Nabeel
"""

import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score
from sklearn.linear_model import LinearRegression

# Read dataset from file
class LTR_Model:
    
    def MakeModel(self,top_10_matching_docs):
        relevance_scores = []
        for doc_id, doc_text , similarity_score in top_10_matching_docs:
            relevance_score = input("\nHow relevant is Document {} to your query? (Enter 1-5)".format(doc_id))
            relevance_scores.append(int(relevance_score))

        # Prepare the labeled dataset
        X = []
        Y = relevance_scores
        for doc_id, doc_text, similarity_score in top_10_matching_docs:
            feature_vector = [similarity_score]  # add more features here if needed
            X.append(feature_vector)

        # Train the LTR model
        model = LinearRegression()
        model.fit(X, Y)

        # Use the model for ranking
        feature_vectors = []
        for doc_id, doc_text, similarity_score in top_10_matching_docs:
            feature_vector = [similarity_score]  # add more features here if needed
            feature_vectors.append(feature_vector)

        predicted_scores = model.predict(feature_vectors)
        ranked_docs = [(doc_id, doc_text, predicted_score) for (doc_id, doc_text,similarity_score), predicted_score in
                       zip(top_10_matching_docs, predicted_scores)]
        ranked_docs = sorted(ranked_docs, key=lambda x: x[1], reverse=True)

        return ranked_docs