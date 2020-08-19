# The HTI module reference implementation (ri) in Python.

## Running with docker

```shell script
docker build . -t gids-hti-module-python:latest  && docker run gids-hti-module-python:latest
```

## Running locally

### Requirements

For building and running the application you need:

- Python 3.8

### Preparing

To setup the application, you'll need to create a virtual environemnt and install the dependencies

```shell script
python3.8 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Staring the application
```shell script
source ./venv/bin/activate
FLASK_APP=application python3 -m flask run
```

Now, navigate to [http://localhost:5000/](http://localhost:5000/), you should see a "403 - Forbidden" page. 

### Accessing the application

To access the application, you'll need to make a HTI launch to the application.
The [https://gids-hti-portal.edia-tst.eu/portal.html](https://gids-hti-portal.edia-tst.eu/portal.html)
application is configured by default to access this reference implementation. To do so, navigate to the 
[https://gids-hti-portal.edia-tst.eu/portal.html](https://gids-hti-portal.edia-tst.eu/portal.html) page and
fill in the following:

 * Activity identifier, set to either: *1*, *2*, *3*, or *4*
 * Audience (aud): depending on your installation, de default is: *localhost:5000*
 * Launch url: depending on your installation, de default is: *http://localhost:5000/module_launch*
 

### Running the tests
To prepare the test, run the following
```shell script
source ./venv/bin/activate
pip install -r requirements-test.txt
```
To run the test and coverage report:
```shell script
source ./venv/bin/activate
pytest --cov=application/ tests/
```

## Copyright

Released under the Mozilla Public License Version 2.0. See the [LICENSE](LICENSE) file.LICENSE
