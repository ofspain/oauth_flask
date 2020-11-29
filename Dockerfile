# pull official base image for python
FROM python:3.8.1-slim-buster

# set working
ENV PWD /usr/src/app
WORKDIR ${PWD}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ${PWD}/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . ${PWD}/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
