FROM python:alpine

RUN apk add ffmpeg

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . app
WORKDIR /app

EXPOSE 80

# runs the production server
ENTRYPOINT ["python", "gargboyz/manage.py"]
CMD ["runserver", "0.0.0.0:80"]