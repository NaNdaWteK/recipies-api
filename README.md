# recipies-api

## Build docker image

`$ docker build .`

## Build docker-compose image

`$ docker-compose build`

## Create Django project

`$ docker-compose run --rm app sh -c "django-admin startproject app ."`

## Linting

### Use flake8 package

- Run it throught docker-compose

`$ docker-compose run --rm app sh -c "flake8"`

## Testing

- Run it with docker-compose

`$ docker-compose run --rm app sh -c "python manage.py test"`

## Start app

`$ docker-compose up`

## Migrations

## Make

`$ docker-compose run --rm app sh -c "python manage.py makemigrations"`

### Apply

`$ docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"`

**Delete volume if errors 'used before'**