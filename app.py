import streamlit as st
import pandas as pd
from aggregator import aggregate, init
from memory_profiler import profile

db = init()

def getData(hourly=False, aggregateBy = 'date'):
    result = aggregate(db, aggregateBy)
    return result

@profile
def start_app():

    st.title('Sensor Monitor')

    option = st.selectbox('Select the aggregate type : ', options=['hourly','daily'], )

    if option == 'daily':
        df = getData(hourly=False, aggregateBy='date')
        df['date'] = df['date'].astype(str)
        st.write(df)
    
    if option == 'hourly':
        df = getData(hourly=True, aggregateBy='hour')
        df['date'] = df['date'].astype(str)
        st.write(df)


if __name__ == '__main__':

    start_app()
