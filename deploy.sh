#!/bin/bash

gunicorn -w 4 -b localhost:8000 mysite:app 
