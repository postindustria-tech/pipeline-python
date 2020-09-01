# 51Degrees V4 Pipeline - Python

## Requirements and installation

* Python 2.7 or Python 3
* [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/) (for running examples)

## Examples and Tests

Note: If you get errors like `no module named 'x'`, then execute `pip install x` and retry.

To run tests in each repository

```
python -m unittest discover -s tests -p test*.py
```

## Examples

The examples depend on the Pipeline modules, you can either use the remote 
versions as normal or local versions. If you want to use the local versions 
then use the `-e` option with `pip install`. For example:

```
pip install -e fiftyone_pipeline_core
```

### Linux

Execute `export FLASK_APP=` with the name of the web example file, then `flask run`.

### Windows

Execute `$env:FLASK_APP = "x"` with the name of the example file, then `flask run`.
