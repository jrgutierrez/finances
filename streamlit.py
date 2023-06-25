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

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 200px;
}
/*center metric label*/
[data-testid="stMetricLabel"] > div:nth-child(1) {
    display: flex;
    justify-content: center;
}

/*center metric value*/
[data-testid="stMetricValue"] > div:nth-child(1) {
    display: flex;
    justify-content: center;
}
</style>
""",
    unsafe_allow_html=True,
)
st.metric(label = "Total Billed", value = f"{sum(data['price']):.2f}€")

if group_time == 'Day':
    data_evo = data.groupby(lambda x: x.date).aggregate({'price': 'sum'})

if group_time == 'Week':
    data_evo = data.groupby(lambda x: x.isocalendar()[1]).aggregate({'price': 'sum'})

if group_time == 'Month':
    data_evo = data.groupby(lambda x: x.month).aggregate({'price': 'sum'})


fig = px.bar(data_evo, x = data_evo.index, y = 'price', title = f'Billing evolution')
fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                  yaxis_title = 'Billing')
fig.update_traces(marker_color='green', marker_line_color = 'green', marker_line_width = 1)
fig.update_xaxes(type='category')
st.plotly_chart(fig, use_container_width=True)

data_company = data.groupby('company').agg({'price': 'sum'})
fig = px.bar(data_company, x = data_company.index, y = 'price', title = 'Billing by company')
fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                  yaxis_title = 'Billing')
fig.update_traces(marker_color='green', marker_line_color = 'green', marker_line_width = 1)
fig.update_xaxes(type='category')
st.plotly_chart(fig, use_container_width=True)