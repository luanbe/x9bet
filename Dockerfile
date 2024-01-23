# pull official base image
FROM python:3.11

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run cron
RUN apt-get update && apt-get -y install cron
COPY crawler-cron /etc/cron.d/crawler-cron
RUN chmod 0644 /etc/cron.d/crawler-cron
RUN crontab /etc/cron.d/crawler-cron
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log