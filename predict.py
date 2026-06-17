import numpy as np
import joblib
from keras.models import load_model

def predict_stock(company, input_data, mae_dict, investment):

    model = load_model(f"models/{company}_model.keras", compile = False)
    scaler = joblib.load(f"scalers/{company}_scaler.pkl")

    input_array = np.array(input_data).reshape(1, -1)
    input_scaled = scaler.transform(input_array)

    pred = model.predict(input_scaled)[0]

    # Short-term decision
    avg = np.mean(pred[:3])

    if pred[0] > 8 and pred[1] > 10 and pred[2] > 15:
        rec = "STRONG BUY"
    elif avg > 5:
        rec = "BUY"
    elif avg > 0:
        rec = "HOLD"
    elif avg < 0:
        rec = "SELL"
    else:
        rec = "STRONG SELL"

    # Confidence
    mae = mae_dict.get(company, 30)
    confidence = max(0, 100 - mae)

    # Future value
    future = {
        "3M": investment * (1 + pred[0]/100),
        "6M": investment * (1 + pred[1]/100),
        "1Y": investment * (1 + pred[2]/100)
    }

    return pred, rec, confidence, future