import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import gspread
import streamlit as st


def get_raw_data():
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    spreadsheet = gc.open_by_key(st.secrets["sheet_id"])
    worksheet = spreadsheet.worksheet(st.secrets["sheet_name"])
    data = pd.DataFrame(worksheet.get_all_records())
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date').sort_index()

def prepare_data(data):
    data = data[['company', 'description', 'price']]
    
    data = data.groupby(lambda x: x.date).aggregate({'price': 'sum'})
    return data.reindex(pd.date_range(data.index[0], data.index[-1])).fillna(1)

def get_data():
    data = get_raw_data()
    return prepare_data(data)