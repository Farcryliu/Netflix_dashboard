import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv('../netflix_genre.csv')  # 请替换为您的实际文件路径

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Top 5 Genres by Count and Proportion"),
    html.Label("Select Gender:"),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Male', 'value': 'male'},
            {'label': 'Female', 'value': 'female'}
        ],
        value='all'
    ),
    html.Label("Select Age Group:"),
    dcc.Dropdown(
        id='age-dropdown',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': '20 to 40', 'value': '20 to 40'},
            {'label': '40 to 65', 'value': '40 to 65'},
            {'label': '65 to 80', 'value': '65 to 80'}
        ],
        value='all'
    ),
    dcc.Graph(id='genre-bar-chart')
])


@app.callback(
    Output('genre-bar-chart', 'figure'),
    [Input('gender-dropdown', 'value'),
     Input('age-dropdown', 'value')]
)
def update_chart(selected_gender, selected_age):
    filtered_df = df.copy()

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


if __name__ == '__main__':
    app.run_server(debug=True)