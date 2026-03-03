#!/bin/bash
# Start the internal REST API in the background on port 5001
gunicorn src.api:app --bind 0.0.0.0:5001 --daemon

# Start the Web UI in the foreground on the Heroku provided $PORT
gunicorn src.app:app --bind 0.0.0.0:$PORT
