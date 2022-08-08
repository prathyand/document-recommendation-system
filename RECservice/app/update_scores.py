import enum
import sent_embedding as se
import json
import numpy as np
from os import path
import os
import faiss
from pandas import DataFrame
import pandas as pd
from dotenv import load_dotenv
from operator import itemgetter
from dbconnector import dbconnector as db
from datetime import datetime
import sys

def NormalizeData(data):
  return data/np.sum(data)


def update_profile(index):
  dbobj = db()
  cursordb = dbobj.get_cursor()
  columns =['keyid','bookmarkflag','views','rating']
  query='''SELECT %s FROM '''% ','.join(columns)+ os.environ['MYSQL_TABLENAME']+''' WHERE bookmarkflag OR views!=0 OR rating!=0 OR snoozed_date is NOT NULL'''
  # print(query)
  cursordb.execute(query)
  df = DataFrame(cursordb.fetchall())
  dbobj.close_cnx()

  if not df.empty:
    df.columns = columns
    df['weight']=df['views']*0.5+df['rating']*1.+df['bookmarkflag']*5.+10.
    print("df shape",df.shape)
    df['weight'] = df['weight'].astype('float32')

    # Calculate average vector
    f = open("cache/keyidmap.json", "r")
    keymapdata = json.load(f)
    f.close()
    r_keymapdata={}
    for k,v in keymapdata.items():
      r_keymapdata[v]=k
    
    keystoconstruct = [ r_keymapdata[i] for i in df['keyid']]

    retrieved_vectors = np.zeros((len(keystoconstruct),index.d)).astype('float32')

    for i,v in enumerate(keystoconstruct):
      retrieved_vectors[i] = index.reconstruct(int(v))

    # xb= faiss.rev_swig_ptr(index.get_xb(), index.ntotal * index.d)
    # xb = xb.reshape(index.ntotal , index.d)

    weighted_profile_Vector = np.average(retrieved_vectors, weights=NormalizeData(df['weight']),axis=0)
    weighted_profile_Vector=weighted_profile_Vector.reshape(1,index.d)

  # Calculate user preference vector
  if not path.exists("cache/profile.json"):
    pd = {"profile": ["cpu ", "gpu"]}
    f = open("cache/profile.json", "w")
    json.dump(pd, f)
    f.close()
  else:
    f = open("cache/profile.json", "r")
    pd = json.load(f)
    f.close()

  pd=pd['profile']

  if pd:
    pd=' '.join(pd)
    print("current profile looks like: ",pd)
    qv = se.getEncoding(pd)
    qv = qv.reshape(1,index.d)

    try:
      return 0.5*weighted_profile_Vector + 0.5*qv
    except:
      return qv

  try:
      return weighted_profile_Vector
  except:
    return None
  

def retrieve_user_profile():
  if not path.exists("cache/profile.json"):
    newprofile={'profile':tuple([])}
    f = open("cache/profile.json", "w")
    json.dump(newprofile, f)
    f.close()
    return newprofile['profile']

  f = open("cache/profile.json", "r")
  profile = json.load(f)
  f.close()
  print("returning" ,profile['profile'])
  return profile['profile']

def update_user_profile(newdata):

  newprofile={'profile':tuple(newdata)}
  f = open("cache/profile.json", "w")
  json.dump(newprofile, f)
  f.close()
  print("updated data profile ",newdata)
  return True

def updateSnoozePriority():
  dbobj = db()
  cursordb = dbobj.get_cursor()
  columns =['keyid','snoozeval_days','snoozed_date','snooze_priority']
  Qr = '''SELECT %s FROM '''% ','.join(columns) + os.environ['MYSQL_TABLENAME']+ ''' WHERE snoozed_date is NOT NULL AND snoozeval_days>0'''
  cursordb.execute(Qr)
  df = DataFrame(cursordb.fetchall())
  dbobj.close_cnx()
  
  if df.empty:
    print("no snooze items")
    return True

  df.columns = columns

  df['snoozed_date'] = pd.to_datetime(df['snoozed_date'])

  # now = datetime.now()
  df['snooze_priority'] =  df['snoozed_date'].rsub(pd.Timestamp('today')).dt.days
  df[['snooze_priority']] = df[['snooze_priority']].astype(int)
  df['snooze_priority']=df['snooze_priority']-df['snoozeval_days']
  df['snooze_priority']=df['snooze_priority'].apply(lambda x:-2 if x<0 else x)
  dflen = len(df)
  print(df)
  dbobj = db()
  cursordb = dbobj.get_cursor()
  base_Qr = '''UPDATE '''+os.environ['MYSQL_TABLENAME']
  for i in range(dflen):
    Qr=base_Qr+''' SET snooze_priority = %s '''%df['snooze_priority'][i]+'''WHERE keyid =%s '''%("'"+df['keyid'][i]+"'")
    cursordb.execute(Qr)
  dbobj.close_cnx()
  return True


def updateScores(keytuple,scoretuple):
  dbobj = db()
  cursordb = dbobj.get_cursor()
  N = len(keytuple)
  base_Qr = '''UPDATE '''+os.environ['MYSQL_TABLENAME']
  for i in range(N):
    Qr=base_Qr+''' SET score = %s '''%scoretuple[i]+'''WHERE keyid =%s '''%("'"+keytuple[i]+"'")
    cursordb.execute(Qr)
  dbobj.close_cnx()
  print("Updated DB with new scores")
  return True


def update_recoms(updateindex=False):

  # Get the updated index
  if updateindex:
    index = se.update_index()
  else:
    index=faiss.read_index("cache/vectors.index")

  f = open("cache/keyidmap.json", "r")
  keymapdata = json.load(f)
  f.close()

  # Update profile vector
  profilevector=update_profile(index)

  # skip update if no profile vector
  if profilevector is None:
    return True

  #Find cosine similarity
  faiss.normalize_L2(profilevector)
  D, I = index.search(profilevector, len(keymapdata))
  D,I =D[0],I[0]

  D = tuple(D)
  I = tuple([str(i) for i in I])
  sorted_keys=itemgetter(*I)(keymapdata)

  #Update scores
  updateScores(sorted_keys,D)
  updateSnoozePriority()

  print("Updated recommendations")
  return True

def search(searchquery,querykeyid,k=None):

  index=faiss.read_index("cache/vectors.index")

  f = open("cache/keyidmap.json", "r")
  keymapdata = json.load(f)
  f.close()

  if k is None:
    k = min(index.ntotal,30)

  if querykeyid is None:
    qv = se.getEncoding(searchquery)
    qv = qv.reshape(1,index.d)
    faiss.normalize_L2(qv)
    faiss.normalize_L2(qv)

  elif searchquery is None:
    r_keymapdata={}
    for ke,v in keymapdata.items():
      r_keymapdata[v]=ke

    ind_q = int(r_keymapdata[querykeyid])
    qv = index.reconstruct(ind_q)
    qv = qv.reshape(1,index.d)

  else: 
    raise Exception("Invalid search request")

  
  D, I = index.search(qv, k)
  I=list(map(str, list(I[0])))
  I = [keymapdata[i] for i in I]

  if querykeyid is not None:
    I = I[1:]
  
  srRslt ={'Resultkeys':I}
  # print("sending this result ",srRslt)
  
  return srRslt


if __name__=="__main__":
  try:
    initial_run = sys.argv[1].lower() == 'true'
  except:
    initial_run=False
  update_recoms(initial_run)

    

