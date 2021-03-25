Task-Manager
============

_Multi-user project/task tracker written with Django_

![](./example.png)

## Start development environment in Docker container

```
docker-compose up -d --build
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py fill_db
docker-compose exec web python manage.py createsuperuser
```

## Start production environment on Heroku in Docker container

Dockerfile is suitable for running a production environment on Heroku using a docker container.
[Link](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true) to manual for getting started
on Heroku.

Don't forget to configure your production environment settings

```
$ heroku config:set DEBUG=0
$ heroku config:set SECRET_KEY=...   # set your own secret_key
$ heroku config:set ALLOWED_HOSTS=.herokuapp.com
$ heroku config:set DATABASE_URL=postgres://...   # get from HEROKU_POSTGRESQL_COBALT_URL

$ heroku config:set SECURE_SSL_REDIRECT=True
$ heroku config:set CSRF_COOKIE_SECURE=True                                                                                                                                                               
$ heroku config:set SECURE_HSTS_PRELOAD=True                                                                                                                                                              
$ heroku config:set SECURE_HSTS_SECONDS=518400
$ heroku config:set SECURE_HSTS_INCLUDE_SUBDOMAINS=True
$ heroku config:set SESSION_COOKIE_SECURE=True
```

Run a shell from a container

```
$ heroku run /bin/sh
```

__Try testing the Task-Manager on
Heroku: [https://pacific-fjord-50202.herokuapp.com](https://pacific-fjord-50202.herokuapp.com/)__

---
*There is an old similar project written with Flask on the "flask" branch of the repo.*