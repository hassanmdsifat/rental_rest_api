# Rental Application Backend

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/hassanmdsifat/rental_rest_api.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies:
```sh
(venv)$ cd rental_application
(venv)$ python manage.py runserver 0.0.0.0:8060
```
And navigate to `http://127.0.0.1:8060/api/product/`.

## Setup
As I have used sqlite database, for setting up initial data, please run:
```sh
(venv)$ python manage.py loaddata domain/meta/product_fixtures.json 
```

Please add local_settings.py file inside, rental_application->config directory
It needs to include
```python
SECRET_KEY = 'TEST'
DEBUG = True
```

## Test
For unittest, please run
```sh
(venv)$ python manage.py test
```
