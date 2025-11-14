import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use("Agg")     # Prevent ScriptRunContext errors
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Predictor", layout="centered")
st.title("📈 Simple Stock Market Predictor (Beginner Friendly)")

st.write("Enter a stock symbol to view charts, moving averages, and simple prediction!")

# Input
ticker = st.text_input("Enter Stock Symbol (Example: AAPL, TSLA, TCS.NS)", "AAPL")

if st.button("Fetch Data"):
    st.write(f"Fetching data for **{ticker}**...")

    # Download last 6 months
    data = yf.download(ticker, period="6mo", progress=False)

    if data.empty:
        st.error("❌ Invalid stock symbol or no data available.")
    else:
        st.success("✅ Data loaded successfully!")

        # Moving Averages
        data["MA_5"] = data["Close"].rolling(5).mean()
        data["MA_10"] = data["Close"].rolling(10).mean()
        data["MA_20"] = data["Close"].rolling(20).mean()

        st.subheader("📊 Last 5 Days of Data")
        st.write(data.tail())

        # Chart
        st.subheader("📉 Price Chart With Moving Averages")
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(data["Close"], label="Close Price")
        ax.plot(data["MA_5"], label="MA 5 Days")
        ax.plot(data["MA_10"], label="MA 10 Days")
        ax.plot(data["MA_20"], label="MA 20 Days")

        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

        # Simple Prediction (beginner level)
        predicted_price = float(data["MA_5"].iloc[-1])
        last_close = float(data["Close"].iloc[-1])

        st.subheader("🔮 Predicted Next Day Price (Simple Method)")
        st.info(f"**Predicted Price:** ₹ {round(predicted_price, 2)}")

        # Prediction UP / DOWN
        if predicted_price > last_close:
            st.success("📈 Prediction: The stock may go UP next day")
        else:
            st.error("📉 Prediction: The stock may go DOWN next day")

        # Download Data
        st.download_button(
            "⬇️ Download Full Data (CSV)",
            data.to_csv().encode("utf-8"),
            file_name=f"{ticker}_data.csv",
            mime="text/csv"
        )
