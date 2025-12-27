# 📊 Retail-Grade Equity Research Platform

A transparent, assumption-driven equity research and valuation platform built in Python.  
This project is designed to make institutional-style financial analysis accessible to retail investors while prioritizing clarity, explainability, and sound financial logic.

---

## 🚀 Project Overview

The **Retail-Grade Equity Research Platform** is an interactive web application that allows users to:

- Analyze real company financial statements  
- Compute key financial ratios used in professional equity research  
- Evaluate company performance, financial health, and valuation metrics  
- Understand how accounting data translates into investment insights  

The platform is built with **Streamlit** and sources public financial data via **Yahoo Finance**.

---

## 🧠 Motivation

Most retail investors rely on opaque metrics or black-box valuation tools.  
This project focuses on:

- **Transparency** — every metric is derived from clearly defined financial statements  
- **Explainability** — users can understand *why* a company looks attractive or risky  
- **Educational value** — mirrors how equity research is performed in real finance roles  

---

## 🛠️ Tech Stack

- Python  
- Streamlit (interactive web app)  
- pandas / numpy (data manipulation)  
- yfinance (financial data sourcing)  
- Git + GitHub (version control)  

---

## 📂 Project Structure

```
Retail-Grade-Equity-Research-Platform/
│
├── app.py              # Streamlit application entry point
├── data.py             # Financial data ingestion (Yahoo Finance)
├── metrics.py          # Key financial ratio calculations
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── venv/               # Virtual environment (local)
```

---

## 📈 Key Features

### 1️⃣ Financial Statements Viewer
- Income Statement  
- Balance Sheet  
- Cash Flow Statement  
- Displayed in readable, formatted tables (in millions)

### 2️⃣ Key Financial Metrics

**Profitability**
- Gross Margin  
- Operating Margin  
- Net Margin  

**Liquidity**
- Current Ratio  
- Quick Ratio  

**Leverage**
- Debt-to-Equity  
- Return on Equity (ROE)  

**Efficiency**
- Return on Assets (ROA)  

**Valuation**
- P/E Ratio  
- P/B Ratio  

Metrics are calculated dynamically using the most recent annual financial data.

---

## 📊 Methodology Notes

- Financial statement data is sourced from **Yahoo Finance**  
- Ratios are calculated using reported accounting figures  
- Market-based ratios (e.g. P/E, P/B) use current share prices  
- Accounting and market data may reflect different dates  
- Metrics are intended for **comparative and educational analysis**, not investment advice  

---

## ▶️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/svarpatel30/Retail-Grade-Equity-Research-Platform.git
cd Retail-Grade-Equity-Research-Platform
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python -m streamlit run app.py
```

Open your browser at:  
http://localhost:8501

---

## 🧩 Future Enhancements

- Discounted Cash Flow (DCF) valuation model  
- Bull / Base / Bear case scenario analysis  
- Free Cash Flow–based valuation metrics  
- Historical trend analysis and visualizations  
- Expanded company overview and qualitative insights  

---

## ⚠️ Disclaimer

This project is for **educational and informational purposes only**.  
It does not constitute financial advice or investment recommendations.

---

## 👤 Author

**Svar Patel**  
Aspiring finance professional with interests in equity research, valuation, and financial analytics.

---

## ⭐ Why This Project Matters

This platform demonstrates:
- Practical application of accounting and finance concepts  
- Data-driven financial analysis and modeling skills  
- Tooling similar to entry-level equity research workflows  

It is designed to grow into a full-featured research platform while remaining transparent and explainable.
