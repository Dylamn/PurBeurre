# Pur Beurre
This application uses the OpenFoodFacts public API.

## Overview
The goal of this project is to help customers who wants to change their diet but
were unsure where to start.
Replace the Nutella with a hazelnut paste, yes, but which one? In which shop to buy it? 

The idea of this application is to provide a handy tool for customers 
to search, compare foodstuffs or even suggest (healthier) substituts for any.

## Features
The main purpose of the application is to provide you a research tool for 
food products.

The application includes user accounts which, are not required in order to use
the application. It just adds an extra feature that's you can register products,
so you can retrieve them easily without worrying about the name of each one.

## Installation
The project has two parts, an API (Application Programming Interface), and a CLI (Command Line Interface).
Below are instructions that will help you to install them.

The project ships with some docker related files that allow you to simply set up the API of 
the project with docker. So you have the choice of the way you install the project.
Below, there're the procedures for an installation through docker or manually.

Before diving into a procedure, there is one action that is necessary for both
which is the following:

When you have cloned the projet, 
you must copy/rename the `.env.example` file and name it `.env`. 
You can then fill the variables inside to fit your requirements.

> You have to fill the `JWT_SECRET_KEY` with a long, random string.

### Docker
Make sure you have docker and docker-compose installed.
You can run the following command to ensure that:
````shell
$ docker -v && docker-compose -v 
````
If there're not installed, you can consult the official documentation 
[here](https://docs.docker.com/get-docker/).

move to the root of the project and run the following command:
```shell
$ docker build -t purbeurre-api .
```
> This will create the docker image of the API. This image is currently not
> published on the docker hub.

When the image build is finished, you can build the services 
in the `docker-compose.yml` file by running the command below:
````shell
$ docker-compose up -d
````
> the `-d` option means that the containers will run in the background.

Then, when both services have started, you can use the following command to see if there're up:
````shell
$ docker ps -f name=purbeurre
````

Finally, you can install the dependencies used by the client.

To do that, you must install them via pip. I recommend using a virtual environment, 
you can either use the [venv](https://docs.python.org/3.8/library/venv.html)
which comes out of the box with python since the 3.3 version, 
[virtualenv](https://virtualenv.pypa.io/en/latest/) or any tool you want.

With `venv`, you can do like so:
````shell
$ python3 -m venv my_venv && source my_venv/bin/activate
````
> You can replace `my_venv` by the name of your choice.

Now, you can install the CLI dependencies by running the following command:
````shell
$ pip install -r requirements/cli_requirements.txt
````
> If you have an error when installing the `selectmenu` 
> check the Troubleshooting section at the end of the file.

### Manual
The API requires some packages (especially Flask) in order to run. 
To do that, you must install them via pip. I recommend using a virtual environment, 
you can either use the [venv](https://docs.python.org/3.8/library/venv.html)
which comes out of the box with python since the 3.3 version, 
[virtualenv](https://virtualenv.pypa.io/en/latest/) or any tool you want.

For example with the venv, you can create and activate a virtual environment 
with the following commands:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

> The second "venv" word is the name of the folder which will contains your 
virtual environment so, you can write anything you want.

After you've done that, use the following command to install the dependencies 
listed in the `requirements.txt` file:

```shell
$ pip install -r requirements.txt
```

## Run the application
When the packages are installed, you'll need to launch the API used by the client.
If you installed the API manually, run it with the python interpreter throught the manager:
```shell
# This command will start the API.
$ python manage.py run
```

If you installed it with docker, check that the containers are running with the following command:
`````shell
$ docker ps -f name=purbeurre
`````
If nothing is printed, you can restart them by running the ``docker-compose up`` command.

> You'll always need to start the API in order to use the CLI properly. If the CLI can't
> communicate with the API, an error will be printed, and the client will stop running.

When it's done, you can start the CLI by passing it to the Python interpreter:
```shell
$ python cli.py
```

## Troubleshooting
When installing python dependencies, sometimes a problem can occurred for the 
`SelectMenu` package where it said that prompt-toolkit isn't installed. To resolve
this issue, you have to install to run the following command before the packages listed
in the the `requirements.txt` (`requirements/cli_requirements.txt` if you have installed the API with docker):
````shell
$ pip install prompt-toolkit==1.0.15
````
