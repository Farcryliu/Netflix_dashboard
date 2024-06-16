import dash
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd

# 创建示例数据
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [20, 30, 40, 50]
}
df = pd.DataFrame(data)

# 创建 Dash 应用
app = dash.Dash(__name__)

# 布局设置
app.layout = html.Div([
    html.Div([
        html.H1('Data Dashboard'),
    ], style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(
            id='pie-chart',
            figure={
                'data': [
                    go.Pie(
                        labels=df['Category'],
                        values=df['Values']
                    )
                ],
                'layout': go.Layout(
                    title='Pie Chart'
                )
            }
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(
            id='bar-chart',
            figure={
                'data': [
                    go.Bar(
                        x=df['Category'],
                        y=df['Values']
                    )
                ],
                'layout': go.Layout(
                    title='Bar Chart'
                )
            }
        )
    ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '2%'}),

    html.Div([
        dcc.Graph(
            id='line-chart',
            figure={
                'data': [
                    go.Scatter(
                        x=df['Category'],
                        y=df['Values'],
                        mode='lines+markers'
                    )
                ],
                'layout': go.Layout(
                    title='Line Chart'
                )
            }
        )
    ], style={'width': '100%', 'display': 'inline-block', 'marginTop': '2%'})
])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
