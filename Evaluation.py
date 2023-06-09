import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, recall_score, label_ranking_average_precision_score
import csv
from Queries_File import Queries_File
from Query_Matching import Query_Matching
from Query_Matching_Evaluation import Query_Matching_Evaluation


class Evaluation:
    def Qalc(self, corpus, input_posting_list, documents, queries_file,dfr):
        self.query_relevant_docs = {}

        with open(queries_file, "r") as f:#names=["query_id", "d", "doc_iid", "rank"]
            dfi = pd.read_csv(queries_file, sep=",", header=None,names=["d", "query_id", "doc_iid", "rank"]) #' 'edit name
            print("NOW IAM IN Queries_File")

            for index, row in dfi.iterrows():
                query_id = row['query_id']
                doc_id = row['doc_iid']
                rank = row['rank']
                print(query_id)
                if query_id not in self.query_relevant_docs:
                    self.query_relevant_docs[query_id] = []
                self.query_relevant_docs[query_id].append((doc_id, rank))

        self.df = Queries_File().Queries_File()
        self.query_matching_old = Query_Matching()
        self.query_matching = Query_Matching_Evaluation()
        self.corpus = corpus
        self.input_posting_list = input_posting_list
        self.documents = documents
        self.queries_file = queries_file
        self.dfr = dfr

    def run_query(self, query_id):
        doc_text_query_mask = self.df['doc_id_query'] == query_id
        print("hiiiii")
        if not doc_text_query_mask.any():
            print('nabeeelo')
            return []
        print(f"hiiiii from doc_text_query and the doc_text_query is ")
        doc_text_query = self.df.loc[doc_text_query_mask, 'doc_text_query'].iloc[0]
        if len(doc_text_query) > 0:
            matched_docs_with_scores = self.query_matching.matching_query_documents(doc_text_query, self.corpus,
                                                                                    self.input_posting_list,
                                                                                  self.documents,self.dfr)
            ranked_docs = [doc_text[0] for doc_id, doc_text, score in
                           sorted(matched_docs_with_scores, key=lambda x: x[2], reverse=True)[:200]]
            # Return the top 200 matching documents
            return ranked_docs
        else:
            return []

    def evaluate(self):
        map_score = 0.0
        recall = 0.0
        mrr_score = 0.0
        p_at_10 = 0.0
        precision = 0.0
        num_queries = len(self.query_relevant_docs)

        print(f"query_relevant_docs = {self.query_relevant_docs}")

        for query_id in self.query_relevant_docs.keys():
            ranked_doc_ids = self.run_query(query_id)

            relevant_docs = [doc_id for doc_id, _ in self.query_relevant_docs[query_id]]
            y_true = [1 if doc_id in relevant_docs else 0 for doc_id in ranked_doc_ids]
            y_scores = np.linspace(1, 0, len(ranked_doc_ids))
            y_scores_binary = [1 if score >= 0.5 else 0 for score in y_scores]


            print(
                f"Query {query_id}: relevant_docs = {relevant_docs}, ranked_doc_ids = {ranked_doc_ids}, y_true = {y_true}, y_scores = {y_scores}")

            if not any(y_true):
                print(f"No relevant documents found for query {query_id}")
                continue

            if not any(y_scores):
                print(f"No scores found for ranked documents in query {query_id}")
                continue

            # Calculate recall
            recall += recall_score(y_true, y_scores_binary, average='binary')
            map_score += average_precision_score(y_true, y_scores_binary)
            # Calculate MRR
            for i, doc_id in enumerate(ranked_doc_ids):
                if doc_id in relevant_docs:
                    mrr_score += 1.0 / (i+1)
                    break

            # Calculate P@10
            p_at_10 += np.sum(y_true[:10]) / 10

        recall /= num_queries
        mrr_score /= num_queries
        p_at_10 /= num_queries

        return {
            "MAP": map_score,
            "Recall": recall,
            "MRR": mrr_score,
            "P@10": p_at_10,
        }


