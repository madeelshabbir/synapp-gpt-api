# Use the official Python image from Docker Hub
FROM python:3.9.15

WORKDIR '/var/www/synappgpt-api'

# Update the package list and then install libpq-dev and SQLite3
RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
RUN chmod 755 ./entrypoints/app.sh
EXPOSE 3001
ENTRYPOINT ["sh", "./entrypoints/app.sh"]
