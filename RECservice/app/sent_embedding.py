# from unittest import result
# import nltk

from sentence_transformers import SentenceTransformer
import numpy as np
from os import path
import os
import faiss
from dotenv import load_dotenv
import json
from dbconnector import dbconnector as db

load_dotenv()

def getEncoding(data):
   bi_encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
   bi_encoder.max_seq_length = 512
   dataembedding = bi_encoder.encode(data,  show_progress_bar=True)
   print(dataembedding.shape)
   dataembedding = np.array([embedding for embedding in dataembedding]).astype("float32")
   return dataembedding

def update_index(return_index=True):
   dbobj = db()
   cursordb = dbobj.get_cursor() 

   if not os.path.exists('cache'):
      os.makedirs('cache')

   querykeys='''SELECT keyid FROM '''+ os.environ['MYSQL_TABLENAME']

   cursordb.execute(querykeys)

   myresult = [str(i[0]) for i in cursordb.fetchall()]
   keystoprocess=[]

   if not path.exists("cache/keylist.txt"):
      keystoprocess=myresult

   else:
      with open('cache/keylist.txt') as f:
         currentkeylist = [str(line.strip()) for line in f.readlines()]

      f.close()
      keystoprocess=set(myresult)-set(currentkeylist)
      print("curr keylist len ",len(currentkeylist)," new list len:",len(myresult))
      

   if not keystoprocess:
      print("all keys processed")
      dbobj.close_cnx()
      if return_index:
         return faiss.read_index("cache/vectors.index")
      else:
         return True

   else:
      print("need to process ",keystoprocess," docs")

      keystoprocess=list(keystoprocess)
      in_params = ','.join(['%s'] * len(keystoprocess))
      query = '''SELECT keyid,title,tags,descrptn FROM '''+ os.environ['MYSQL_TABLENAME']+''' WHERE keyid IN (%s)''' % in_params
      cursordb.execute(query,keystoprocess)
      docs=[(str(i[0]),str(i[1])+str(i[2])+str(i[3])) for i in cursordb.fetchall()]

      # New keys and their docs data
      keystoprocess=[i[0] for i in docs]
      docs=[i[1] for i in docs]

      # Function to remove special characters
      def remove_special_characters(character):
         if character.isalnum() or character == ' ':
            return True
         else:
            return False
      
      #clean data and create embeddings
      cachedStopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])
      docs= [''.join(filter(remove_special_characters, sente))for sente in docs]
      docs=[' '.join([word for word in sente.split() if word not in cachedStopWords]) for sente in docs]

      corpus_embeddings = getEncoding(docs)

      print("len of corpus emb list",len(corpus_embeddings),"\n"
            "len of corpus emb vector",len(corpus_embeddings[0]),"\n")

      check_keyidmap=True
      # Check for an index file
      if not path.exists("cache/vectors.index"):
         index = faiss.index_factory(corpus_embeddings.shape[1], "Flat", faiss.METRIC_INNER_PRODUCT)
         check_keyidmap=False
      else:
         index=faiss.read_index("cache/vectors.index")

      
      next_index_id = index.ntotal

      if check_keyidmap:
         if not path.exists("cache/keyidmap.json"):
            print("missing keyid map")
            return False
         else:
            f = open("cache/keyidmap.json", "r")
            keymapdata = json.load(f)
            f.close()

            for i in range(len(keystoprocess)):
               keymapdata[next_index_id]=keystoprocess[i]
               next_index_id+=1
            
            f = open("cache/keyidmap.json", "w")
            json.dump(keymapdata, f)
            f.close()


      else:
         keymapdata = {}

         for i in range(len(keystoprocess)):
               keymapdata[next_index_id]=keystoprocess[i]
               next_index_id+=1
            
         with open("cache/keyidmap.json", 'w') as f:
            json.dump(keymapdata, f)

         f.close()

      #Add embedding vectors to the index
      faiss.normalize_L2(corpus_embeddings)
      index.add(corpus_embeddings)

      #save index to files
      faiss.write_index(index, "cache/vectors.index")
      print(f"Number of vectors in the Faiss index: {index.ntotal}")

      with open("cache/keylist.txt","a+") as f:
         for row in keystoprocess:
            f.write(str(row) + '\n')
      f.close()

      dbobj.close_cnx()

      if return_index:
         return index
      else:
         return True

if __name__ == "__main__":
   update_index(False)
