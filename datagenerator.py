import pandas as pd
import os
import json
import duckdb
import random
import time
from datetime import datetime, timedelta
from memory_profiler import profile

def generateDate(start, end):

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    
    days = (end - start).days

    date = start + timedelta(days=random.randint(0,days))
    return date

def generateTimeSeries():
    d = pd.date_range(start='2023/01/01', end='2023/12/31', freq='s')
    return d


def generateSamples():
    data = [{
        'timestamp': str(i),
        'sensorID': '1',
        'temp': random.randint(0,1000)
    } for i in generateTimeSeries().tolist()]

    return data


def init():
    db = duckdb.connect('sensordb.duckdb')
    db.execute('CREATE OR REPLACE TABLE FACT_SENSOR (timestamp TIMESTAMP, sensorID STRING, temp INTEGER)')
    return db

def append(db, df):
    db.register('sample_df', df)
    db.sql('INSERT INTO FACT_SENSOR SELECT * FROM sample_df')
    
if __name__ == '__main__':
    db = init()

    # for i in range(0,100000):
    #print('Running Batch : ', 1)
    samples = generateSamples()
    df = pd.DataFrame(samples)
    append(db, df)

    db.sql("""
    COPY (SELECT timestamp::DATE date, timestamp, temp FROM FACT_SENSOR) 
    TO 
    sensor_readings 
    (FORMAT PARQUET, PARTITION_BY (date),  OVERWRITE_OR_IGNORE)
    """)
        
