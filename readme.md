# 51Degrees Pipeline API

![51Degrees](https://51degrees.com/DesktopModules/FiftyOne/Distributor/Logo.ashx?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Data rewards the curious") **Python Pipeline**

[Developer Documentation](https://51degrees.com/pipeline-python/index.html?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Developer Documentation")

## Introduction
This repository contains the components of the Python implementation of the 51Degrees Pipeline API.

The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines) 

## Contents
This repository contains 3 modules:

- **fiftyone_pipeline_core** - Defines the essential components of the Pipeline API such as 'flow elements', 'flow data' and 'evidence'
- **fiftyone_pipeline_engines** - Functionality for a specialized type of flow element called an engine.
- **fiftyone_pipeline_cloudrequestengine** - An engine used to make requests to the 51Degrees cloud service.

## Requirements

* Python 3.5+ 
* The `flask` python library to run the web examples 

## Installation

### From PyPI

Generally, you will want to be installing one of the engines such as [device detection](https://pypi.org/project/fiftyone-devicedetection/) or [location](https://pypi.org/project/fiftyone-location/). However, if you do want to install the core modules directly (for example, to work on your own engine) then just use `pip install` with the relevant module name: 

`pip install fiftyone_pipeline_core`
`pip install fiftyone_pipeline_engines`
`pip install fiftyone_pipeline_cloundrequestengine`

### From GitHub

* Clone repository
* Install `pipenv` https://pypi.org/project/pipenv/
* Run `pipenv install` in the root of the folder
* Launch the environment shell by running `pipenv shell`

## Running tests and examples

If you've cloned the repository from GitHub, you can run the tests 
and examples that are available. To run tests:

* Go to each directory (for example `fiftyone_pipeline_core`)
* Run `python -m unittest discover -s tests -p test*.py`

To run the web examples navigate into Examples folder:

#### Linux

Execute `export FLASK_APP=web` where `web` is the example file, and start your application via `flask run`.

#### Windows

Execute `$env:FLASK_APP = "web"` where `web` is the example file, and start your application via `flask run`.
