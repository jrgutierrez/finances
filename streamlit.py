import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from data import get_data

st.set_page_config(layout = 'wide')

data = get_data()

window = st.sidebar.radio(
        'Select window 👇',
        options=['Overview', 'Detail', 'Forecasting'],
    )

if window in ['Overview', 'Detail']:
    group_time = st.sidebar.radio(
            'Select time group 👇',
            options=['Day', 'Week', 'Month'],
        )

if window == 'Forecasting':
    n_fc = st.sidebar.number_input('Insert Forecasting days:', min_value=1, max_value=60, value=15)

initial_date = st.sidebar.date_input(
    'Select initial date:',
    datetime(2023, 6, 1),
    min_value = datetime(2023, 6, 1), 
    max_value = datetime.today())

final_date = st.sidebar.date_input(
    'Select final date:',
    datetime.today(),
    min_value = datetime(2023, 6, 1), 
    max_value = datetime.today())


data = data.loc[initial_date:final_date]

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 150px;
    color: rgb(0, 255, 0);
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
if window in ['Overview', 'Detail']:
    if group_time == 'Day':
        data_evo = data.groupby(lambda x: x.date).aggregate({'price': 'sum'})
        data_evo = data_evo.reindex(pd.date_range(datetime(2023, 6, 1), datetime.today())).fillna(0)

    if group_time == 'Week':
        data_evo = data.groupby(lambda x: x.isocalendar()[1]).aggregate({'price': 'sum'})

    if group_time == 'Month':
        data_evo = data.groupby(lambda x: x.month).aggregate({'price': 'sum'})

if window == 'Forecasting':
    data_evo = data.groupby(lambda x: x.date).aggregate({'price': 'sum'})
    data_evo = data_evo.reindex(pd.date_range(datetime(2023, 6, 1), datetime.today())).fillna(0)

def overview_plots():
    st.metric(label = "Total Billed", value = f"{sum(data['price']):.2f}€")

    fig = px.line(data_evo, x = data_evo.index, y = 'price', markers = True, title = f'Billing evolution')
    fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                    yaxis_title = 'Billing')
    fig.update_traces(line_color = '#00ff00')
    st.plotly_chart(fig, use_container_width=True)


def detail_plots():
    fig = px.bar(data_evo, x = data_evo.index, y = 'price', title = f'Billing evolution')
    fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                    yaxis_title = 'Billing')
    fig.update_traces(marker_color='green', marker_line_color = 'green', marker_line_width = 1)
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True)

    data_company = data.groupby('company').agg({'price': 'sum'})#.drop(0)
    fig = px.bar(data_company, x = data_company.index, y = 'price', title = 'Billing by company')
    fig.update_layout(xaxis_title = 'Company', 
                    yaxis_title = 'Billing')
    fig.update_traces(marker_color='green', marker_line_color = 'green', marker_line_width = 1)
    fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True)


def forecast(data, forecast_days = 15):
    from statsmodels.tsa.arima.model import ARIMA
    import warnings
    warnings.filterwarnings('ignore')
    from datetime import timedelta

    y = data['price']

    ARIMAmodel = ARIMA(y, order = (5, 2, 5))
    ARIMAmodel = ARIMAmodel.fit()

    y_pred = ARIMAmodel.get_forecast(forecast_days)
    y_pred_df = y_pred.conf_int(alpha = 0.05) 
    y_pred_df["Predictions"] = ARIMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = [data.index[-1] + timedelta(days = i) for i in range(forecast_days)]
    return y_pred_df


def fc_plots():
    y_pred_out = forecast(data_evo, n_fc)
    fig = px.line(data_evo, x = data_evo.index, y = 'price', markers = True, title = 'Billing Forecast', color_discrete_sequence=['#00ff00'])
    fig.add_scatter(x=y_pred_out.index, y=y_pred_out['Predictions'], mode='markers+lines')
    fig.update_traces(showlegend=False)
    fig.update_layout(xaxis_title = 'Week'if group_time == 'Week' else 'Month' if group_time == 'Month' else 'Date', 
                    yaxis_title = 'Billing')
    st.plotly_chart(fig, use_container_width=True)

if window == 'Overview':
    overview_plots()

if window == 'Detail':
    detail_plots()

if window == 'Forecasting':
    fc_plots()