import pandas as pd
import numpy as np
import joblib

from tensorflow.keras.models import load_model


FEATURES = [
    "Prev Close",
    "Open",
    "High",
    "Low",
    "Close",
    "VWAP",
    "Volume",
    "Turnover",
    "Daily_Return",
    "Volatility",
    "Momentum_5",
    "MA20_Ratio",
    "MA50_Ratio",
    "MA252_Ratio"
]


CATEGORY_MAP = {

    "All Companies": [
        "ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJ-AUTO",
        "BAJAJFINSV","BAJFINANCE","BHARTIARTL","BPCL",
        "BRITANNIA","CIPLA","COALINDIA","DRREDDY",
        "EICHERMOT","GAIL","GRASIM","HCLTECH",
        "HDFC","HDFCBANK","HEROMOTOCO","HINDALCO",
        "HINDUNILVR","ICICIBANK","INDUSINDBK","INFY",
        "IOC","ITC","JSWSTEEL","KOTAKBANK",
        "LT","MARUTI","MM","NESTLEIND",
        "NTPC","ONGC","POWERGRID","RELIANCE",
        "SBIN","SHREECEM","SUNPHARMA","TATAMOTORS",
        "TATASTEEL","TCS","TECHM","TITAN",
        "ULTRACEMCO","UPL","VEDL","WIPRO","ZEEL"
    ],

    "Banking & Finance": [
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "AXISBANK",
        "KOTAKBANK",
        "INDUSINDBK",
        "BAJFINANCE",
        "BAJAJFINSV",
        "HDFC"
    ],

    "IT": [
        "TCS",
        "INFY",
        "WIPRO",
        "HCLTECH",
        "TECHM"
    ],

    "Pharma": [
        "SUNPHARMA",
        "DRREDDY",
        "CIPLA",
        "UPL"
    ],

    "Auto": [
        "MARUTI",
        "TATAMOTORS",
        "BAJAJ-AUTO",
        "HEROMOTOCO",
        "EICHERMOT",
        "MM"
    ],

    "FMCG & Consumer": [
        "HINDUNILVR",
        "ITC",
        "NESTLEIND",
        "BRITANNIA",
        "TITAN",
        "ASIANPAINT"
    ],

    "Energy & Utilities": [
        "RELIANCE",
        "ONGC",
        "GAIL",
        "IOC",
        "BPCL",
        "NTPC",
        "POWERGRID",
        "COALINDIA"
    ],

    "Metals & Mining": [
        "TATASTEEL",
        "JSWSTEEL",
        "HINDALCO",
        "VEDL"
    ],

    "Infrastructure & Cement": [
        "LT",
        "ADANIPORTS",
        "ULTRACEMCO",
        "SHREECEM",
        "GRASIM"
    ],

    "Telecom & Media": [
        "BHARTIARTL",
        "ZEEL"
    ]
}


HORIZON_INDEX = {
    "3M": 0,
    "6M": 1,
    "1Y": 2,
    "2.5Y": 3,
    "5Y": 4
}


def get_recommendation(ret):

    if ret > 20:
        return "Strong Buy"

    elif ret > 10:
        return "Buy"

    elif ret > 0:
        return "Hold"

    elif ret > -10:
        return "Sell"

    else:
        return "Strong Sell"


def rank_companies(category,
                   horizon,
                   investment,
                   mae_dict):

    latest_df = pd.read_csv("latest_features.csv")

    companies = CATEGORY_MAP[category]

    results = []

    idx = HORIZON_INDEX[horizon]

    for company in companies:

        row = latest_df[
            latest_df["Company"] == company
        ]

        if len(row) == 0:
            continue

        X = row[FEATURES]

        scaler = joblib.load(
            f"scalers/{company}_scaler.pkl"
        )

        model = load_model(
            f"models/{company}_model.keras",
            compile = False
        )

        X_scaled = scaler.transform(X)

        pred = model.predict(
            X_scaled,
            verbose=0
        )[0]

        predicted_return = float(pred[idx])

        future_value = (
            investment *
            (1 + predicted_return/100)
        )

        mae = mae_dict.get(company, 30)

        confidence = max(
            0,
            100 - mae
        )

        score = predicted_return * (confidence / 100)

        results.append({
            "Company": company,
            "Predicted Return (%)":
                round(predicted_return, 2),

            "Future Value":
                round(future_value, 2),

            "Confidence (%)":
                round(confidence, 2),

            "Recommendation":
                get_recommendation(
                    predicted_return
                ),

            "Score": round(score, 2)
        })

    results = pd.DataFrame(results)

    results = results.sort_values(
        "Score",
        ascending=False
    )

    return results.head(10)