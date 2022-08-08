
from bs4 import BeautifulSoup
import dateutil.parser
import hashlib
from dotenv import load_dotenv
import os
from dbconnector import dbconnector as db
import feedparser
import urllib.request
import json


# Category Taxonomy : https://arxiv.org/category_taxonomy
TOPICS =['cs.CV','cs.DC','cs.AI','cs.LG']
START_INDEX=0
MAX_INDEX=20

BASE_URL="http://export.arxiv.org/api/query?"

def encode_feedparser_dict(d):
    if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
        j = {}
        for k in d.keys():
            j[k] = encode_feedparser_dict(d[k])
        return j
    elif isinstance(d, list):
        l = []
        for k in d:
            l.append(encode_feedparser_dict(k))
        return l
    else:
        return d

def getidfromurl(url):
    ix = url.rfind('/')
    idversion = url[ix+1:]
    idversion=idversion.replace('.','-')
    return idversion

def getobjectDictionary(j):
    objd = {}
    extrid = getidfromurl(j['id'])
    objd['key']=extrid
    objd['source']='arxiv'
    objd['itemType']='report'

    if 'authors' in j:
        atstr=""
        for ia in j['authors']:
            atstr+=ia['name']+","
        atstr=atstr[:-1]
        objd['authors']=atstr
        # print(atstr)
           

    objd['title']=j['title']
    objd['abstractNote']=j['summary'].strip()
    objd['date']=str(dateutil.parser.parse(j['updated']))
    objd['url']=j['link']
    objd['doc_url']="http://arxiv.org/pdf/"+objd['url'][objd['url'].rfind('/')+1:]
    tstr=""
    for tg in j['tags']:
        tstr+=tg['term']+"<>"
    tstr=tstr[:-2]
    objd['tags']=tstr

    return objd

def fetcharxivData():
    load_dotenv()
    dbobj = db()
    cursordb = dbobj.get_cursor()
    try:
        getkeysQuery = '''SELECT keyid from recom WHERE source = %s'''
        cursordb.execute(getkeysQuery,('arxiv',))
        existing_keys=set([i[0] for i in cursordb.fetchall()])
        dbobj.close_cnx()
        # print(existing_keys)
    except Exception as e:
        dbobj.close_cnx()
        print(e)

    f = open("userProfile.json", "r")
    upro = json.load(f)
    f.close()

    RESULTS_PER_QUERY = int(upro['arxiv_fetchNewItemsLimit'])

    fetchQuery='cat:'+'+OR+cat:'.join(upro['arxiv_subscribed_topics'])
    DataList=[]
    for i in range(START_INDEX,MAX_INDEX,RESULTS_PER_QUERY):
        query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (fetchQuery,
                                                                                    i, RESULTS_PER_QUERY)
        # print(i,query)
        print(BASE_URL+query)
        with urllib.request.urlopen(BASE_URL+query) as url:
            response = url.read()
        parse = feedparser.parse(response)

        for e in parse.entries:

            j = encode_feedparser_dict(e)
            if getidfromurl(j['id']) in existing_keys:
                continue

            DataList.append(getobjectDictionary(j))

    return DataList





