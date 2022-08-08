import requests
import json
import requests
import dateutil.parser


GIT_URL_PREFIX = 'https://api.github.com/repos/'

def fetchLatestcommit(repo,headers,old_etag=None):
    eurl =GIT_URL_PREFIX+repo+"/events"
    print(eurl)
    if old_etag:
        headers['If-None-Match']=old_etag
    

    
    r= requests.get(eurl,headers=headers)

    if r.status_code==304:
        print("no changes in repo: ",repo)
        return 

    if r.status_code==200:
        body=r.json()

        #Update Etag
        etag=r.headers['ETag']
        print(etag)
        f = open("cache/lastLibraryversion.json", "r")
        libraryversionData = json.load(f)
        f.close()
        libraryversionData[repo+'_ETag']=etag
        f = open("cache/lastLibraryversion.json", "w")
        json.dump(libraryversionData, f)
        f.close()
        dlist=[]
        for item in body:
            # Check for pushevent
            if item['type']!="PushEvent":
                continue
            objd ={}
            objd['key']=item['id']
            objd['source']='github'
            objd['itemType']=item['type']
            objd['url']='https://github.com/'+repo+"/commit/"+item['payload']['commits'][0]['sha']
            objd['title']=repo+" - "+item['type']
            objd['abstractNote']=item['payload']['commits'][0]['message']
            objd['date']=str(dateutil.parser.parse(item['created_at']))
            objd['authors'] = item['payload']['commits'][0]['author']['name']
            objd['tags']="git"
            dlist.append(objd)
        return dlist

    else:
        print("Error in fetching data from: ",repo)
        return 



def fetchRepoData():
    #load all the Etags
    f = open("cache/lastLibraryversion.json", "r")
    etagData = json.load(f)
    f.close()
    f = open("userProfile.json", "r")
    upro = json.load(f)
    f.close()

    REPOS=upro['git_repository_list']

    data =[]
    headers = {'Authorization':'token '+upro['gitAuthenticationToken']}
    for repo in REPOS:
        etg = etagData.get(repo+"_ETag")
        print("passing etag",etg)
        d=fetchLatestcommit(repo,headers,etg)
        if d:
            data.extend(d)

    print("fetched total %d items"%len(data))

    return data
