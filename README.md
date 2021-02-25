# Pur Beurre
This application uses the OpenFoodFacts public API.

## Overview
The goal of this project is to help customers who wants to change their diet but
were unsure where to start.
Replace the Nutella with a hazelnut paste, yes, but which one? In which shop to buy it? 

The idea of this application is to provide a handy tool for customers 
to search, compare foodstuffs or even suggest (healthier) substituts for any.

## Installation
This application requires some packages (especially Flask) in order to run. 
To do that, you must them via pip. I recommend using avirtual environment, 
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
$ python3 -m pip install -r requirements.txt
```

## Run the application
When the packages are installed, you'll need to launch the API used by the client.
To run the API, execute it with the python interpreter throught the manager:

```shell
# This command will start the API.
$ python3 manage.py run
```

> You'll always need to start the API in order to use the CLI properly.

When it's done, you can start the CLI by passing it to the Python interpreter:
```shell
$ python3 cli.py
```

## Features
The main purpose of the application is to provide you a research tool for 
food products.

The application includes user accounts which, are not required in order to use
the application. It just adds an extra feature that's you can register products,
so you can retrieve them easily without worrying about the name of each one.

