import requests
from bs4 import BeautifulSoup
import dateutil.parser
import hashlib
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


base_url='https://dl.acm.org'
CONFERENCES=['ase','icse']
# CONFERENCES=['ice','hpdc','ase','icse']
def fetchProceedingsLink(conferences_list):
    conf_pro_urls=[]
    for conf in conferences_list:
        preq = requests.get(base_url+"/conference/"+conf)
        soup = BeautifulSoup(preq.text, "html.parser")
        tx=soup.find("div",attrs={"class":"tabbed-content tabbed-content--proceedings-tabs"})
        tx=tx.find("li",class_='grid-item')
        conf_pro_urls.append((base_url+tx.a['href'],conf))

    return conf_pro_urls

def fetchlinksonPage(link):
    URLLIST=[]
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    tx=soup.findAll("div",class_="issue-item-container")
    exit=False
    for div in tx:
        dctnry = {}

        links = div.find('h5',class_='issue-item__title')
        
        lk=links.find('a')
        URL=base_url+lk['href']
        dctnry['url']=URL
        dctnry['title']=lk.text
            
        abst = div.find('div',class_='issue-item__abstract truncate-text trunc-done')
        dctnry['abstractNote']=abst.find('p').getText()

        
    return URLLIST

def fetchdocdetails(link):
    print("fetching link ",link)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    docobjct={}
    abstr = soup.find("div",class_="abstractSection abstractInFull")
    try:
        docobjct['descrptn']=abstr.p.getText()
    except Exception as e:
        docobjct['descrptn']=" "
        print(e)
    docobjct['title']=soup.find("title").getText()
    docobjct['dateMod']=str(dateutil.parser.parse(soup.find("span",class_="CitationCoverDate").getText()))
    docobjct['urllink']=link
    docobjct['itemType']=soup.find("span",class_="issue-heading").getText()
    # print(docobjct)
    return docobjct


def fetch():
    sufs=['?tocHeading=heading1','?tocHeading=heading2','?tocHeading=heading3']
    confproclinks=fetchProceedingsLink(CONFERENCES)
    print(confproclinks)
    # lnk='https://dl.acm.org/doi/proceedings/10.1145/3465084'

    for lnk in confproclinks:
        linksset=set()
        docset=[]
        for suf in sufs:
            try:
                linksset.update(fetchlinksonPage(lnk[0]+suf))
            except Exception as e:
                print(e)

        for doclink in linksset:
            keyid=str(doclink)
            keyid=hashlib.md5(keyid.encode())
            keyid=keyid.hexdigest()
            # print("keyid :",keyid)
            docobjct=fetchdocdetails(doclink)
            docobjct['keyid']=keyid
            docobjct['tags']=lnk[1]
            docset.append(docobjct)

        yield docset



def updateCONFs():
    # yd=dateutil.parser.parse("19 April 2022")
    # print(yd)
    config = {
        'user': os.environ['MYSQL_USER'],
        'password': os.environ['MYSQL_PASSWORD'],
        'host': os.environ['MYSQL_HOST'],
        'port': os.environ['MYSQL_PORT'],
        'database': os.environ['MYSQL_DATABASE'] ,
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursordb = cnx.cursor(buffered=False)

    qs='''INSERT IGNORE INTO recom (keyid,itemType,title,descrptn,dateMod,urllink,tags) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    for docsets in fetch():
        for docset in docsets:
            vals=[docset['keyid'],docset['itemType'],docset['title'],docset['descrptn'],docset['dateMod'],docset['urllink'],docset['tags']]
            try:
                cursordb.execute(qs,tuple(vals))
            except Exception as e:
                print(e)

    cnx.commit()
    cnx.close()
    cursordb.close()