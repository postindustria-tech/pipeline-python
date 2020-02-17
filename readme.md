# 51Degrees V4 Pipeline - Python

## Requirements and installation

* Python 2.7 or Python 3
* `pip install -r requirements.txt` (requirements are only the web stuff, requests and flask)

## Running tests and examples

All tests are currently in the root level tests folder (in various subfolders) to run:

To run all tests:

`python -m unittest discover -s tests -p test*.py`

Individual tests

* `python -m unittest tests.core.test_core`
* `python -m unittest tests.engines.test_engines`
* `python -m unittest tests.javascriptbundler.test_javascriptbundler`
* `python -m unittest tests.devicedetection.test_devicedetection_cloud`

At the moment the example in examples/core needs to be moved into a root level folder to work. And run with `export FLASK_APP=custom_flowelement.py` and `flask run`.