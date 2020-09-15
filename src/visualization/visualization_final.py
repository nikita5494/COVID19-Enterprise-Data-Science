import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.io as pio

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import os

print(os.getcwd())
df_input_large=pd.read_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_final_set.csv',sep=';')
df_SIR_large=pd.read_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_JH_flat_table_confirmed.csv',sep=';',parse_dates=[0])
df_SIR_large=df_SIR_large.sort_values('date',ascending=True)

fig=go.Figure()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    dcc.Markdown('''
    #  Enterprise Data Science Application on COVID 19 data

    Goal of the project is to teach data science by applying a cross industry standard process,
    it covers the full walkthrough of: automated data gathering, data transformations,
    filtering and machine learning to approximating the doubling time, and
    (static) deployment of responsive dashboard alongwith SIR Simulation

    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
        value=['US', 'Germany','Italy'], # which are pre-selected
        multi=True
    ),

    dcc.Tabs([
        dcc.Tab(label='Tab one', children=[
            dcc.Markdown('''
                ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
                '''),


            dcc.Dropdown(
            id='doubling_time',
            options=[
                {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
                {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
                {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
                {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
            ],
            value='confirmed',
            multi=False
            ),

            dcc.Graph(figure=fig, id='main_window_slope')
            ]),

        
