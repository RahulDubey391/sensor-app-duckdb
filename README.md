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

The dataset is partitioned at date level and follows the Hive Partitioning strategy. Also the phyical storage of data is in Apache Parquet format since DuckDB exploits the metadata at file level to reduce seek time for the qureries using Row Group/Column Chunk level statistics.

## Experiment
The experiment is intended to check the following metrics for the ad-hocs query processing over the data:
* In-process Memory footprint (MB)
* Query Processing Time/Latency (in Milliseconds)

Only the aggregation part of the program is tested to check the above metrics. Since Streamlit UI adds overhead for rendering components, we are leaving out the UI runtime.

### Environment Setup
#### VM Instance Setup
For our experiment and as of any real-world application, we are deploying/testing the application in the Cloud Environment. Since this code is not tested on real IOT device, we'll constrain the VM Instance to lower-end of specification. 

For our case, the low-tier VM instance is chosen from the Google Compute Engine service with following specification:
* Memory - 1 GB
* vCPU/Core - 1/1
* Disk Space - 10 GB

The Disk Space is kept high since the HDDs/SSDs are cheaper than memory and usually on the higher range for IOT devices. The intention is to utilize the Disk Space as much as possible to utilize filesystem's capabilities.

#### Docker Setup
Application is tested in the docker environment to isolate other OS processes and to facilitate the full utilization of the resources assigned. Although Docker itself incurs some runtime memory overhead, but we'll ignore it's resource utilization. The Applicaiton is containerized and deployed using the Dockerfile provided with the code base. Since the Google Compute Engine service requires custom mapping for external exposure of IP addresses, we are just utilizing the local access to test the runtime footprint.

Specification for Docker Container:
* Lightweight with fraction of 1 GB Memory and 1 vCPU
* Mounted Volume with the data to be processed
* Port 4000:80

#### Tasks & Queries
Since the data exists at Seconds level, there are two types of queries used to measure the metrics. 
* Aggregation at Date Level (Daily Temprature) - Temprature aggregate query at Date Level
* Aggregation at Hourly Level (Hourly Temprature for each day) - Temprature aggregate query at Hourly level for each single day

The partitioned nature of data is utilized to exploit the processing of data. Although the number of threads for DuckDB is set to 1 since we only want to utilize as much less resource as possible, but still the partitioned and physical nature of the files stored in filesystem provides sufficient advantages.

##### Query 1 - Daily Aggregate
```
SELECT
  timestamp::DATE as date,
  SUM(temp) as temprature 
FROM read_parquet('sensor_readings/**/*.parquet', hive_partitioning = true)
GROUP BY 1 
ORDER BY 1 DESC
```

##### Query 2 - Hourly Aggregate
```
SELECT
  timestamp::DATE as date,
  date_part('hour', timestamp) as hour,
SUM(temp) as temprature
FROM read_parquet('sensor_readings/**/*.parquet', hive_partitioning = true)
GROUP BY 1,2
ORDER BY 1,2
```

## Conclusion
The memory footprint for the DuckDB during in-process remains in range of (100 - 150 MB) of memory and the queries takes about (900ms - 2s) of runtime.

DuckDB provides much better capabilities to run lightweight analytical applications where the resources are more constrained. Also since the local filesystem of the VM instance is used, the network transfer are almost nil which adds up performance for the application. 

Besides the OLAP capabilities, the Application still might need an external database for User/Session management which will add overhead for the application, but at least the data for aggregation can reside in the same device where the application is hosted.
