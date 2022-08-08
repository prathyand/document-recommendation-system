## File structure

```
.
└── RECservice/
    ├── app/
    │   ├── userProfile.json
    │   ├── apiservice.py
    │   ├── arxivApi.py
    │   ├── git_scrapper.py
    │   ├── dbconnector.py
    │   ├── acm_scrapper_service.py
    │   └── cache/
    │       ├── lastLibraryversion.json
    │       └── updatelogs.json
    ├── Dockerfile
    └── requirements.txt 
```

## userProfile.json
This json file contains user settings and preferences which must be defined before the app startup.

**userProfile.json** 
```json
{"ZoteroUserID":"1234567",
"ZOTERO_API_SECRET_KEY":"aF2cfw18ikd92VpqnQFpAVoY",
"git_repository_list":["prathyand/samplerepo","prathyand/floorplan_obfuscation"],
"gitAuthenticationToken":"ghp_foEuMidWdbm3nzPaSvrxWNGeNHcVfY0KSJbC",
"arxiv_subscribed_topics":["cs.CV","cs.DC","cs.AI","cs.LG"],
"arxiv_fetchNewItemsLimit":50
}
```
- **ZoteroUserID:** User's zotero userid [more info](https://www.zotero.org/settings/keys)
- **ZOTERO_API_SECRET_KEY:** secret API key for zotero api [more info](https://www.zotero.org/settings/keys/new)
- **git_repository_list:** list of private and personal repositories to track
- **gitAuthenticationToken:** Personal authentication git token [more info](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- **arxiv_subscribed_topics:** List of topics to track from arxiv api, [more info](https://arxiv.org/category_taxonomy)
- **arxiv_fetchNewItemsLimit:** Number of documents fetched from arxiv api


## apiservice.py

This module is responsible for updating DB from user's Zotero library. This module is the entrypoint of the entire stack. Modules responsible for all other sources of data `(git,arxiv)` are called from this module on startup. Data fetched from different sources is parsed and updated into the databse by calling the `sendDatatoDB()` function from the main function.

Once the data is updated in the database, timestamp of the update for every source is stored in `cache/updatelogs.json`. This is used to avoid multiple calls to APIs in a short span of time. Other parameters such as current `library version`, github repository `ETag`, are stored in `cached/lastLibraryversion.json`, and is used while making new calls to git and zotero APIs which are optimized for polling.

Fields fethed from the zotero api are defined with the `FIELDS_TO_FETCH` variable:
```python
FIELDS_TO_FETCH ={"key","itemType","title","creators","abstractNote","date","shortTitle","url","tags","dateAdded"}
```

## arxivApi.py
This module contains useful functions to access the arxiv api, retrieves new document metadata based on `arxiv_fetchNewItemsLimit` parameter and return the list.

## git_scrapper.py
This module contains helper functions to retrieve new events in repositories in the tracking list. 

## dbconnector.py
This is small helper module containing useful functions to create and close connections with the `mysql` database