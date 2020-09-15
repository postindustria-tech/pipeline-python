![51Degrees](https://51degrees.com/DesktopModules/FiftyOne/Distributor/Logo.ashx?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Data rewards the curious") **Python Pipeline Core**

## Introduction

The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines) 

## This package fiftyone_pipeline_core

This package definds the essential components of the Pipeline API such as `flow elements`, `flow data` and `evidence`. It also packages together JavaScript served by a pipeline and allows for client side requests for additional data populated by evidence from the client side.

It can be used on its own or with the following additional packages.

- **fiftyone_pipeline_engines** - Adds a specialized type of flow element called an engine which allows for additional features including an auto-updating data file for properties, a service called when a requested property is missing and a caching system.

Engines created by 51Degrees including:

- **fiftyone_devicedetection** - A device detection engine
- **fiftyone_location** - A geolocation lookup engine

Make use of the above along with the following additional packages:

- **fiftyone_pipeline_cloudrequestengine** - An engine used to make requests to the 51Degrees cloud service.

## Requirements and installation

* Python 2.7 or Python 3
* The `flask` python library to run the web examples 

## Running tests and examples

To run tests:

* Run `python -m unittest discover -s tests -p test*.py`

To run the web examples:

### Linux

Execute `export FLASK_APP=` with the name of the web example file, then `flask run`.

### Windows

Execute `$env:FLASK_APP = "x"` with the name of the example file, then `flask run`.
