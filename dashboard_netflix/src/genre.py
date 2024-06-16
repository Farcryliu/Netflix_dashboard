import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

def generate_genre_chart():
    return html.Div([
        dbc.Row([
            html.H4("Top 5 Genres Viewed", style={'color': 'white', 'textAlign': 'center'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Select Gender:", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='gender-dropdown',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Male', 'value': 'male'},
                            {'label': 'Female', 'value': 'female'}
                        ],
                        value='all',
                        style={'color': 'black', 'backgroundColor': '#f8f9fa'}
                    ),
                ]),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.Label("Select Age Group:", style={'color': 'white'}),
                    dcc.Dropdown(
                        id='age-dropdown',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': '20 to 40', 'value': '20 to 40'},
                            {'label': '40 to 65', 'value': '40 to 65'},
                            {'label': '65 to 80', 'value': '65 to 80'}
                        ],
                        value='all',
                        style={'color': 'black', 'backgroundColor': '#f8f9fa'}
                    ),
                ]),
            ], width=6),
        ]),
        dbc.Row([
            dcc.Graph(id='genre-bar-chart')
        ]),
    ], style={'padding': '10px'})

def register_callbacks_genre_chart(app, data):
    @app.callback(
        Output('genre-bar-chart', 'figure'),
        [Input('gender-dropdown', 'value'),
         Input('age-dropdown', 'value')]
    )
    def update_chart(selected_gender, selected_age):
        filtered_df = data.copy()

        if selected_gender != 'all':
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

        if selected_age != 'all':
            filtered_df = filtered_df[filtered_df['age_group'] == selected_age]

        genre_counts = filtered_df['genre'].value_counts().nlargest(5)
        genre_proportions = genre_counts / genre_counts.sum()

        fig = px.bar(
            y=genre_counts.index,
            x=genre_counts.values,
            text=genre_proportions.apply(lambda x: f"{x:.2%}"),
            labels={'y': 'Genre', 'x': 'Count'},
            title="Top 5 Genres by Count and Proportion",
            orientation='h'  # 设置条形图为横向
        )
        fig.update_layout(template='plotly_dark')

        return fig