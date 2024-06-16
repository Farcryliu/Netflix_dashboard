from dash import Dash, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def generate_distribution_chart(data):
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[
                    {'label': 'Gender', 'value': 'gender'},
                    {'label': 'Age Group', 'value': 'age_group'},
                    {'label': 'Segmentation', 'value': 'segmentation'}
                ],
                value='gender',
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[
                    {'label': 'Recency', 'value': 'recency'},
                    {'label': 'Frequency', 'value': 'frequency'},
                    {'label': 'Monetary', 'value': 'monetary'},
                    {'label': 'View Numbers', 'value': 'view_num'},
                ],
                value='recency',
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        dcc.Graph(id='indicator-graphic')
    ])

def register_callbacks_distribution(app, data):
    @app.callback(
        Output('indicator-graphic', 'figure'),
        [Input('xaxis-column', 'value'),
         Input('yaxis-column', 'value')])
    def update_graph(xaxis_column_name, yaxis_column_name):
        grouped_data = data.groupby(xaxis_column_name).agg({yaxis_column_name: 'mean'}).reset_index()
        fig = px.bar(grouped_data, x=xaxis_column_name, y=yaxis_column_name,
                     labels={xaxis_column_name: xaxis_column_name.capitalize(),
                             yaxis_column_name: yaxis_column_name.capitalize()})
        fig.update_layout(xaxis_title=xaxis_column_name.capitalize(),
                          yaxis_title=yaxis_column_name.capitalize(),
                          margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                          hovermode='closest')
        return fig