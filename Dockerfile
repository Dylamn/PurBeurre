FROM debian:stable-slim

MAINTAINER Dylan Vallée "dylan.vallee@hotmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev default-libmysqlclient-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install prompt-toolkit==1.0.15 && \
    pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "manage.py", "run" ]
