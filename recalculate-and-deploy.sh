#!/bin/bash

# Scrape new data, add it to DB, rebuild app, and deploy.

# Log time first.
date
date >&2

# Exit if any command errors.
set -e

# cd to directory containing this file.
cd $(dirname "$0")

git checkout main
git pull

# Pull latest submodules. This is mainly important for picking up new members in congress-legislators.
git submodule foreach git pull origin main

# Scrape all vote data from the last 3 days.
cd submodules/congress
source venv/bin/activate
usc-run votes --fast --force --log=info
cd ../..

docker system prune -f
docker compose stop
docker compose build
docker compose run --rm --remove-orphans back-end python manage.py migrate
docker compose run --rm --remove-orphans back-end python manage.py recalculate-all
echo 'finished loading data'
docker compose up -d --remove-orphans back-end
echo 'finished backend'
docker compose run --rm --remove-orphans front-end /bin/bash -c 'npm run build && npm run deploy'
docker compose stop
docker compose rm -f
docker system prune -f
