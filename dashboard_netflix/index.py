from dash import html, Dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from src.barcharts import generate_bar_chart, register_callbacks_barchart
from src.radarchart import generate_radar_chart,register_callbacks_radar_chart
from src.distribution import generate_distribution_chart,register_callbacks_distribution
from src.longitudinal import generate_longitudinal_chart,register_callbacks_longitudinal_chart
from src.genre import generate_genre_chart,register_callbacks_genre_chart

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], title='Netflix Data Analysis Dashboard')
server = app.server
def generate_stats_card (title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '80px','alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px','fontSize': '30px','fontWeight': 'bold','color':'black'}),
                html.H4(title, className="card-title", style={'margin': '0px','fontSize': '25px','fontWeight': 'bold','color':'black'}),
            ], style={'textAlign': 'center'}),
        ], style={'paddingBlock':'10px',"backgroundColor":'#ffcc00','border':'none','borderRadius':'10px','height': '220px'})
    )


# Call generate_bar_chart function to get the components
data = pd.read_csv('netflix_user_segs.csv')
data2 = pd.read_csv('longitudinal_counts.csv')
data2['month'] = pd.to_datetime(data2['month'])
data3 = pd.read_csv('netflix_genre.csv')
register_callbacks_barchart(app, data)
register_callbacks_radar_chart(app, data)
register_callbacks_distribution(app, data)
register_callbacks_longitudinal_chart(app,data2)
register_callbacks_genre_chart(app,data3)

num_of_respondents = 77
num_of_views = 125097
monthly_view_nums = 28.25
engagement_time = 1435.70

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Img(src="./assets/netflix_logo.png",width="400")],width=4,align="center"),
            dbc.Col([html.H2("Consumer Segmentation Dashboard", style={'textAlign': 'center'})], width=8, align="center")
            ], align="center"),
        dbc.Row([
            dbc.Col(generate_stats_card("Respondents",num_of_respondents,"./assets/users_icon.png"), width=3,align="center"),
            dbc.Col(generate_stats_card("Total views",num_of_views,"./assets/views.png"), width=3,align="center"),
            dbc.Col(generate_stats_card("Average monthly views",monthly_view_nums,"./assets/movie-icon.png"),width=3,align="center"),
            dbc.Col(generate_stats_card("Engagement time per person",engagement_time,"./assets/engagement_time.png"),width=3,align="center"),
        ]),
        html.Div(style={'margin': '20px'}),
        dbc.Row([
            dbc.Col(generate_bar_chart(data), width=6),
            dbc.Col(generate_radar_chart(app,data,hover_name=None), width=6),
        ]),
        html.Div(style={'margin': '20px'}),
        dbc.Row([
            dbc.Col(generate_distribution_chart(data),width = 6),
            dbc.Col(generate_genre_chart(),width = 6)
        ]),
        html.Div(style={'margin': '20px'}),
        dbc.Row([
            dbc.Col(generate_longitudinal_chart(data2),width = 12),
        ])
    ])
],style={'backgroundColor': 'black', 'minHeight': '100vh'})

if __name__ == '__main__':
    app.run(debug=True,port=8081)