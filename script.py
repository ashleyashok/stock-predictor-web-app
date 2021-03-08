import streamlit as st
import datetime
import yfinance as yf
from fbprophet import Prophet
from plotly import graph_objs as go
import requests

# get stock data
@st.cache
def getStockData(ticker, start, end):
    df = yf.download(ticker, start, end)
    df.reset_index(inplace=True)
    return df

today = datetime.date.today()
st.title('Stock Forecast App')

st.sidebar.write('Select Option')
typeDash = st.sidebar.selectbox('Type of Dashboard:',('Forecast', 'Correlation'))


if typeDash == 'Forecast':
    
    st.subheader('Forecast Dashboard')
    
    symbol = st.sidebar.text_input("Enter text here", 'AAPL', max_chars=5, type='default')

    start_dt = st.sidebar.date_input('Select start date:', max_value=today)
    end_dt = st.sidebar.date_input('Select end date:', max_value=today)
    
    if st.sidebar.button('Generate Forecast'):

        st.image(f"https://finviz.com/chart.ashx?t={symbol}")

        data = getStockData(symbol, start_dt, end_dt)
    
        st.dataframe(data.tail())


# st.text_area('Area for textual entry')


# selected_stocks = st.selectbox(['1', '2'])

# def load_data(ticker):
#     data = yf.download(ticker)
#     data.reset_index(inplace=True)
#     return data
# st.header('This is a header')
# st.subheader('Testing')
# st.write('this is normal text')

# a = st.sidebar.radio('R:',[1,2])


# '''
# This is a markdown sentence
# # Header using markdown

# '''

# st.sidebar.write('Normal text on the sidebar')
# st.image()