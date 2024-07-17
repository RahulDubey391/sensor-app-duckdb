# sensor-app-duckdb
Naive demonstration on using DuckDB as a data processing engine for Sensor Device applications with low-end resources

## About
This is a simple app that demonstrates how DuckDB can be utilized to do data processing in-process of application. The application tends to be lightweight and not supposed to exceed the resource quota on the hosting platform.

## How it works?
The application is written in Python and contains the code snippet for the following components:
* app.py - Contains the UI application code using Streamlit framework. It's just a SPA with nothing but selection for aggregation levels.
* aggregator.py - Aggregations are performed on the timeseries data. Contains instance decalartion for DuckDB database for filesystem. Instance is just used to query the physical data in filesystem and doesn't intent to load/dump anything to the database.
* datagenerator.py - Script to generate mock up data for Sensor device. It only contains logic for temprature readings only, but it can be modified include other stuff.
* requirements.txt - Necessary dependencies for Python environment setup
* Dockerfile - Script to create Docker image for the final build

## Data in question
The data is merely a mockup for Sensor Device generation data for each second. This interval can be change to generate at Millisecond, Nanosecond, Minute, Hours etc in the data generator script. Although DuckDB has another way to write/read in separate threads to al least simulate the streaming of data. But the intention of the above app is to just check how much time it takes to run quries against data stored in filesystem.

The primary intention is to check the feasibility of DuckDB for Industrial IOT where the end-users are the operators of the application deployed at the edge. Refer to Experiment section to get more on the applicability of DuckDB as an alternative to custom written aggregator service.

## Experiment
The 
