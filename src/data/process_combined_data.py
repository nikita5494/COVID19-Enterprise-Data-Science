import pandas as pd
import numpy as np
import requests
import subprocess
import os

from datetime import datetime


def store_relational_JH_data():
    data_path='C:/Users/Nitin/ds-covid19/data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    pd_raw=pd.read_csv(data_path)

    pd_data_base=pd_raw.rename(columns={'Country/Region':'country',
                                   'Province/State':'state'})
    pd_data_base['state']=pd_data_base['state'].fillna('no')
    pd_data_base=pd_data_base.drop(['Lat','Long'],axis=1)


    pd_relational_model=pd_data_base.set_index(['state','country'])\
                                .T                             \
                                .stack(level=[0,1])            \
                                .reset_index()                 \
                                .rename(columns={'level_0':'date',
                                                0:'confirmed'},
                                               )

    pd_relational_model['date']=pd_relational_model.date.astype('datetime64[ns]')

    pd_relational_model.to_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_relational_confirmed.csv',sep=';')
    #print(' Number of rows stored: '+str(pd_relational_model.shape[0]))
    #print(' Latest date is: '+str(max(pd_relational_model.date)))

def store_flat_table_JH_data():
    "process raw JH data into a flat table data structure"
    datapath='C:/Users/Nitin/ds-covid19/data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    JH_data_raw=pd.read_csv(datapath)
    time_index=JH_data_raw.columns[4:]
    pd_flat_table=pd.DataFrame({'date':time_index})
    country_list=JH_data_raw['Country/Region'].unique()
    for country in country_list:
        pd_flat_table[country]=np.array(JH_data_raw[JH_data_raw['Country/Region']==country].iloc[:,4::].sum(axis=0))
    time_index=[datetime.strptime(each,"%m/%d/%y") for each in pd_flat_table.date]
    pd_flat_table['date']=time_index
    pd_flat_table.to_csv('C:/Users/Nitin/ds-covid19/data/processed/COVID_JH_flat_table_confirmed.csv',sep=';',index=False )
    print('Latest date is'+str(max(pd_flat_table.date)))
    print(' Number of rows stored: '+str(pd_flat_table.shape[0]))

if __name__ == '__main__':

    store_relational_JH_data()
    store_flat_table_JH_data()
