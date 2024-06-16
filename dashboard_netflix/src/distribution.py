from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def generate_distribution_chart(data):
    return html.Div([
        dbc.Row([
            html.H4("Check the distribution of your interest metric", style={'color': 'white', 'textAlign': 'center'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Group", style={'color': 'white', 'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[
                            {'label': 'Gender', 'value': 'gender'},
                            {'label': 'Age Group', 'value': 'age_group'},
                            {'label': 'Segmentation', 'value': 'segmentation'}
                        ],
                        value='gender',
                        style={'width': '100%', 'color': 'black', 'backgroundColor': '#f8f9fa'}
                    ),
                ]),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H6("Metric", style={'color': 'white', 'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[
                            {'label': 'Recency (Days since the last recorded viewing)', 'value': 'recency'},
                            {'label': 'Frequency', 'value': 'frequency'},
                            {'label': 'Monetary', 'value': 'monetary'},
                            {'label': 'View Numbers', 'value': 'view_num'},
                        ],
                        value='recency',
                        style={'width': '100%', 'color': 'black', 'backgroundColor': '#f8f9fa'}
                    ),
                ]),
            ], width=6),
            html.Br(),  # 添加一行空白行
            dcc.Graph(id='indicator-graphic')
        ], style={'padding': '10px'})
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
                             yaxis_column_name: yaxis_column_name.capitalize()},
                     template='plotly_dark')
        fig.update_layout(xaxis_title=xaxis_column_name.capitalize(),
                          yaxis_title=yaxis_column_name.capitalize(),
                          margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                          hovermode='closest'
                          )
        return fig