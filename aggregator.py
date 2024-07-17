import duckdb
import pandas as pd
import time
from memory_profiler import profile
import os

def init():
    db = duckdb.connect('sensordb.duckdb')
    db.sql('SET threads TO 1')
    db.sql("SET memory_limit = '125MB'")
    return db

@profile
def aggregate(db, by='date'):

    if by == 'date':
        df = db.sql("""SELECT
                    timestamp::DATE as date,
                    SUM(temp) as temprature 
                    FROM read_parquet('sensor_readings/**/*.parquet', hive_partitioning = true)
                    GROUP BY 1 
                    ORDER BY 1 DESC""").fetchdf()

    if by == 'hour':
        df = db.sql("""
        SELECT
        timestamp::DATE as date,
        date_part('hour', timestamp) as hour,
        SUM(temp) as temprature
        FROM read_parquet('sensor_readings/**/*.parquet', hive_partitioning = true)
        GROUP BY 1,2
        ORDER BY 1,2
        """).fetchdf()

    return df


if __name__ == '__main__':
    
    print(os.getcwd())
    print(os.listdir())
    db = init()
    
    df = aggregate(db, 'hour')
    print(df)
