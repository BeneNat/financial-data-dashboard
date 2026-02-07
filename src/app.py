import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Investment Dashboard", layout="wide")

st.title("Simple Stock Market Dashboard")
st.write("Enter the symbol of the company or cryptocurrency to view the chart.")

ticker_symbol = st.sidebar.text_input("Symbol (np. AAPL, BTC-USD, TSLA):", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if ticker_symbol:
    try:
        df = yf.download(ticker_symbol, start=start_date, end=end_date)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty:
            st.error(f"No data found for symbol: {ticker_symbol}")
        else:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])

            fig.update_layout(
                title=f"Price chart for {ticker_symbol}",
                yaxis_title="Price (USD)",
                xaxis_rangeslider_visible=False,
            )

            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Show raw data"):
                st.dataframe(df)

    except Exception as e:
        st.error(f"An error has occurred: {e}")


