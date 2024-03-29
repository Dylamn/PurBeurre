FROM debian:stable-slim

MAINTAINER Dylan Vallée "dylan.vallee@hotmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev default-libmysqlclient-dev

# We copy just the requirements/api.txt & common.txt first to leverage Docker cache
COPY ./requirements/common_requirements.txt /app/common_requirements.txt
COPY ./requirements/api_requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "manage.py", "run", "--host", "0.0.0.0", "--port", "5000" ]
