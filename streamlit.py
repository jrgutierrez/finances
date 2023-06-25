import streamlit as st
import plotly.express as px
from data import get_data
from plotly.subplots import make_subplots


st.set_page_config(layout="wide")

data = get_data()




initial_date = st.sidebar.date_input(
    "Select initial date:",
    data.index[0],
    min_value=data.index[0], 
    max_value=data.index[-1])

final_date = st.sidebar.date_input(
    "Select final date:",
    data.index[-1],
    min_value=initial_date, 
    max_value=data.index[-1])


data = data.loc[initial_date:final_date]

fig = px.bar(data, x = data.index, y = 'price', markers = True, title = 'Billing evolution')
fig.update_traces(line_color='#00ff00')
fig.update_layout(xaxis_title = 'Date', yaxis_title = 'Billing')
st.plotly_chart(fig, use_container_width=True)