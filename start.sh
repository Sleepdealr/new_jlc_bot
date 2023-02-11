#!/bin/bash

# Pulls from git
# Sometimes it doesn't feel like pulling so you need to stash and reset it
# There is probably a better way of doing this
# Comment out to disable
git fetch
git stash
git stash drop
git pull

source venv/bin/activate

pip install -r requirements.txt

python3 app.py
