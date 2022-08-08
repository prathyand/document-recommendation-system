## File structure
```
.
└── backendAPI/
    ├── Dockerfile
    ├── requirements.txt
    ├── readme.md
    ├── backedAPI/
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── db.sqlite3
    ├── __init__.py
    ├── manage.py
    └── recomapiservice/
        ├── admin.py
        ├── apps.py
        ├── __init__.py
        ├── migrations/
        │   ├── 0001_initial.py
        │   └── __init__.py
        ├── models.py
        ├── serializers.py
        ├── tests.py
        ├── urls.py
        └── views/
            ├── __init__.py
            ├── recomviews.py
            ├── searchview.py
            ├── similardocview.py
            └── userinteractionsview.py
```
**Django API interface to handle API calls from frontend UI**


