import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.io as pio


df_SIR_large=pd.read_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_JH_flat_table_confirmed.csv',sep=';',parse_dates=[0])
df_SIR_large=df_SIR_large.sort_values('date',ascending=True)

fig=go.Figure()
app=dash.Dash()

app.layout=html.Div([
        dcc.Markdown('''
                     # COVID-19 Data Dashboard visualization using Applied Data Science
                     This Dashboard provides a visual representation of the actual confirmed infected people and the simulated
                     SIR (susceptible,infected,recovered) curve.
                    '''),
    # For Country dropdown menu
        dcc.Markdown(''' ## Select a Country for Visualization'''),

        dcc.Dropdown( id='single_select_country',
                     options=[{'label':each,'value':each} for each in df_SIR_large.columns[1:]],
                     value='Germany',
                     multi=False),
    #For changing beta ,gamma, t_initial, t_intro_measures,t_hold,t_relax
    dcc.Markdown(''' ## In order to manipulate the SIR curve, change the values regarding to the measures and press enter:'''),
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
    # For plotting graph
        dcc.Graph(figure=fig,
                  id='SIR_curve',
                  animate=False,)

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

def update_figure(country,initial_time,intro_measures,hold_time,relax_time,max_beta,min_beta,gamma_max):
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
        'SIR model for simulatin spread'
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
                         marker_color='aquamarine',
                         name='Confirmed Cases'
                        ))

    fig.add_trace(go.Scatter(x=xdata,
                            y=propagation_rates.infected,
                            mode='lines',
                            marker_color='darkred',
                            name='Simulated curve'))

    fig.update_layout(shapes=[
                            dict(type='rect',xref='x',yref='paper',x0=0,y0=0,x1=t_initial,y1=1,fillcolor="magenta",opacity=0.4,layer="below",line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial,y0=0,x1=t_initial+t_intro_measures,y1=1,fillcolor="magenta",opacity=0.5,layer="below",line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial+t_intro_measures,y0=0,x1=t_initial+t_intro_measures+t_hold,y1=1,fillcolor="magenta",opacity=0.6,layer='below',line_width=0,),
                            dict(type='rect',xref='x',yref='paper',x0=t_initial+t_intro_measures+t_hold,y0=0,x1=t_initial+t_intro_measures+t_hold+t_relax,y1=1,fillcolor='magenta',opacity=0.7,layer='below',line_width=0,)
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

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)
