import plotly.graph_objs as go
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def generate_bar_chart(data):
    overall_segmentation_counts = data['segmentation'].value_counts()
    fig = go.Figure(
        data=[
            go.Bar(
                x=overall_segmentation_counts.index,
                y=overall_segmentation_counts.values,
                name='Frequency',
                marker={'color': '#ffcc00'}
            ),
        ],
        layout={
            'xaxis': {'title': 'Segmentation'},
            'yaxis': {'title': 'Frequency'},
            'template': 'plotly_dark'
        }
    )

    radio_items = dbc.RadioItems(
        id='segmentation-radio',
        options=[
            {'label': 'Overall', 'value': 'overall'},
            {'label': 'Gender', 'value': 'gender'}
        ],
        value='overall',
        labelStyle={'display': 'inline-block'},
        inline=True
    )

    chart = dcc.Graph(id='segmentation-bar-chart', figure=fig)

    bar_chart = html.Div([html.H4('Frequency distribution of segmentation'),
                          html.H6('Distribution in:'),
                          radio_items,
                          chart])
    return bar_chart

def register_callbacks_barchart(app, data):
    @app.callback(
        Output('segmentation-bar-chart', 'figure'),
        [Input('segmentation-radio', 'value')]
    )
    def update_chart(option):
        if option == 'overall':
            overall_segmentation_counts = data['segmentation'].value_counts()
            overall_segmentation_counts_sorted = overall_segmentation_counts.sort_index()  # 根据索引排序，保持顺序不变
            updated_fig = go.Figure(
                data=[
                    go.Bar(
                        x=overall_segmentation_counts_sorted.index,
                        y=overall_segmentation_counts_sorted.values,
                        name='Frequency',
                        marker={'color': '#ffcc00'}
                    ),
                ],
                layout={
                    'xaxis': {'title': 'Segmentation'},
                    'yaxis': {'title': 'Frequency'},
                    'template': 'plotly_dark'
                }
            )
        elif option == 'gender':
            gender_segmentation_counts = data.groupby(['segmentation', 'gender']).size().unstack(fill_value=0)
            gender_segmentation_counts_sorted = gender_segmentation_counts.sort_index()  # 根据索引排序，保持顺序不变
            colors = ['#ffcc00', '#008080']
            updated_fig = go.Figure(
                data=[
                    go.Bar(
                        x=gender_segmentation_counts_sorted.index,
                        y=gender_segmentation_counts_sorted[column],
                        name=column,
                        marker={'color': colors[i]}  # 使用不同颜色
                    ) for i, column in enumerate(gender_segmentation_counts_sorted.columns)  # 使用enumerate()为每个 stack 设置不同颜色
                ],
                layout={
                    'xaxis': {'title': 'Segmentation'},
                    'yaxis': {'title': 'Frequency'},
                    'barmode': 'stack',
                    'template': 'plotly_dark'
                }
            )
        return updated_fig