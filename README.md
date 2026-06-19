# 📈 NiveshAI - AI Powered Stock Recommendation Platform

NiveshAI is an AI-powered stock recommendation platform designed for Indian equity markets. It leverages Machine Learning and Deep Learning models to analyze historical stock data and provide intelligent investment recommendations based on the user's investment amount, sector preference, and investment horizon.

The platform predicts expected returns, estimates future portfolio value, calculates confidence scores, and ranks the best investment opportunities using company-specific trained models.

---

## 🚀 Live Demo

**Web Application:** https://niveshai-85ic.onrender.com/

---

# ✨ Features

* AI-powered stock recommendation engine
* Sector-wise investment analysis
* Multi-company ranking system
* Expected return prediction
* Future portfolio value estimation
* Confidence score generation
* Buy/Hold/Avoid recommendations
* Top 10 stock suggestions
* PDF report download
* Interactive Streamlit interface
* Deep learning models trained individually for companies
* Responsive UI suitable for both Light and Dark themes

---

# 🧠 Machine Learning Pipeline

### Data Collection

Historical stock data was collected and processed for multiple companies.

### Feature Engineering

Features used:

* Prev Close
* Open
* High
* Low
* Close
* VWAP
* Volume
* Turnover
* Daily_Return
* Volatility
* Momentum_5
* MA20_Ratio
* MA50_Ratio
* MA252_Ratio

### Data Preprocessing

* Missing value handling
* Scaling using StandardScaler
* Feature normalization

### Model Training

Deep learning models were trained separately for each company using TensorFlow/Keras.

### Prediction

The trained models predict stock returns and estimate:

* Expected Return (%)
* Future Value
* Confidence Score
* Investment Recommendation

---

# 🛠 Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Machine Learning

* TensorFlow
* Keras
* Scikit-Learn
* NumPy
* Pandas

### Visualization

* Streamlit DataFrame

### Report Generation

* ReportLab

### Deployment

* Render

### Version Control

* Git
* GitHub

---

# 📂 Project Structure

```text
NiveshAI
│
├── app.py
├── rank_companies.py
├── predict.py
├── requirements.txt
├── runtime.txt
├── README.md
├── latest_features.csv
├── mae_dict.pkl
│
├── models/
│      ├── company_model files
│
├── scalers/
│      ├── scaler files
│
├── data/
│      ├── stock datasets
│
├── notebooks/
│      └── NiveshAI_Model_Training.ipynb
│
└── screenshots/
```

---

# 📊 User Inputs

The platform takes:

* Investment Amount
* Investment Sector
* Investment Duration

---

# 📈 Output Generated

For each recommended company:

* Predicted Return (%)
* Estimated Future Value
* Confidence Score (%)
* Recommendation Type
* Overall Ranking Score

Top 10 companies are displayed to the user.

---

# 🖥 Installation and Local Setup

## Step 1 : Clone Repository

```bash
git clone https://github.com/piyushvohra25/NiveshAI.git
```

---

## Step 2 : Move into Project Folder

```bash
cd NiveshAI
```

---

## Step 3 : Create Virtual Environment

Windows:

```bash
python -m venv stock_env
```

Activate:

```bash
stock_env\Scripts\activate
```

---

## Step 4 : Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 : Run Application

```bash
streamlit run app.py
```

---

## Step 6 : Open Browser

```text
http://localhost:8501
```

---

# 📚 Training Notebook

Model training and feature engineering are available inside:

```text
notebooks/NiveshAI_Model_Training.ipynb
```

The notebook contains:

* Data preprocessing
* Feature engineering
* Scaling
* Model training
* Saving models
* Evaluation metrics

---

# 📌 Future Enhancements

* Live stock market API integration
* Portfolio management system
* User authentication
* Historical performance graphs
* Candlestick charts
* News sentiment analysis
* Risk assessment engine
* Portfolio diversification suggestions
* Real-time recommendations
* Mobile application

---

# 👨‍💻 Author

### Piyush Vohra