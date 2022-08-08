from dotenv import load_dotenv
import os
from os import path
import requests
import urllib
import json
from urllib.parse import quote_plus
from datetime import datetime,timedelta
from dbconnector import dbconnector as db
import acm_scrapper_service as scrapper
import git_scrapper as gitscrp
import arxivApi as arxivapi

load_dotenv()

class ZoteroFetch:
    FIELDS_TO_FETCH ={"key","itemType","title","creators","abstractNote","date","shortTitle","url","tags","dateAdded"}
    BASE_URL="https://api.zotero.org/users/"
    CONTENT_TYPE="items?"
    PARAMS={'format':"json",
            'limit':100,
            'itemType':"Report || WebPage || Preprint"
            }
    headers={"Authorization":""}
    requestURL = BASE_URL
    fetchedVersion=None

    def __init__(self):
        f = open("userProfile.json", "r")
        upro = json.load(f)
        f.close()

        self.headers["Authorization"]='Bearer '+upro['ZOTERO_API_SECRET_KEY']
        self.requestURL+=str(upro["ZoteroUserID"])+"/"+self.CONTENT_TYPE

    
    def __fetchdata(self):
        
        if not path.exists("cache/lastLibraryversion.json"):
            print("missing lastLibraryversion, fetching all items")
            self.PARAMS['since']=0
            libraryversionData={'Last-Modified-Version':0}
            f = open("cache/lastLibraryversion.json", "w")
            json.dump(libraryversionData, f)
            f.close()

        else:
            f = open("cache/lastLibraryversion.json", "r")
            libraryversionData = json.load(f)
            f.close()
            self.PARAMS['since']=int(libraryversionData['Last-Modified-Version'])
            print("Fetching changes since version ",libraryversionData['Last-Modified-Version'])


        params = urllib.parse.urlencode(self.PARAMS, safe="|",quote_via=urllib.parse.quote)
        r= requests.get(self.requestURL, params=params,headers=self.headers)


        if r.status_code==200:
            print("Fetch successfull status:",r.status_code)
            yield r.json()
            lk=r.headers['Link']
            
            self.fetchedVersion = r.headers['Last-Modified-Version']

            if self.fetchedVersion==self.PARAMS['since']:
                print("nothing to update ")
                return 


            nxt=lk.find('rel="next"')
            while(nxt!=-1):
                prev=lk.find('rel="prev"')
                if prev==-1:
                    nxtlnk=lk[lk.find('<')+1:lk.find('>')]
                else:
                    nxtlnk=lk[lk.find('<',prev+11,len(lk))+1:lk.find('>',prev+11,len(lk))]
                r= requests.get(nxtlnk,headers=self.headers)
                lk=r.headers['Link']
                yield r.json()
                # print("nextJson:",r.json())
                nxt=lk.find('rel="next"')
        else:
            print("Fetch unsuccessfull status:",r.status_code)
            yield None

    def __parseData(self,data):
        # parse data
        for ind,jobj in enumerate(data):
            jobj=jobj['data']
            keys=list(jobj.keys())
            for k in keys:
                if k not in self.FIELDS_TO_FETCH:
                    jobj.pop(k,None)
            jobj['key'] = jobj['key'].replace('.','-')
            s=""
            for tagitem in jobj['tags']:
                s+=tagitem['tag']+"<>"
            if s:
                jobj['tags']=s[:-2]

            jobj['source']='zotero'
            if 'date' in jobj and jobj['date']:
                d=jobj['date']
                jobj['date']=str(datetime.strptime(d, "%Y-%m-%d"))
            else:
                jobj.pop("date", None)

            if 'arxiv.org' in jobj['url']:
                jobj['doc_url'] = "http://arxiv.org/pdf/"+jobj['url'][jobj['url'].rfind('/')+1:]
            if 'creators' in jobj:
                atslst=jobj['creators']
                authorname=""
                for cname in atslst:
                    authorname+=cname.get("firstName", "")+" "+cname.get("lastName", "")+","
                authorname=authorname[:-1]
                jobj['authors']=authorname
            data[ind]=jobj
        return data

    def requestData(self):
        data=[]
        for r in self.__fetchdata():
            if r is not None:
                data.extend(r)
        if not data:
            print("No data in response")
            return None
        else:
            return self.__parseData(data)

