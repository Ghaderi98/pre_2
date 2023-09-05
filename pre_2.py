# -*- coding: utf-8 -*-
"""pre_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GPGKYTT6Gr1Acd87N9mssx6fb1zi55c7
"""

import streamlit as st
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import requests


def get_stock_data(symbol):
    stock_data = yf.download(symbol)
    return stock_data


def train_lstm(data):
    # پیاده‌سازی مدل LSTM با لایه‌بندی
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(None, 1)))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # آموزش مدل با داده‌های آموزشی
    # ...

    return model


def predict_lstm(model, data):
    # تبدیل داده‌ها به آرایه numpy
    data = np.array(data)

    # تغییر شکل داده‌ها برای ورودی LSTM
    data = np.reshape(data, (data.shape[0], data.shape[1], 1))

    # پیش‌بینی با استفاده از مدل LSTM
    predictions = model.predict(data)

    return predictions


def calculate_profit(data, buy_date, buy_price):
    # پیدا کردن قیمت سهام در تاریخ خرید
    buy_price = data.loc[buy_date, 'Close']

    # پیدا کردن قیمت سهام در تاریخ فروش (به عنوان مثال، تاریخ امروز)
    sell_date = datetime.date.today().strftime("%Y-%m-%d")
    sell_price = data.loc[sell_date, 'Close']

    # محاسبه سود
    profit = (sell_price - buy_price) * 100 / buy_price

    return profit


def fetch_stock_info(symbol):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro&exsentences=3&titles={symbol}"
    response = requests.get(url).json()
    page_id = list(response['query']['pages'].keys())[0]
    info = response['query']['pages'][page_id]['extract']
    return info


def plot_prediction(data, prediction):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Actual')
    plt.plot(data.index, prediction, label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Prediction')
    plt.legend()
    st.pyplot(plt)


def main():
    st.title("Stock Trading App")

    symbol = st.text_input("Enter stock symbol (e.g., AAPL for Apple):")
    if not symbol:
        st.warning("Please enter a stock symbol.")
        return

    if st.button("Get Data"):
        st.write("Fetching stock data...")
        stock_data = get_stock_data(symbol)

        if len(stock_data) == 0:
            st.error("No data available for the symbol. Please enter a valid symbol.")
            return

        st.write("Stock Data:")
        st.write(stock_data)

        # آموزش مدل LSTM
        model = train_lstm(stock_data)

        # پیش‌بینی با استفاده از مدل LSTM
        prediction = predict_lstm(model, stock_data)

        st.write("Prediction:")
        st.write(prediction)

        # دریافت اطلاعات سهام از ویکی‌پدیا
        stock_info = fetch_stock_info(symbol)
        st.write("Stock Info:")
        st.write(stock_info)

        # پیش‌بینی روند بازار برای 10 روز بعد
        future_dates = pd.date_range(start=stock_data.index[-1], periods=10, closed='right')
        future_data = pd.DataFrame(index=future_dates, columns=stock_data.columns)

        # تکمیل داده‌های آینده با استفاده از مدر ادامه، کد برای تکمیل بخش پیش‌بینی روند بازار برای 10 روز بعد و تکمیل داده‌های آینده با استفاده از مدل LSTM را می‌آورم:



        # تکمیل داده‌های آینده با استفاده از مدل LSTM
        last_data = np.array(stock_data['Close'][-100:])  # 100 روز گذشته
        for i in range(len(future_data)):
            next_day_prediction = predict_lstm(model, last_data.reshape(1, -1, 1))
            future_data.iloc[i] = next_day_prediction
            last_data = np.append(last_data[1:], next_day_prediction)

        st.write("Future Prediction:")
        st.write(future_data)