#!/bin/bash
set -e
# pip install flask_api
# pip install flask_cors
exec python3 update_scores.py 'true' &
exec python3 sent_embedding.py &
exec python3 webserver.py 