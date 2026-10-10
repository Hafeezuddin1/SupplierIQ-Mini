
# SupplierIQ Mini

An interactive supplier comparison prototype built with Python.

## Features
- Compare suppliers by price, delivery time, and quality
- Adjust scoring preferences
- Automatically rank suppliers
- Search suppliers by name
- Explain why the top supplier ranks first

## Technologies
- Python
- Pandas
- Streamlit

## Data and limitations
This prototype uses fictional supplier data. Rankings are calculated using a weighted scoring formula. It does not currently use an AI model or verify real supplier performance.

## Run locally
Install dependencies:

`pip install -r requirements.txt`

Run the dashboard:

`python -m streamlit run app.py`