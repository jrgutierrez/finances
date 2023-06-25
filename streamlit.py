import streamlit as st
import plotly.express as px
from data import get_data

st.set_page_config(layout="wide")

data = get_data()

window = st.sidebar.radio(
        "Select window 👇",
        options=["Overview", "Detail", "Forecasting"],
    )

group_time = st.sidebar.radio(
        "Select time group 👇",
        options=["Day", "Week", "Month"],
    )

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

if group_time == 'Day':
    data_1 = data.groupby(lambda x: x.date).aggregate({'price': 'sum'})

if group_time == 'Week':
    data_1 = data.groupby(lambda x: x.isocalendar()[1]).aggregate({'price': 'sum'})

if group_time == 'Month':
    data_1 = data.groupby(lambda x: x.month).aggregate({'price': 'sum'})


fig = px.bar(data_1, x = data_1.index, y = 'price', title = f'{data.columns} evolution')
fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                  yaxis_title = 'Billing')
fig.update_traces(marker_color='green')
st.plotly_chart(fig, use_container_width=True)

data = data.groupby('company').agg({'price': 'sum'})

fig = px.bar(data, x = data.index, y = 'price', title = 'Billing by company')
fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                  yaxis_title = 'Billing')
fig.update_traces(marker_color='green')
st.plotly_chart(fig, use_container_width=True)