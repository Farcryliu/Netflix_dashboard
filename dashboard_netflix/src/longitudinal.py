import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


def generate_longitudinal_chart(data):
    months = data['month'].dt.to_period('M').unique()
    month_years = [str(month.start_time.year) for month in months]  # 仅提取年份
    month_marks = {str(i): year if month.start_time.month == 1 else '' for i, (year, month) in
                   enumerate(zip(month_years, months))}

    layout = html.Div(
        [dbc.Row([
             html.H4("Longitudinal Change in Average Monthly Views per User", style={'color': 'white', 'textAlign': 'center'})
         ]),
        dbc.Row([
        dcc.Graph(id='line-plot')]),
        dbc.Row([
        dcc.RangeSlider(
            id='month-slider',
            min=0,
            max=len(months) - 1,
            value=[0, len(months) - 1],
            marks=month_marks,
            step=None
        )])
    ])

    return layout

def register_callbacks_longitudinal_chart(app, data):
    @app.callback(
        Output('line-plot', 'figure'),
        Input('month-slider', 'value')
    )
    def update_figure(selected_range):
        months = data['month'].dt.to_period('M').unique()
        start_month = months[selected_range[0]].start_time
        end_month = months[selected_range[1]].end_time  # 使用月份的结束时间作为结束点
        filtered_df = data[(data['month'] >= start_month) & (data['month'] <= end_month)]

        fig = px.line(filtered_df, x="month", y="counts", color="type", line_group="type", hover_name="type",
                      color_discrete_map={'episode': '#ffcc00', 'movie': px.colors.qualitative.Plotly[0]})
        fig.update_layout(template='plotly_dark', transition_duration=500)  # 设置模板为 plotly_dark
        return fig

