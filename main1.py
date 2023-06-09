# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:12:28 2023

@author: Nabeel
"""

# This is a sample Python script.
from Data_Representation import Data_Representation
from Document_Ranking import Document_Ranking
from Indexing import Indexing
from Query_Matching import Query_Matching
from Read_file import Read_file
from Text_Processing import TextProcessing
from Query_Refinement import Query_Refinement
from Query_Suggestion import Query_Suggestion
from LTR_Model import LTR_Model
from Evaluation import Evaluation

'''
processing = TextProcessing()

processing.preprocess_input_file('C:/Users/Nabeel/.ir_datasets/antique/collection.csv',
                                 'C:/Users/Nabeel/.ir_datasets/antique/clean.csv')
'''

reader = Read_file()
print("========= Now IN READ FILE ==========")
documents , df =reader.read_file("C:/Users/Nabeel/.ir_datasets/antique/orginal_date.csv")
#documents , df =reader.read_file("C:/Users/Nabeel/.ir_datasets/antique/orginal_date.csv")

print("========= Now IN data_representation ==========")
indexer = Indexing()
print("========= Now IN inverted_index ==========")
posting_list , vectorizer , corpus = indexer.build_inverted_index(df)
indexer.store_inverted_index(posting_list, "C:/Users/Nabeel/.ir_datasets/antique/posting_list2.csv")
indexer.print_inverted_index()
#indexer.store_inverted_index(posting_list, "C:/Users/Nabeel/.ir_datasets/wikIR1k/posting_list2.csv")
#indexer.store_inverted_index(posting_list, "C:/Users/Mohammed/reemo_saly.csv")
#indexer = Indexing()
#posting_list = indexer.load_inverted_index()
#query = "southern methodist university"
query2 = "iraq oil"

query = "What do you mean by weed ?"
top = Document_Ranking().documents_Ranking(query,corpus,posting_list,documents,df)

#LTR=======================
ltr_model = LTR_Model()
for idd , text , score in ltr_model.MakeModel(top):
    print("ID:",idd ,"\ntext:",text,"\nscore:",score)

refine = Query_Refinement()
refine.refine_queries_file("C:/Users/Nabeel/.ir_datasets/wikIR1k/test/queries.csv","C:/Users/Nabeel/.ir_datasets/wikIR1k/test/refineQuery.csv") 
suggest = Query_Suggestion("C:/Users/Nabeel/.ir_datasets/wikIR1k/test/refineQuery.csv")
similar_queries  = suggest.suggest_similar_queries(query,n=5)
print("Query Similier : ======>")
print("Query is : " , query)
for i,s in enumerate(similar_queries):
    print(i,",",s)

evaluation = Evaluation()
evaluation.Qalc(corpus, posting_list, documents, "C:/Users/Nabeel/.ir_datasets/antique/test/Querls.txt",df)
results = evaluation.evaluate()

print("MAP:", results["MAP"])
print("Recall:", results["Recall"])
print("MRR:", results["MRR"])
print("P@10:", results["P@10"])
