#!/bin/bash

source .env/bin/activate
gunicorn -w 2 -b 0.0.0.0:8000 mysite:app 
