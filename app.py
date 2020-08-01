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

confirmed_pd['Population'] = population_pd['population']

confirmed_pd = confirmed_pd[confirmed_pd['Population']!=0].reset_index(drop=True)

state = confirmed_pd.copy()
state = state[state["State"] == 'FL']
local= state[state["County Name"].isin(['Okaloosa County', 'Walton County', 'Santa Rosa County'])]
local = local.reset_index(drop=True)


###########################################################
#NEW CASES FIGURE
###########################################################
x=[]
y=[]

i=60
while i>0:
    d1 = columns[-i]
    d2 = columns[-(i+1)]

    x.append(d1)
    y.append(local[d1].sum() - local[d2].sum())
    i -= 1

fig = px.bar(x=x, y=y, title='Active Cases')
fig.update_traces(marker_color='#00ff00')
fig.update_xaxes(showline=True, linecolor='white', title_text='Date')
fig.update_yaxes(showline=True, linecolor='white', title_text='Active Cases')
fig.update_layout(height=400,yaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
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
    y.append(local[d1].sum() - local[d2].sum())
    i -= 1

fig2 = px.bar(x=x, y=y, title='Active Cases')
fig2.update_traces(marker_color='#00ff00')
fig2.update_xaxes(showline=True, linecolor='white', title_text='Date')
fig2.update_yaxes(showline=True, linecolor='white', title_text='Active Cases')
fig2.update_layout(height=400,yaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
#############################################################



###########################################################
#INICIDENCE RATE FIGURE
###########################################################
x=[]
y=[]
z=[]

i=60
while i>0:
    d1 = columns[-i]
    d2 = columns[-(i+14)]

    x.append(d1)
    y.append((local[d1].sum() - local[d2].sum())/local['Population'].sum()*100000)
    z.append((state[d1].sum() - state[d2].sum())/state['Population'].sum()*100000)
    i -= 1

LineData = pd.DataFrame(list(zip(x,y,z)), columns = ['Dates', 'Local', 'Florida']) 
    
fig3 = px.line(LineData, x='Dates', y=['Local', 'Florida'], title='Incidence Rate')
fig3.update_xaxes(title_text='Date')
fig3.update_yaxes(showline=True, linecolor='white', title_text='Incidence Rate')
fig3.update_layout(height=400,yaxis_showgrid=False, xaxis_showgrid=False, xaxis_tickangle = -45, title_x = 0.4, font={"size":15, "color":"gray"}, plot_bgcolor='#111110', paper_bgcolor='#111110', title_font_color='white')
################################################################    

    
app = dash.Dash(__name__)
server=app.server

##APP LAYOUT
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(figure=fig),
        ],className='six columns', style={'width':'50%'}),
        html.Div([
            dcc.Graph(figure=fig2),
        ],className='six columns', style={'width':'50%'}),
    ],className='row', style={'display':'flex'}),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig3),
        ],className='six columns', style={'width':'60%'}),
        html.Div([
            html.Br(),
            html.H1('Local:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(local[columns[-1]].sum()-local[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(local[columns[-1]].sum()-local[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('          Florida:',style={'color':'white'}),
            html.H1('Active Cases: ' + str(state[columns[-1]].sum()-state[columns[-15]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H1('New Cases: ' + str(state[columns[-1]].sum()-state[columns[-2]].sum()),style={'color':'white', 'text-align':'center'}),
            html.H2('Last Update: ' + str(columns[-1]),style={'color':'white', 'text-align':'right'}),
        ],className='six columns', style={'width':'40%'}),
    ],className='row', style={'display':'flex'}),
    
    dcc.Interval(
        id='graph-update',
        interval = 100),
    ], className='container', style={'backgroundColor':'#111110'})

if __name__ == '__main__':
    app.run_server(debug=False)
#------------------------------------------------------------------------------
