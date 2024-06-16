import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def generate_radar_chart(app,data,hover_name=None):
    rfm_score = data.groupby('segmentation').agg(
        {'recency_score': 'mean', 'frequency_score': 'mean', 'monetary_score': 'mean'})
    rfm_score.reset_index(inplace=True)

    categories = ['recency_score', 'frequency_score', 'monetary_score']
    fig = go.Figure()

    for i, row in rfm_score.iterrows():
        r_values = [row["recency_score"], row["frequency_score"], row["monetary_score"]]
        r_values.append(r_values[0])
        theta_values = categories + [categories[0]]

        line_dash = 'solid' if row["segmentation"] == hover_name else 'dash'
        fill_option = 'toself' if row["segmentation"] == hover_name else 'none'

        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            fill=fill_option,
            name=row["segmentation"],
            line=dict(dash=line_dash),
            text=row["segmentation"]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        template='plotly_dark',
    )
    chart = dcc.Graph(id='segmentation-radar-chart', figure=fig)
    radar_chart = html.Div([html.H4('Average RFM score of each segmentation'),
                          chart])
    return radar_chart

def register_callbacks_radar_chart(app, data):
    rfm_score = data.groupby('segmentation').agg(
        {'recency_score': 'mean', 'frequency_score': 'mean', 'monetary_score': 'mean'})
    rfm_score.reset_index(inplace=True)
    @app.callback(
        Output('segmentation-radar-chart', 'figure'),
        Input('segmentation-radar-chart', 'hoverData')
)
    def update_figure(hoverData):
        fig = go.Figure()
        if hoverData is None:
            for i, row in rfm_score.iterrows():
                r_values = [row["recency_score"], row["frequency_score"], row["monetary_score"]]
                r_values.append(r_values[0])
                theta_values = ['recency_score', 'frequency_score', 'monetary_score', 'recency_score']

                line_dash = 'solid'
                fill_option = 'toself'

                fig.add_trace(go.Scatterpolar(
                    r=r_values,
                    theta=theta_values,
                    fill=fill_option,
                    name=row["segmentation"],
                    line=dict(dash=line_dash),
                    text=row["segmentation"]
                ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=True,
                template='plotly_dark',
            )
        else:
            hover_index = hoverData['points'][0]['curveNumber']
            hover_name = rfm_score.iloc[hover_index]['segmentation']
            for i, row in rfm_score.iterrows():
                r_values = [row["recency_score"], row["frequency_score"], row["monetary_score"]]
                r_values.append(r_values[0])
                theta_values = ['recency_score', 'frequency_score', 'monetary_score', 'recency_score']

                line_dash = 'solid' if row["segmentation"] == hover_name else 'dash'
                fill_option = 'toself' if row["segmentation"] == hover_name else 'none'

                fig.add_trace(go.Scatterpolar(
                    r=r_values,
                    theta=theta_values,
                    fill=fill_option,
                    name=row["segmentation"],
                    line=dict(dash=line_dash),
                    text=row["segmentation"]
                ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )
                ),
                showlegend=True,
                template='plotly_dark'
            )

        return fig