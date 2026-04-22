# MediCharge Analytics — Insurance Cost Predictor & Analyzer

A professional, multi-page Streamlit web application for Medical Insurance Charge Analysis and Prediction.

## Features

- **Home / Overview** — KPI dashboard with key dataset metrics and findings
- **Exploratory Data Analysis (EDA)** — Interactive Plotly charts covering distributions, categories, scatter plots, and box plots
- **Data Insights** — Correlation heatmaps, BMI/age group analysis, regional breakdowns, and risk summaries
- **Charge Predictor (ML Model)** — Linear Regression model to predict insurance charges based on patient details
- **Dataset Viewer** — Searchable, filterable data table with CSV export

## Tech Stack

- Python 3.9+
- Streamlit
- Pandas / NumPy
- Scikit-learn (Linear Regression)
- Plotly (interactive visualizations)

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset

- `hospital data.csv` — Raw dataset (~1070 records) with columns: age, sex, bmi, children, smoker, region, charges
- `cleaned_data.csv` — Preprocessed dataset with one-hot encoded categorical features

## License

For educational and analytics purposes only.
