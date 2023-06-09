import pandas as pd
class Queries_File:

 def Queries_File (self):
     #"C:/Users/Nabeel/.ir_datasets/wikIR1k/test/queries.csv"
     #"C:/Users/Nabeel/.ir_datasets/antique/test/queries.txt"
     filename = "C:/Users/Nabeel/.ir_datasets/wikIR1k/test/queries.csv"
     df = pd.read_csv(filename, sep=",", header=None, names=["doc_id_query", "doc_text_query"]) #\t
     print("NOW IAM IN Queries_File")
     return df;

