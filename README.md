# gargboyz

A django project to display gargboyz memorabilia. 

## Usage

```bash
# For prod
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput --clear
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --noinput
```

## Development

```bash
# For dev
docker-compose up -d --build
docker-compose exec web python manage.py flush --noinput
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py createsuperuser --noinput
# For cleaning up
docker-compose down -v
docker system prune --all --force --volumes
docker volume  prune --all --force
```

```bash
# For test
docker-compose -f docker-compose.test.yml up -d --build
docker-compose -f docker-compose.test.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.test.yml exec web python manage.py collectstatic --noinput --clear
docker-compose -f docker-compose.test.yml exec web python manage.py createsuperuser --noinput
# For cleaning up
docker-compose -f docker-compose.test.yml down -v
docker system prune --all --force --volumes
docker volume  prune --all --force
```

## Meme app

An app that displays and allows uploads of memes.

### Tables

#### meme

| **column name**            | **type**             | **description**                              |
| -------------------------- | -------------------- | -------------------------------------------- |
| number                     | PositiveSmallInteger | actual number of the meme                    |
| declared_number            | PositiveBigInteger   | the declared number of the meme              |
| media_path                 | FilePath             | local file directory link to media           |
| media_type                 | string               | image, gif or video                          |
| media_created_at           | Date                 |                                              |
| voice_recording_path       | FilePath             | local file directory link to recording       |
| voice_recording_created_at | DateTime             | unix timecode                                |
| voice_recording_transcript | Text                 | transcription of voice recording             |
| authors                    | list of foreign keys | comma seperated list of authors              |
| season                     | PositiveSmallInteger | meme season 1,2,3 e.t.c                      |
| subseason                  | string               | irish rick and morty, daniels tooltips e.t.c |


## Credits

Big thank you to testdrivenio for writing [this guide](https://github.com/testdrivenio/django-on-docker)!