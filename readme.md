# document-recommendation-system
A document recommendation system based on a hybrid of content based recommendation algorithm (cosine similarity in user profile embedding and document embeddings) and spaced repetition [SM-2](https://github.com/thyagoluciano/sm2)  algorithm.

## :building_construction: System Architecture

![sysarch](images/doc-recom.drawio.svg?raw=true "sysarch")


## Requirements:
 ```
latest version of docker/docker compose
 ```
## Instructions:

1. Clone the repository
 ```
git clone https://github.com/prathyand/document-recommendation-system.git
```
2. Configure user preferences in:
```
zoteroapiserv/app/userProfile.json
```
**userProfile.json** 
```json
{"ZoteroUserID":"1234567",
"ZOTERO_API_SECRET_KEY":"aF2cfw18ikd92VpqqQFpAVoY",
"git_repository_list":["prathyand/samplerepo","prathyand/floorplan_obfuscation"],
"gitAuthenticationToken":"ghp_foEuMidWdbm6nzPaSvrxWNGeNHcVfY0KSJbC",
"arxiv_subscribed_topics":["cs.CV","cs.DC","cs.AI","cs.LG"],
"arxiv_fetchNewItemsLimit":20
}
```

3. Build the project and run from root directory using:
```
docker compose up
```

## Project Structure:
### Project has five major components, each running in it's own docker environment:
- **[zoteroapiserv:](zoteroapiserv/)**  This component is responsible for fetching any updated data from Zotero, Git or arxiv based on configuration parameters set in `zoteroapiserv/app/userProfile.json`

- **[RECservice:](RECservice/)** This component contains the logic for recommendation algorithm based on cosine similarity, sm2like logic, semantic search and generating embeddings from documents

- **[backendAPI](backendAPI/):** This is the Django API interface that handles all API calls to and from Frontend and triggers recommendation update/search events in recommendation engine (RECservice) if necessary

- **RD_webapp:** Front end ReactJS UI

- **[mysqlREC](mysqlREC/):** MySQL database client




---------------------------
## sm2like logic
more about spaced repetition [SM-2](https://github.com/thyagoluciano/sm2)

```python
def sm2like(quality,repetitions,previous_interval,previous_ef):

    if quality>=3:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 3
        else:
            interval = int(round(previous_interval * previous_ef))
        
        repetitions+=1
        easeFactor = previous_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    else:
        repetitions = 0
        interval = 1
        easeFactor = previous_ef

    if (easeFactor < 1.3):
        easeFactor = 1.3
        
    return (interval,repetitions,easeFactor)
```


![Input3](images/sm2like_recom.drawio.png?raw=true "smwlike")
## Web UI

![Input2](images/UI_1.png?raw=true "ui")

![Input2](images/UI_2.png?raw=true "ui")
