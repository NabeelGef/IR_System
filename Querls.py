import csv

import pandas as pd


class Querls :
    def fr(self, queries_file):
        print("hi")
        with open(queries_file, "r") as f: #names=["query_id", "d", "doc_iid", "rank"]
             dfi = pd.read_csv(queries_file, sep=",", header=None, names=["d", "query_id", "doc_iid", "rank"])# ' ' + names=
             print("NOW IAM IN Queries_File")
             for index, row in dfi.iterrows():
                    query_id = row['query_id']
                    doc_id = row['doc_iid']
                    rank = row['rank']
                    print(query_id)
