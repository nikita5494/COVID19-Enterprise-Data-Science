import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_bootstrap_components as dbc
import plotly.io as pio

import os
print(os.getcwd())
df_input_large=pd.read_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_final_set.csv',sep=';')
df_SIR_large=pd.read_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_JH_flat_table_confirmed.csv',sep=';',parse_dates=[0])
df_SIR_large=df_SIR_large.sort_values('date',ascending=True)

fig=go.Figure()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'COVID-19 Dashboard based on Applied Data Science'

app.layout = html.Div([

        dbc.Row(dbc.Col(html.H1('COVID-19 Data Dashboard Visualization using Applied Data Science'),
                        width={'size': 8, 'offset': 1},
                        ),
                ),

        dbc.Row(dbc.Col(html.Div('''
                            Goal of the project is to teach data science by applying a cross industry standard process,
                            it covers the full walkthrough of: automated data gathering, data transformations,
                            filtering and machine learning to approximating the doubling time, and
                            (static) deployment of responsive dashboard alongwith SIR simulation.
                            '''),
                        width={'size': 8, 'offset': 1},
                        )
                ),


       dbc.Row(dbc.Col(html.H5('Select a single country for SIR simulation curve'),
                        width={'size': 5, 'offset': 1},
                        ),
                ),

        dbc.Row(
        [
                  dbc.Col(

                        dcc.Dropdown( id='single_select_country',
                             options=[{'label':each,'value':each} for each in df_SIR_large.columns[1:]],
                             value='Germany',
                             multi=False),
                             width={'size': 5, "offset": 1, 'order': 'second'}),
            ],
        ),


        dbc.Row(dbc.Col(html.H5('In order to manipulate the SIR curve, vary the values regarding the measures and press enter:'),
                        width={'size': 5, 'offset': 1},
                        ),
                ),


        dbc.Row(
        [

            #For changing beta ,gamma, t_initial, t_intro_measures,t_hold,t_relax
            dbc.Row(children=[
            html.Br(),
            html.Br(),
            html.Label(["No measures introduced (in days):",
                      dcc.Input(id='t_initial',
                     type='number',
                     value=28,debounce=True)],style={"margin-left": "30px"}),
            html.Label(["Measures introduced over (in days):",
                      dcc.Input(id='t_intro_measures',
                     type='number',
                     value=14,debounce=True)],style={"margin-left": "30px"}),
            html.Label(["Introduced measures hold time (in days):",
                      dcc.Input(id='t_hold',
                     type='number',
                     value=21,debounce=True)],style={"margin-left": "30px"}),
            html.Br(),
            html.Br(),
            html.Label(["Introduced measures relaxed (in days):",
                      dcc.Input(id='t_relax',
                     type='number',
                     value=21,debounce=True)],style={"margin-left": "30px"}),
            html.Label(["Beta max:",
                      dcc.Input(id='beta_max',
                     type='number',
                     value=0.4,debounce=True)],style={"margin-left": "30px"}),
            html.Label(["Beta min:",
                      dcc.Input(id='beta_min',
                     type='number',
                     value=0.11,debounce=True)],style={"margin-left": "30px"}),
            html.Label(["Gamma:",
                      dcc.Input(id='gamma',
                     type='number',
                     value=0.1,debounce=True)],style={"margin-left": "30px"}),
            html.Br(),
            html.Br(),
            ]
            ),


                dbc.Col(dcc.Graph(
                            figure=fig,
                            id='SIR_curve'),
                        width=6, md={'size': 10,  "offset": 1, 'order': 'last'}
                        ),
            ]
        ),

         dbc.Row(dbc.Col(html.H5('Multi - Select Country for Visualization'),
                        width={'size': 5, 'offset': 1},
                        ),
                ),


        dbc.Row(
            [
                dbc.Col(
                       dcc.Dropdown(
                      id='country_drop_down',
                      options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
                      value=['US', 'Germany','Italy'], # which are pre-selected
                      multi=True),
                      width={'size': 5, "offset": 1, 'order': 'first'}
                     ),

                ], no_gutters=True
        ),

      dbc.Row(dbc.Col(html.H5('Select Timeline of confirmed COVID-19 cases or the approximated doubling time'),
                        width={'size': 5, 'offset': 1},
                        ),
                ),


        dbc.Row(
            [
                dbc.Col(


                dcc.Dropdown(
                id='doubling_time',
                options=[
                    {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
                    {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
                    {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
                    {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
                ],
                value='confirmed',
                multi=False),
                width={'size': 3, "offset": 1, 'order': 'first'}
                        ),

             ],
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(
                            id='main_window_slope'
                            ),
                        width=6, md={'size': 8,  "offset": 1, 'order': 'first'}
                        ),

                ],
            ),
 ])


@app.callback(
    Output('SIR_curve', 'figure'),
    [Input('single_select_country', 'value'),
    Input('t_initial','value'),
    Input('t_intro_measures','value'),
    Input('t_hold','value'),
    Input('t_relax','value'),
    Input('beta_max','value'),
    Input('beta_min','value'),
    Input('gamma','value')])


def SIR_figure(country,initial_time,intro_measures,hold_time,relax_time,max_beta,min_beta,gamma_max):
    ydata=df_SIR_large[country][df_SIR_large[country]>=30]
    xdata=np.arange(len(ydata))
    N0=5000000
    I0=30
    S0=N0-I0
    R0=0
    gamma=gamma_max
    SIR=np.array([S0,I0,R0])

    t_initial=initial_time
    t_intro_measures=intro_measures
    t_hold=hold_time
    t_relax=relax_time
    beta_max=max_beta
    beta_min=min_beta
    propagation_rates=pd.DataFrame(columns={'susceptible':S0,'infected':I0,'recovered':R0})
    pd_beta=np.concatenate((np.array(t_initial*[beta_max]),
                       np.linspace(beta_max,beta_min,t_intro_measures),
                       np.array(t_hold*[beta_min]),
                       np.linspace(beta_min,beta_max,t_relax),
                       ))

    def SIR_model(SIR,beta,gamma):
        'SIR model for simulating spread'
        'S: Susceptible population'
        'I: Infected popuation'
        'R: Recovered population'
        'S+I+R=N (remains constant)'
        'dS+dI+dR=0 model has to satisfy this condition at all time'
        S,I,R=SIR
        dS_dt=-beta*S*I/N0
        dI_dt=beta*S*I/N0-gamma*I
        dR_dt=gamma*I
        return ([dS_dt,dI_dt,dR_dt])

    for each_beta in pd_beta:
        new_delta_vec=SIR_model(SIR,each_beta,gamma)
        SIR=SIR+new_delta_vec
        propagation_rates=propagation_rates.append({'susceptible':SIR[0],'infected':SIR[1],'recovered':SIR[2]},ignore_index=True)

    fig=go.Figure()
    fig.add_trace(go.Bar(x=xdata,
                         y=ydata,
                         marker=dict(color='Lightseagreen'),
                         name='Confirmed Cases'
                        ))

    fig.add_trace(go.Scatter(x=xdata,
                            y=propagation_rates.infected,
                            mode='lines',
                            marker=dict(color='DarkRed'),
                            name='Simulated curve'))

    fig.update_layout(shapes=[
                            dict(type='rect',xref='x',yref='paper',x0=0,y0=0,x1=t_initial,y1=1,fillcolor="MediumPurple",opacity=0.4,layer="below",line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial,y0=0,x1=t_initial+t_intro_measures,y1=1,fillcolor="MediumPurple",opacity=0.5,layer="below",line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial+t_intro_measures,y0=0,x1=t_initial+t_intro_measures+t_hold,y1=1,fillcolor="MediumPurple",opacity=0.6,layer='below',line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial+t_intro_measures+t_hold,y0=0,x1=t_initial+t_intro_measures+t_hold+t_relax,y1=1,fillcolor='MediumPurple',opacity=0.7,layer='below',line_width=0,)
                            ],
                    title='SIR Simulation Model for COVID19',
                    title_x=0.5,
                    xaxis=dict(title='Time (in days)',
                               titlefont_size=16),
                    yaxis=dict(title='Confirmed cases based on Johns Hopkins Data, log scale ',
                               type='log',
                                titlefont_size=16,
                              ),
                    width=1280,
                    height=600,
                     )
    return fig

@app.callback(
     Output('main_window_slope', 'figure'),
     [Input('country_drop_down', 'value'),
     Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):


     if 'doubling_rate' in show_doubling:
         my_yaxis={'type':"log",
                'title':'Approximated doubling rate over 3 days (larger numbers are better #stayathome)'
               }
     else:
         my_yaxis={'type':"log",
                   'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
               }


     traces = []
     for each in country_list:

         df_plot=df_input_large[df_input_large['country']==each]

         if show_doubling=='doubling_rate_filtered':
             df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
         else:
             df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()
        #print(show_doubling)


         traces.append(dict(x=df_plot.date,
                                 y=df_plot[show_doubling],
                                 mode='markers+lines',
                                 opacity=0.9,
                                 name=each
                         )
                 )

     return {
             'data': traces,
             'layout': dict (
                 height=720,

                 xaxis={'title':'Timeline',
                         'tickangle':-45,
                         'nticks':20,
                         'tickfont':dict(size=14,color="#7f7f7f"),
                       },

                 yaxis=my_yaxis
         )
     }
if __name__ == '__main__':
     app.run_server(debug=True,use_reloader=False)
