# gargboyz

A django project to display gargboyz memorabilia. 

## Apps
### memes

An app that displays and allows uploads of memes.

## Usage

```bash
# For prod
docker compose -f compose.prod.yml pull
docker compose -f compose.prod.yml up -d
docker compose -f compose.prod.yml exec web python manage.py collectstatic --noinput --clear
docker compose -f compose.prod.yml exec web python manage.py migrate --noinput
# For first time
docker compose -f compose.prod.yml exec web python manage.py createsuperuser --noinput
```

### Development

```bash
# Local development
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver
# For cleaning up
rm -rf mediafiles db.sqlite3
```

```bash
# For dev. Testing db changes e.t.c
docker compose up -d --build
docker compose exec web python manage.py flush --noinput
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py createsuperuser --noinput
# For cleaning up
docker compose down -v
docker system prune --all --force --volumes
docker volume  prune --all --force
```

```bash
# For test. Testing gunicorn, nginx, logging, static files e.t.c
docker compose -f compose.test.yml up -d --build
docker compose -f compose.test.yml exec web python manage.py migrate --noinput
docker compose -f compose.test.yml exec web python manage.py collectstatic --noinput --clear
docker compose -f compose.test.yml exec web python manage.py createsuperuser --noinput
# For cleaning up
docker compose -f compose.test.yml down -v
docker system prune --all --force --volumes
docker volume  prune --all --force
```

## Credits

Big thank you to testdrivenio for writing [this guide](https://github.com/testdrivenio/django-on-docker)!