FROM python:3.8-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean


ADD ./project/requirements.txt \
    ./project/dev.requirements.txt \
     /project/

RUN pip install --upgrade pip \
    && pip install \
    --no-cache-dir -Ur /project/requirements.txt \
    --no-cache-dir -Ur /project/dev.requirements.txt

COPY ./project /project


WORKDIR /project
CMD ["/project/start.sh"]