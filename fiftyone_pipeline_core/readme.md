# 51Degrees V4 Pipeline Core - Python

## Requirements and installation

* Python 2.7 or Python 3
* The `flask` python library to run the web examples 

## Running tests and examples

To run tests in each repository

`python -m unittest discover -s tests -p test*.py`

To run the web examples:

### Linux

Execute `export FLASK_APP=` with the name of the web example file, then `flask run`.

### Windows

Execute `$env:FLASK_APP = "x"` with the name of the example file, then `flask run`.