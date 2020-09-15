![51Degrees](https://51degrees.com/DesktopModules/FiftyOne/Distributor/Logo.ashx?utm_source=github&utm_medium=repository&utm_content=readme_main&utm_campaign=python-open-source "Data rewards the curious") **Python Pipeline Engines**

## Introduction

The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines) 

## This package fiftyone_pipeline_engines

This package extends the `flow element` class created by the `fiftyone.pipeline.core` pacakge into a specialized type of flow element called an engine. This allows for additional features including:

* An auto-updating data file for properties
* A service called when a requested property
* A caching system and implementation of an LRU (least recently used) cache

Engines created by 51Degrees:

- **fiftyone_devicedetection** - A device detection engine
- **fiftyone_location** - A geolocation lookup engine

Make use of this package along with the following additional packages:

- **fiftyone_pipeline_cloudrequestengine** - An engine used to make requests to the 51Degrees cloud service.

## Requirements and installation

* Python 2.7 or Python 3
* The `flask` python library to run the web examples 

## Running tests

* Run `python -m unittest discover -s tests -p test*.py`

