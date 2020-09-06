# 51Degrees V4 Pipeline - Python

## Requirements and installation

* Python 2.7 or Python 3

## To install from git repository

* Install `pipenv` https://pypi.org/project/pipenv/
* Run `pipenv install` in the root of the folder
* Launch the environment shell by running `pipenv shell`

## Running tests and examples

To run tests in each repository.

* Go to each directory (for example `fiftyone_pipeline_core`)
* Run `python -m unittest discover -s tests -p test*.py`

To run the web examples:

### Linux

Execute `export FLASK_APP=` with the name of the web example file, then `flask run`.

### Windows

Execute `$env:FLASK_APP = "x"` with the name of the example file, then `flask run`.
