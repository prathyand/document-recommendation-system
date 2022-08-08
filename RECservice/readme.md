## File structure:

```
.
└── RECservice/
    ├── app/
    │   ├── dbconnector.py
    │   ├── sent_embedding.py
    │   ├── update_scores.py
    │   ├── sm2Like.py
    │   ├── webserver.py
    │   ├── cache/
    │   │   ├── keyidmap.json
    │   │   ├── keylist.txt
    │   │   ├── profile.json
    │   │   └── vectors.index
    │   └── entrypoint.sh
    ├── Dockerfile
    └── requirements.txt
```

## sent_embedding.py

This module is responsible for:
- Checking if the database has been updated with new documents by `zoteroapiserv` for parsing and indexing. It maintains a list of previously processed documents in `cache/keylist.txt`

- Creating embedding vectors for new documents using `all-MiniLM-L6-v2` pretrained transformer model

- Indexing newly created embedding vectors using `faiss` library and storing the indices in `cache/vectors.index`

- Maintain and update the document `keyid` and its corresponding `index-id` mapping in `cache/keyidmap.json`

## update_scores.py

This module contains useful functions for updating recommendations, calculating user_profile vector from user interaction data and user preferences, updating user_preferences with changes triggered from the UI and serving search query requests by generating search results.

some of the important functions:
- **`update_profile (index)` :**  This function takes `faiss index` as an input and calculates the weighted user profile vector based on user interactions. Another user profile vector is calculated using user preferences stored in `cache/profile.json`. These two profile vectors are weighted equally (0.5, 0.5) to calculate the final profile vector which is further used in ranking the documents based on cosine similarity.
- **`retrieve_user_profile()` :**  This function simply returns the user preferences stored in `cache/profile.json`

- **`update_user_profile (newdata)` :** This function takes new user preferences as a list, and updates these preferences into `cache/profile.json`

- **`updateSnoozePriority()` :** This function checks for any overdue reminders for snoozed items, and changes the priority value based on length of overdue period 

- **`update_recoms (updateindex=False)` :** This function acts as a trigger to updates the recommendations based on latest user profile vector (generated `update_profile`)

- **`search (searchquery,querykeyid,k=None)` :** This function is triggered every time user uses  the'search' feature from the UI. Django passes the search query to this function, which returns `k` most relevant document `keyid` to django API. 


## sm2Like.py
This module contains useful functions for spaced repetition algorithm(sm2) based recommendation generation.

some of the important functions:
- **`sm2like (quality,repetitions,previous_interval,previous_ef)` :**  This function takes four input, quality,repetitions,previous_interval,previous_ef. The function returns three outputs: interval, repetitions, and ease factor. All three values should be saved and passed to the next call to SM-2 as inputs.
more about [SM-2](https://github.com/thyagoluciano/sm2)

- **`calculate_sm2like (keyidList)` :**
This function takes the list of documents' `keyid` as an input and updates the next interval for each document in the list based on the sm2 logic. Changes are commited to the database immediately. 

- **`updateStatus()` :**
This function checks for any incorrect/invalid `curr_status` field and updates the interval and `curr_status` based on user interaction.

## dbconnector.py

This is small helper module containing useful functions to create and close connections with the `mysql` database

## webserver.py
This is a flask API interface to handle API calls between Django(`backendAPI`) and `RECservice`