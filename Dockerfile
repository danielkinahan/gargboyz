FROM python:3

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=gargboyz.settings

RUN apt update && apt install -y ffmpeg

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . app
WORKDIR /app

RUN python manage.py collectstatic --no-input

# EXPOSE 80

# # runs the production server
# ENTRYPOINT ["python", "manage.py"]
# CMD ["runserver", "0.0.0.0:80"]

CMD ["gunicorn", "gargboyz.wsgi:application", "--bind", "0.0.0.0:80"]