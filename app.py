import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output


url = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv'
popUrl = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv'
deathUrl = 'https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv'

confirmed_pd = pd.read_csv(url, index_col=False)
population_pd = pd.read_csv(popUrl, index_col=False)
confirmed_pd.columns = confirmed_pd.columns.astype(str)


columns = confirmed_pd.columns

population_pd = population_pd.drop(['County Name','State'], axis=1).reset_index(drop=True)

confirmed_pd = pd.merge(confirmed_pd, population_pd, on=['countyFIPS']).dropna().reset_index(drop=True)

confirmed_pd = confirmed_pd[confirmed_pd['population']!=0]
confirmed_pd = confirmed_pd[confirmed_pd['countyFIPS']>1000].reset_index(drop=True)

FLstate = confirmed_pd.copy()
FLstate = FLstate[FLstate["State"] == 'FL']
FLlocal= FLstate[FLstate["County Name"]=='Santa Rosa County']
FLlocal = FLlocal.reset_index(drop=True)


NYstate = confirmed_pd.copy()
NYstate = NYstate[NYstate["State"] == 'NY']
NYlocal= NYstate[NYstate["County Name"]=='Delaware County']
NYlocal = NYlocal.reset_index(drop=True)



###########################################################
#INICIDENCE RATE FIGURE
###########################################################
x=[]
y1=[]
z1=[]
y2=[]
z2=[]

i=60
while i>0:
    d1 = columns[-i]
    d2 = columns[-(i+14)]

    x.append(d1)
    y1.append((FLlocal[d1].sum() - FLlocal[d2].sum())/FLlocal['population'].sum()*100000)
    z1.append((FLstate[d1].sum() - FLstate[d2].sum())/FLstate['population'].sum()*100000)
    y2.append((NYlocal[d1].sum() - NYlocal[d2].sum())/NYlocal['population'].sum()*100000)
    z2.append((NYstate[d1].sum() - NYstate[d2].sum())/NYstate['population'].sum()*100000)
    i -= 1

LineData = pd.DataFrame(list(zip(x,y1,z1,y2,z2)), columns = ['Dates', 'Santa Rosa', 'Florida', 'Delaware', 'NY']) 
    
fig1 = px.line(LineData, x='Dates', y=['Santa Rosa', 'Florida', 'Delaware', 'NY'], title='Incidence Rate')
fig1.update_xaxes(title_text='Date')
fig1.update_yaxes(showline=True, linecolor='white', title_text='Incidence Rate')
fig1.update_layout(yaxis_showgrid=False, xaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
################################################################    



###########################################################
#ACTIVE CASES FIGURE
###########################################################
x=[]
y=[]

i=60
while i>0:
    d1 = columns[-i]
    d2 = columns[-(i+14)]

    x.append(d1)
    y.append(FLlocal[d1].sum() - FLlocal[d2].sum())
    i -= 1

fig2 = px.bar(x=x, y=y, title='Santa Rosa')
fig2.update_traces(marker_color='#00ff00')
fig2.update_xaxes(showline=True, linecolor='white', title_text='Date')
fig2.update_yaxes(showline=True, linecolor='white', title_text='Active Cases')
fig2.update_layout(height=400,yaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
#############################################################




###########################################################
#ACTIVE CASES FIGURE
###########################################################
x=[]
y=[]

i=60
while i>0:
    d1 = columns[-i]
    d2 = columns[-(i+14)]

    x.append(d1)
    y.append(NYlocal[d1].sum() - NYlocal[d2].sum())
    i -= 1

fig3 = px.bar(x=x, y=y, title='Delaware')
fig3.update_traces(marker_color='#00ff00')
fig3.update_xaxes(showline=True, linecolor='white', title_text='Date')
fig3.update_yaxes(showline=True, linecolor='white', title_text='Active Cases')
fig3.update_layout(height=400,yaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
#############################################################




    
app = dash.Dash(__name__)
server=app.server

##APP LAYOUT
app.layout = html.Div([
    
    html.Div([
        html.Div([
            dcc.Graph(figure=fig1),
        ],className='twelve columns', style={'width':'100%'})
    ],className='row', style={'display':'flex'}),
    
    html.Div([
        html.Div([
            dcc.Graph(figure=fig2),
        ],className='six columns', style={'width':'50%'}),
        html.Div([
            dcc.Graph(figure=fig3),
        ],className='six columns', style={'width':'50%'}),
    ],className='row', style={'display':'flex'}),
    
    html.Div([
        html.Div([
            html.Br(),
            html.H1('Santa Rosa:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(FLlocal[columns[-1]].sum()-FLlocal[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(FLlocal[columns[-1]].sum()-FLlocal[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('          Florida:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(FLstate[columns[-1]].sum()-FLstate[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(FLstate[columns[-1]].sum()-FLstate[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
        ],className='six columns', style={'width':'50%'}),
        html.Div([
            html.Br(),
            html.H1('Delaware:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(NYlocal[columns[-1]].sum()-NYlocal[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(NYlocal[columns[-1]].sum()-NYlocal[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('          New York:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(NYstate[columns[-1]].sum()-NYstate[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(NYstate[columns[-1]].sum()-NYstate[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H2('Last Update: ' + str(columns[-1]),style={'color':'white', 'text-align':'right'}),
        ],className='six columns', style={'width':'50%'}),
    ],className='row', style={'display':'flex'}),
    
    dcc.Interval(
        id='graph-update',
        interval = 100),
    ], className='container', style={'backgroundColor':'#111110'})


if __name__ == '__main__':
    app.run_server(debug=False)
#------------------------------------------------------------------------------
