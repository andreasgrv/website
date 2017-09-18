#!/bin/bash

cd "$(dirname "$0")"
source .env/bin/activate
gunicorn -w 1 -b 0.0.0.0:8000 mysite:app 
