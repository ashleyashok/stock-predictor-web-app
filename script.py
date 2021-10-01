import streamlit as st
import datetime
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from pandas_datareader import data as pdr

import requests

# get stock data
@st.cache
def getStockData(ticker, start, end):
    # df = yf.download(ticker, start, end)
    df = pdr.get_data_yahoo(ticker, start, end)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df


def plot_stock(data,symbol):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name=symbol)])

    fig.update_xaxes(type='category')
    fig.update_layout(autosize=True, rangemode='tozero')
    fig.update_layout(autosize=True)
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)
    return

def prophetForecast(data, period=30):

    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.add_seasonality('self_define_cycle',period=252,fourier_order=8,mode='additive')
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period,freq='D')
    forecast = m.predict(future)

    return forecast, m

today = datetime.date.today()

st.sidebar.text('Select Option')
typeDash = st.sidebar.selectbox('Type of Dashboard:',('Forecast', 'Correlation'))


if typeDash == 'Forecast':
    st.title('Stock Forecast Dashboard')

    symbol = st.sidebar.text_input("Enter Stock Ticker here", 'AAPL', max_chars=5, type='default')
    start_dt = st.sidebar.date_input('Select start date:', value = today - datetime.timedelta(days=365), max_value= today -datetime.timedelta(days=365))
    end_dt = st.sidebar.date_input('Select end date:',max_value=today)
    forecast_period = st.sidebar.text_input('Enter number of days to forecast:', value=30, max_chars=3)

    if st.sidebar.button('Generate Forecast'):
        st.subheader(f'Stock chart: {symbol}')
        st.image(f"https://finviz.com/chart.ashx?t={symbol}")

        data = getStockData(symbol, start_dt, end_dt)

        forecast, m = prophetForecast(data, period=int(forecast_period))

        st.subheader(f'FB Prohet forecasting chart: {symbol} for {forecast_period} days')
        fig1 = plot_plotly(m, forecast)
        fig1.update_yaxes(title_text='Share Price ($)',rangemode="tozero")

        st.plotly_chart(fig1)

if typeDash =='Correlation':

    st.write('Stay tuned! Future Ash will work on it')