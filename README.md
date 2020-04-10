## Dependencies
 - Docker

## Setup

Clone repository

`git clone git@github.com:Blobixx/metron_test.git`

Build and start server

`docker-compose up -d`
 
 Migrate database
 
 `docker-compose run web python manage.py migrate`
 
Access website

 Go to `localhost:8000/api/metron_test`
 
 ## Run tests

`docker-compose run web python manage.py test`