def sendDatatoDB(resp,mode=None):
    success=False
    MAPPINGS = {'key':'keyid','itemType':'itemType','source':'source','authors':'authors','title':'title',
                'abstractNote':'descrptn','date':'dateMod','url':'urllink','tags':'tags','doc_url':'doc_url'}
    dbobj = db()
    cursordb = dbobj.get_cursor()
    try:
        querystring='''REPLACE INTO '''+ os.environ['MYSQL_TABLENAME']
        if resp:
            someFailed = 0
            for dp in resp:
                columns='''('''
                vals=[]
                valsString='''('''
                for k,v in dp.items():
                    if k in MAPPINGS:
                        ctype=MAPPINGS[k]
                        columns+=ctype+''','''
                        valsString+='''%s,'''
                        vals.append(str(v))
                columns=columns[:-1]+''')'''
                valsString=valsString[:-1]+''')'''
                query = querystring+''' '''+ columns+''' VALUES '''+valsString
                # print(query)
                try:
                    
                    cursordb.execute(query,tuple(vals))
                except Exception as e:
                    someFailed+=1
                    print(e)

            if someFailed==0:
                print("All changes updated in the DB ")
                success=True

                if mode=='zotero':
                    f = open("cache/lastLibraryversion.json", "r")
                    libraryversionData = json.load(f)
                    f.close()
                    libraryversionData['Last-Modified-Version']=zf.fetchedVersion

                    f = open("cache/lastLibraryversion.json", "w")
                    json.dump(libraryversionData, f)
                    f.close()

            else:
                success=True
                print("{} items not inserted in the DB for {}".format(someFailed,mode))

        else:
            print("Nothing to update")
            success=True

        dbobj.close_cnx()

        return success

    except Exception as e:
        print(e)
        dbobj.close_cnx()
        success=False
        return success

if __name__=="__main__":
    # Check for logs
    zotero_needsupdate=False
    arxiv_needsupdate=False
    git_needsupdate=False
    if not os.path.exists('cache'):
      os.makedirs('cache')
    if not path.exists("cache/updatelogs.json"):
        newlog={}
        lastup = datetime.now()-timedelta(hours=1.5)
        lastup=lastup.strftime("%Y-%m-%d %H:%M:%S")
        newlog['zotero'] = lastup
        newlog['arxiv'] = lastup
        newlog['git'] = lastup
        f = open("cache/updatelogs.json", "w")
        json.dump(newlog, f)
        f.close()
        zotero_needsupdate=True
        arxiv_needsupdate=True
        git_needsupdate=True
    else:
        f = open("cache/updatelogs.json", "r")
        currlog = json.load(f)
        f.close()

        if currlog.get('zotero'):
            zut=datetime.strptime(currlog['zotero'],"%Y-%m-%d %H:%M:%S")
            deltaz = (datetime.now()-zut).total_seconds()/3600
            print("last zotero update was %s hours ago"%deltaz)
            if deltaz>1:
                zotero_needsupdate=True
        else:
            zotero_needsupdate=True

        if currlog.get('arxiv'):
            arxut=datetime.strptime(currlog['arxiv'],"%Y-%m-%d %H:%M:%S")
            deltaarx = (datetime.now()-arxut).total_seconds()/3600
            print("last arxiv update was %s hours ago"%deltaarx)
            if deltaarx>1:
                arxiv_needsupdate=True
        else:
            arxiv_needsupdate=True

        if currlog.get('git'):
            zut=datetime.strptime(currlog['git'],"%Y-%m-%d %H:%M:%S")
            deltaz = (datetime.now()-zut).total_seconds()/3600
            print("last git update was %s hours ago"%deltaz)
            if deltaz>1:
                git_needsupdate=True
        else:
            git_needsupdate=True


    if zotero_needsupdate:
        # Fetching Zotero data
        zf = ZoteroFetch()
        resp=zf.requestData()
        result=sendDatatoDB(resp,'zotero')

        if result:
            print("Zotero Update Successfull\nSaving timestamp")
            f = open("cache/updatelogs.json", "r")
            currlog = json.load(f)
            f.close()
            lastup = datetime.now()
            lastup=lastup.strftime("%Y-%m-%d %H:%M:%S")
            currlog['zotero']=lastup
            f = open("cache/updatelogs.json", "w")
            json.dump(currlog, f)
            f.close()

    
    if arxiv_needsupdate:
        # Fetching arxiv data
        result=sendDatatoDB(arxivapi.fetcharxivData(),mode="arxiv")
        if result:
            print("arxiv Update Successfull\nSaving timestamp")
            f = open("cache/updatelogs.json", "r")
            currlog = json.load(f)
            f.close()
            lastup = datetime.now()
            lastup=lastup.strftime("%Y-%m-%d %H:%M:%S")
            currlog['arxiv']=lastup
            f = open("cache/updatelogs.json", "w")
            json.dump(currlog, f)
            f.close()

    if git_needsupdate:
        # Fetching arxiv data
        result=sendDatatoDB(gitscrp.fetchRepoData(),mode="git")
        if result:
            print("git Update Successfull\nSaving timestamp")
            f = open("cache/updatelogs.json", "r")
            currlog = json.load(f)
            f.close()
            lastup = datetime.now()
            lastup=lastup.strftime("%Y-%m-%d %H:%M:%S")
            currlog['git']=lastup
            f = open("cache/updatelogs.json", "w")
            json.dump(currlog, f)
            f.close()
    # scrapper.updateCONFs()
    # gitscrp.fetchLatestcommit()


