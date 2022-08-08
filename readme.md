# research-dashboard

## Requirements:
 ```
latest version of docker/docker compose
 ```
## Instructions:

1. Clone the repository
 ```
git clone git@github.iu.edu:prateeks/research-dashboard.git
```
2. Configure user preferences in:
```
zoteroapiserv/app/userProfile.json
```
**userProfile.json** 
```json
{"ZoteroUserID":"1234567",
"ZOTERO_API_SECRET_KEY":"aF2cfw18ikd92VpqnQFpAVoY",
"git_repository_list":["prathyand/samplerepo","prathyand/floorplan_obfuscation"],
"gitAuthenticationToken":"ghp_foEuMidWdbm3nzPaSvrxWNGeNHcVfY0KSJbC",
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
![Input3](images/sm2like_recom.drawio.png?raw=true "smwlike")
## Web UI

![Input2](images/UI_1.png?raw=true "ui")

![Input2](images/UI_2.png?raw=true "ui")