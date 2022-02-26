


import pandas as pd
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a7e2dbc442da45a142f2887478f9cf4fae1edd13/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths ='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a7e2dbc442da45a142f2887478f9cf4fae1edd13/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a7e2dbc442da45a142f2887478f9cf4fae1edd13/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date1,var_name='date',value_name='confirmed')

death = pd.read_csv(url_deaths)
date2 = death.columns[4:]
total_death  = death.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date2,var_name='date',value_name='death')

recovered = pd.read_csv(url_recovered)
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_vars=date3,var_name='date',value_name='recovered')

covid_data = total_confirmed.merge(right=total_death,how ='left',on= ['Province/State','Country/Region','Lat','Long','date'])
covid_data = covid_data.merge(right=total_recovered,how='left',on=['Province/State','Country/Region','Lat','Long','date'])

#Changing the time value
covid_data['date']=pd.to_datetime(covid_data['date'])
#Filling Nan Values
covid_data['recovered'] = covid_data.recovered.fillna(0)
#Create column Active Patients
covid_data["active"] = covid_data['confirmed']-covid_data['death'] - covid_data['recovered'] 
#Grouping Data Global
covid_data_global = covid_data.groupby(["date"])[['confirmed','death','recovered','active']].sum().reset_index()
#covid_data_global.to_csv("Global_Data.csv")

#covid_data.to_csv("assets/covid.csv",index=False)

df = pd.read_csv("assets/Indexed.csv")
#print(df.columns.unique())

#Finding  Total cases
total_death= df["death"].sum()
total_death = round(total_death.astype(float)/1000000000,2)
total_death = total_death.astype(str)+"Billion"

total_recovered=df["recovered"].sum()
total_recovered = round(total_recovered.astype(float)/1000000000,2)
total_recovered = total_recovered.astype(str)+"Billion"

total_confirmed=df["confirmed"].sum()
total_confirmed = round(total_confirmed.astype(float)/1000000000,2)
total_confirmed = total_confirmed.astype(str)+"Billion"



from dash import Dash, Input, Output, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import gunicorn 


#df = covid_data

    

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],)
server=app.server
        
# Layout Section: BOOTSTRAP
card_recovered = [
    dbc.CardHeader("Total Recovered"),
    dbc.CardBody(
        [
            html.H5( total_recovered, className="card-title"),
            html.P(
                "This much people were recovered till now",
                className="card-text",
            ),
        ]
    ),
]

card_death = [
    dbc.CardHeader("Total Death"),
    dbc.CardBody(
        [
            html.H5( total_death, className="card-title"),
            html.P(
                "Unfortunately this much people were Dead till now",
                className="card-text",
            ),
        ]
    ),
]

card_confirmed = [
    dbc.CardHeader("Total Confirmed"),
    dbc.CardBody(
        [
            html.H5( total_confirmed, className="card-title"),
            html.P(
                "This much people were confirmed as having corona",
                className="card-text",
            ),
        ]
    ),
]


app.layout = html.Div([
    dbc.Row([ (html.H1("Covid Data Dashboard",
        className='text-center font-weight-bold text-success'))
         
             

    ]),

    

    dbc.Row([ 
        dbc.Col([
            (html.H3("Deaths",
        className='text-center  text-danger')),
            dcc.Dropdown(id='my-dpdn',multi=False,value='India',
                    options=[{'label':x,'value':x}
                            for x in sorted(df['Country/Region'].unique())]),
            dcc.Graph(id='line-fig',figure={})
        
        ]),

        
        dbc.Col([
            (html.H3("Recovered",
        className='text-center  text-success')),
            dcc.Dropdown(id='my-dpdn2',multi=True,value=['India','Australia'],
                    options=[{'label':x,'value':x}
                            for x in sorted(df['Country/Region'].unique())]),
            dcc.Graph(id='line-fig2',figure={})

        
        ])

        


    
    
    
    ]),

    


    dbc.Row([ 
         dbc.Col(dbc.Card(card_recovered,color="success",inverse=True)),

            
        
        dbc.Col(dbc.Card(card_confirmed,color="warning",inverse=True)),

        dbc.Col(dbc.Card(card_death,color="danger",inverse=True)),


        



        


    ])


]) 

#Callback

@app.callback(
    Output('line-fig','figure'),
    Input('my-dpdn','value')
)

def update_graph(country_selected):
    dff = df[df['Country/Region'] == country_selected ]
    figln = px.line(dff, x='date',y='death')
    return figln

#Histogram
@app.callback(
    Output('line-fig2','figure'),
    Input('my-dpdn2','value')
)
def update_graph(country_selected):
    dff = df[df['Country/Region'].isin(country_selected)]
    figln2 = px.line(dff,x='date',y='confirmed',color='Country/Region')
    return figln2






if __name__=='__main__':
    app.run_server(debug=True)




#By Immanuel




        

        

    






  


