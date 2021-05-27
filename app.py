# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 23:32:50 2021

@author: Samuil
"""
#import os
#####os.chdir(r"c:/acc/choosebankproject")  
#os.getcwd()

import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
#import plotly.express as px
#import dash_table as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc


###########coef block
A0=20   #size
A1=300
AK=1
B0=0.7       #UAH-0 FX-1 
B1=1
BK=1
C0=0        #0 doesnot need loan 
C1=100
CK=0.5
D0=0        #0-cautiоn 1-greed
D1=1
DK=1
##########

k=pd.read_excel(r'coefficients.xlsx', index_col=0)
key = pd.read_excel(r'keyshort.xlsx')
key.columns=['CODE', 'DT', 'NKB', 'LONG', 'GRUPA','STAN', 'SHORT', 'GRUPAS', 'GRUPASS']
key=key[key.DT==max(key.DT)]
key=key[['NKB', 'SHORT']]
k=pd.merge(key, k, how="right", on=['NKB'])
#k=k.drop(columns='NKB')
#k=k[['SHORT','dgfk','uahs','irck','n3k' ]]
k['cmik']=0
kin=[150,50,0,0]

def banklist():
    k.cmik=k.bik*(AK*abs(k.dgfk-(kin[0]-A0)/(A1-A0))+BK*abs(k.uahs-(kin[1]/100))+CK*abs(k.irck-(kin[2]-C0)/(C1-C0))+DK*abs(k.n3k-(kin[3]/100)))
    k1=k.sort_values(by=['cmik'], ignore_index=True).head(10)    
    k1=k1[['NKB','SHORT', 'DFOOSU', 'DFOOSF']]
    k1.DFOOSU=round(k1.DFOOSU,1)
    k1.DFOOSF=round(k1.DFOOSF,1)
    k1.columns=['nkb', 'Банк', 'Гривневі депозити, млн грн', 'Валютні депозити, млн грн']
    return k1 

k2=banklist()
nkbi=k2.nkb[0]
#k2.drop(columns='nkb', inplace=True)

######################################
######################################
#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
def generate_table(dataframe, max_rows=7):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

dfoos=pd.read_excel(r'depo.xlsx', index_col=0)

#https://plotly.com/python/multiple-axes/
#https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
def generate_chart(nkbi0,nkbi1,nkbi2):
    kc0=dfoos[dfoos.NKB==nkbi0]
    kc0=pd.merge(key, kc0, how="right", on=['NKB'])
    kc0n=max(kc0.SHORT)
    kc0.drop(columns=['NKB','SHORT'], inplace=True)

    kc1=dfoos[dfoos.NKB==nkbi1]
    kc1=pd.merge(key, kc1, how="right", on=['NKB'])
    kc1n=max(kc1.SHORT)
    kc1.drop(columns=['NKB','SHORT'], inplace=True)

    kc2=dfoos[dfoos.NKB==nkbi2]
    kc2=pd.merge(key, kc2, how="right", on=['NKB'])
    kc2n=max(kc2.SHORT)
    kc2.drop(columns=['NKB','SHORT'], inplace=True)

    fig = make_subplots(rows=3, cols=1, subplot_titles=[kc0n,kc1n,kc2n], 
                        y_title='млрд', row_heights=[500,500,500],
                        vertical_spacing=0.2, horizontal_spacing=0.5, 
                        specs=[[{"secondary_y": True}],
                               [{"secondary_y": True}],
                               [{"secondary_y": True}]])
    # left
    fig.add_trace(
        go.Scatter(x=kc0.DT, y=kc0.DFOOSU, name='грн'),
   #     px.line(x=kc0.DT, y=kc0.DFOOSU),
        row=1, col=1, secondary_y=False)
    
    fig.add_trace(
        go.Scatter(x=kc0.DT, y=kc0.DFOOSD, name="дол"),
        row=1, col=1, secondary_y=True,
    )
    
    # middle
    fig.add_trace(
        go.Scatter(x=kc1.DT, y=kc1.DFOOSU, name="грн"),
        row=2, col=1, secondary_y=False)
    
    fig.add_trace(
        go.Scatter(x=kc1.DT, y=kc1.DFOOSD, name="дол"),
        row=2, col=1, secondary_y=True,
    )
    
    # right
    fig.add_trace(
        go.Scatter(x=kc2.DT, y=kc2.DFOOSU, name="грн"),
        row=3, col=1, secondary_y=False)
    
    fig.add_trace(
        go.Scatter(x=kc2.DT, y=kc2.DFOOSD, name="дол"),
        row=3, col=1, secondary_y=True,
    )
    return fig
    #fig.show()

######################################

di=pd.read_excel(r'ir.xlsx', index_col=0)
di['DFOOSU']=di.ir[di.currency=='UAH']
di['DFOOSD']=di.ir[di.currency=='USD']

def generate_chart_i(nkbi0,nkbi1,nkbi2):
    kc0=di[di.NKB==nkbi0]
    kc0=pd.merge(key, kc0, how="right", on=['NKB'])
    kc0n=max(kc0.SHORT)
    kc0.drop(columns=['NKB','SHORT'], inplace=True)

    kc1=di[di.NKB==nkbi1]
    kc1=pd.merge(key, kc1, how="right", on=['NKB'])
    kc1n=max(kc1.SHORT)
    kc1.drop(columns=['NKB','SHORT'], inplace=True)

    kc2=di[di.NKB==nkbi2]
    kc2=pd.merge(key, kc2, how="right", on=['NKB'])
    kc2n=max(kc2.SHORT)
    kc2.drop(columns=['NKB','SHORT'], inplace=True)

    fig = make_subplots(rows=3, cols=1, subplot_titles=[kc0n,kc1n,kc2n], 
                        y_title='% річних', row_heights=[500,500,500],
                        vertical_spacing=0.2, horizontal_spacing=0.5, 
                        specs=[[{"secondary_y": True}],
                               [{"secondary_y": True}],
                               [{"secondary_y": True}]])
    # left

#    fig.add_trace(px.line(x=kc0.DT, y=kc0.DFOOSU)),
    

    fig.add_trace(go.Scatter(x=kc0.DT, y=kc0.DFOOSU, name='грн', mode='lines'), row=1, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=kc0.DT, y=kc0.DFOOSD, name="дол"),row=1, col=1, secondary_y=True,)
    
    # middle
    fig.add_trace(
        go.Scatter(x=kc1.DT, y=kc1.DFOOSU, name="грн"),
        row=2, col=1, secondary_y=False)
    
    fig.add_trace(
        go.Scatter(x=kc1.DT, y=kc1.DFOOSD, name="дол"),
        row=2, col=1, secondary_y=True,
    )
    
    # right
    fig.add_trace(
        go.Scatter(x=kc2.DT, y=kc2.DFOOSU, name="грн"),
        row=3, col=1, secondary_y=False)
    
    fig.add_trace(
        go.Scatter(x=kc2.DT, y=kc2.DFOOSD, name="дол"),
        row=3, col=1, secondary_y=True,
    )
    return fig
    #fig.show()

######################################


######################################

#import plotly.graph_objects as go
external_stylesheets =  [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([ 
  html.H2('Вибір банку для вкладу'), 
  html.H5('(Перерахунок - останній слайдер)'), 
  dbc.Row([
        dbc.Col(html.Div([
#            html.H3('Column 1'),
            html.Div(id='RS'),
            dcc.Slider(id='SS', min=A0, max=A1, marks={i: '{} тис.'.format(i) for i in range(A0,A1+1,int((A1-A0)/2))}, value=50), 
            html.Div(id='RU'),
            dcc.Slider(id='SU', min=B0*100, max=B1*100, step=(B1-B0)*100/10, value=50), 
            html.Div(id='RC'),
            dcc.Slider(id='SC', min=C0, max=C1, marks={i: '{} тис.'.format(i) for i in range(C0,C1+1,int((C1-C0)/2))}, value=0),
            html.Div(id='RT'),
            dcc.Slider(id='ST', min=D0*100, max=D1*100, value=50), 
            html.H5('Банки, що найкраще відповідають критеріям'),
            html.Table(id='TT'),
#            html.Img(src='274.png'),

            ])),

        dbc.Col(html.Div([
            html.H5('Кошти на рахунках, млрд од. валюти'),
            dcc.Graph(id='GT', style={'width': '60vh', 'height': '90vh'})  
            ])),

        dbc.Col(html.Div([
            html.H5('Ставки за 3-міс. депозитами'),
            dcc.Graph(id='IT', style={'width': '60vh', 'height': '90vh'})  
            ])),

            ])
          ])


@app.callback(
    dash.dependencies.Output('RS', 'children'),
    [dash.dependencies.Input('SS', 'value')])
def update_outputRS(value):
    kin[0]=value
    #k2=k2.to_dict('records')
    return 'Сума вкладу {} тис. грн'.format(value)

@app.callback(
    dash.dependencies.Output('RU', 'children'),
    [dash.dependencies.Input('SU', 'value')])
def update_outputRU(value):
    kin[1]=value
    #k2=banklist()
    return 'Гривня {} %'.format(value), ' <      > Валюта {}%'.format(100-value)

@app.callback(
    dash.dependencies.Output('RC', 'children'),
    [dash.dependencies.Input('SC', 'value')])
def update_outputRC(value):
    kin[2]=value
    #k2=banklist()
    return 'Деколи братиму кредит {} тис. грн'.format(value)

@app.callback(
    dash.dependencies.Output('RT', 'children'),
    dash.dependencies.Output('TT', 'children'),
    dash.dependencies.Output('GT', 'figure'),
    dash.dependencies.Output('IT', 'figure'),
    [dash.dependencies.Input('ST', 'value')])
def update_outputRT(value):
    kin[3]=value
    k2=banklist()
    g2=generate_chart(k2.nkb[0],k2.nkb[1],k2.nkb[2])
    i2=generate_chart_i(k2.nkb[0],k2.nkb[1],k2.nkb[2])
    k2.drop(columns='nkb', inplace=True)
    k2=generate_table(k2)
    return ('Обережність {}%'.format(100-value)+'  Дохідність {}%'.format(value)), k2 , g2 , i2

#print(kin)


if __name__ == '__main__': app.run_server(debug=True)