# import numpy as np
# import pandas as pd
# from sklearn.metrics import average_precision_score, recall_score, label_ranking_average_precision_score
# import csv
#
# from Queries_File import Queries_File
# from Query_Matching import Query_Matching
# from Query_Matching_Evaluation import Query_Matching_Evaluation
# class Evaluation:
#         def Qalc(self, corpus, input_posting_list, documents, queries_file):
#             self.query_relevant_docs = {}
#
#             with open(queries_file, "r") as f:
#                 dfi = pd.read_csv(queries_file, sep=" ", header=None, names=["query_id", "d", "doc_iid", "rank"])
#                 print("NOW IAM IN Queries_File")
#
#                 for index, row in dfi.iterrows():
#                     query_id = row['query_id']
#                     doc_id = row['doc_iid']
#                     rank = row['rank']
#                     print(query_id)
#                     if query_id not in self.query_relevant_docs:
#                         self.query_relevant_docs[query_id] = []
#                     self.query_relevant_docs[query_id].append((doc_id, rank))
#
#             self.df = Queries_File().Queries_File()
#             self.query_matching = Query_Matching_Evaluation()
#             self.corpus = corpus
#             self.input_posting_list = input_posting_list
#             self.documents = documents
#             self.queries_file = queries_file
#
#         def run_query(self, query_id):
#             doc_text_query_mask = self.df['doc_id_query'] == query_id
#             print("hiiiii")
#             if not doc_text_query_mask.any():
#                 return []
#             print("hiiiii from doc_text_query and the doc_text_query is {doc_text_query} ")
#             doc_text_query = self.df.loc[doc_text_query_mask, 'doc_text_query'].iloc[0]
#             matched_docs_with_scores = self.query_matching.matching_query_documents(doc_text_query, self.corpus,
#                                                                                     self.input_posting_list,
#                                                                                     self.documents)
#             ranked_docs = [doc_text[0] for doc_id, doc_text, score in
#                            sorted(matched_docs_with_scores, key=lambda x: x[2], reverse=True)[:100]]
#             # Return the top 20 matching documents
#             return ranked_docs
#
#     def evaluate(self):
#         map_score = 0.0
#         recall = 0.0
#         mrr_score = 0.0
#         p_at_10 = 0.0
#         precision = 0.0
#         num_queries = len(self.query_relevant_docs)
#
#         print(f"query_relevant_docs = {self.query_relevant_docs}")
#
#         for query_id in self.query_relevant_docs.keys():
#             ranked_doc_ids = self.run_query(query_id)
#
#             relevant_docs = [doc_id for doc_id, rank in self.query_relevant_docs[query_id]]
#             y_true = [1 if doc_id in relevant_docs else 0 for doc_id in ranked_doc_ids]
#             y_scores = np.linspace(1, 0, len(ranked_doc_ids))
#
#             print(
#                 f"Query {query_id}: relevant_docs = {relevant_docs}, ranked_doc_ids = {ranked_doc_ids}, y_true = {y_true}, y_scores = {y_scores}")
#
#             if not any(y_true):
#                 print(f"No relevant documents found for query {query_id}")
#                 continue
#
#             if not any(y_scores):
#                 print(f"No scores found for ranked documents in query {query_id}")
#                 continue
#
#             map_score += average_precision_score(y_true, y_scores)
#             recall += recall_score(y_true, relevant_docs)
#             mrr_score += 1.0 / (np.argmax(y_true) + 1)
#             p_at_10 += np.mean(y_true[:10])
#
#         map_score /= num_queries
#         recall /= num_queries
#         mrr_score /= num_queries
#         p_at_10 /= num_queries
#
#         return {
#             "MAP": map_score,
#             "Recall": recall,
#             "MRR": mrr_score,
#             "P@10": p_at_10,
#         }
#
#     # class Evaluation:
#         #     def Qalc(self, corpus, input_posting_list, documents, queries_file):
#         #         self.query_relevant_docs = {}
#         #
#         #         with open(queries_file, "r") as f:
#         #             dfi = pd.read_csv(queries_file, sep=" ", header=None, names=["query_id", "d", "doc_iid", "rank"])
#         #             print("NOW IAM IN Queries_File")
#         #
#         #             for index, row in dfi.iterrows():
#         #                 query_id = row['query_id']
#         #                 doc_id = row['doc_iid']
#         #                 rank = row['rank']
#         #                 print(query_id)
#         #                 if query_id not in self.query_relevant_docs:
#         #                     self.query_relevant_docs[query_id] = []
#         #                 self.query_relevant_docs[query_id].append((doc_id, rank))
#         #
#         #         self.df = Queries_File().Queries_File()
#         #         self.query_matching = Query_Matching_Evaluation()
#         #         self.corpus = corpus
#         #         self.input_posting_list = input_posting_list
#         #         self.documents = documents
#         #         self.queries_file = queries_file
#         #
#         #     def run_query(self, query_id):
#         #         doc_text_query_mask = self.df['doc_id_query'] == query_id
#         #         print("hiiiii")
#         #         if not doc_text_query_mask.any():
#         #             return []
#         #         print("hiiiii from doc_text_query and the doc_text_query is {doc_text_query} ")
#         #         doc_text_query = self.df.loc[doc_text_query_mask, 'doc_text_query'].iloc[0]
#         #         matched_docs_with_scores = self.query_matching.matching_query_documents(doc_text_query, self.corpus,
#         #                                                                                 self.input_posting_list,
#         #                                                                                 self.documents)
#         #         ranked_docs = [doc_text[0] for doc_id, doc_text, score in
#         #                        sorted(matched_docs_with_scores, key=lambda x: x[2], reverse=True)[:100]]
#         #         # Return the top 20 matching documents
#         #         return ranked_docs
#
#             # def evaluate(self):
#             #     map_score = 0.0
#             #     recall = 0.0
#             #     mrr_score = 0.0
#             #     p_at_10 = 0.0
#             #     precision = 0.0
#             #     num_queries = len(self.query_relevant_docs)
#             #
#             #     print(f"query_relevant_docs = {self.query_relevant_docs}")
#             #
#             #     for query_id in self.query_relevant_docs.keys():
#             #         ranked_doc_ids = self.run_query(query_id)
#             #
#             #         relevant_docs = [doc_id for doc_id, rank in self.query_relevant_docs[query_id]]
#             #         y_true = [1 if doc_id in relevant_docs else 0 for doc_id in ranked_doc_ids]
#             #         y_scores = np.linspace(1, 0, len(ranked_doc_ids))
#             #
#             #         print(
#             #             f"Query {query_id}: relevant_docs = {relevant_docs}, ranked_doc_ids = {ranked_doc_ids}, y_true = {y_true}, y_scores = {y_scores}")
#             #
#             #         if not any(y_true):
#             #             print(f"No relevant documents found for query {query_id}")
#             #             continue
#             #
#             #         if not any(y_scores):
#             #             print(f"No scores found for ranked documents in query {query_id}")
#             #             continue
#             #
#             #         map_score += average_precision_score(y_true, y_scores)
#             #         recall += recall_score(y_true, relevant_docs)
#             #         mrr_score += 1.0 / (np.argmax(y_true) + 1)
#             #         p_at_10 += np.mean(y_true[:10])
#             #
#             #     map_score /= num_queries
#             #     recall /= num_queries
#             #     mrr_score /= num_queries
#             #     p_at_10 /= num_queries
#             #
#             #     return {
#             #         "MAP": map_score,
#             #         "Recall": recall,
#             #         "MRR": mrr_score,
#             #         "P@10": p_at_10,
#             #     }
#
#             import numpy as np
#             import pandas as pd
#             from sklearn.metrics import average_precision_score, recall_score, label_ranking_average_precision_score
#             import csv
#
#             from Queries_File import Queries_File
#             from Query_Matching import Query_Matching
#             from Query_Matching_Evaluation import Query_Matching_Evaluation