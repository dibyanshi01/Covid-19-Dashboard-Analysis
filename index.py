import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from scipy.special import logsumexp

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered= 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

#unpivot data frames

date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars= ['Province/State','Country/Region','Lat','Long'], value_vars=date2, var_name='date', value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars= ['Province/State','Country/Region','Lat','Long'], value_vars=date2, var_name='date', value_name='recovered')

#Merging data frames
covid_data = total_confirmed.merge(right=total_deaths, how = 'left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right=total_recovered, how = 'left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])


#converting date column
covid_data['date'] = pd.to_datetime(covid_data['date'])

#Check missing(NaN) values
covid_data.isna().sum()

#Replace NaN with zero
covid_data['recovered'] = covid_data['recovered'].fillna(0)

#Creating Active column
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

covid_data_1 = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

#Create dictionary of list
covid_data_list= covid_data[['Country/Region','Lat', 'Long']]
dict_of_locations=covid_data_list.set_index('Country/Region')[['Lat', 'Long']].T.to_dict('dict')

app = dash.Dash(__name__, meta_tags=[{"name": "viewport"}] )

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('coronavirus.jpg'),
                     id = 'corona-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'})


        ],className='one-third column'),

        html.Div([
            html.Div([
                html.H3('Covid - 19', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Track Covid - 19 Cases', style={'margin-bottom': '0px', 'color': 'white'})
            ])
        ], className='one-half column', id= 'title'),

        html.Div([
            html.H6('Last Updated: ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')),
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')



    ], id = 'header', className= 'row flex-display',style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
            html.H6(children='Global Cases',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['confirmed'].iloc[-1]:,.0f}",
                       style={'textAlign': 'center',
                           'color': 'orange',
                              'fontSize': 40}),
            html.P('new:' + f"{covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) / covid_data_1['confirmed'].iloc[-1]) * 100, 2)) + '%)',

                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 15,
                           'margin-top': '-18px'})


        ], className='card_container four columns'),

html.Div([
            html.H6(children='Global Deaths',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['death'].iloc[-1]:,.0f}",
                       style={'textAlign': 'center',
                           'color': '#dd1e35',
                              'fontSize': 40}),
            html.P('new:' + f"{covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['death'].iloc[-1] - covid_data_1['death'].iloc[-2]) / covid_data_1['death'].iloc[-1]) * 100, 2)) + '%)',

                    style={'textAlign': 'center',
                           'color': '#dd1e35',
                           'fontSize': 15,
                           'margin-top': '-18px'})


        ], className='card_container four columns'),

html.Div([
            html.H6(children='Global Active',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{covid_data_1['active'].iloc[-1]:,.0f}",
                       style={'textAlign': 'center',
                           'color': 'green',
                              'fontSize': 40}),
            html.P('new:' + f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) / covid_data_1['active'].iloc[-1]) * 100, 2)) + '%)',

                    style={'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 15,
                           'margin-top': '-18px'})

        ], className='card_container four columns'),

    ], className='row flex display'),

   html.Div([
           html.Div([
               html.P('Select Country:', className='fix_label', style={'color': 'white'}),
               dcc.Dropdown(id='w_countries',
                            multi=False,
                            searchable=True,
                            value='US',
                            placeholder='Select Countries',
                            options=[{'label': c, 'value': c}
                                     for c in (covid_data['Country/Region'].unique())], className='dcc_compon', style={'width': '200px', 'color':'#1f2c56'}),

               html.P('New Cases: ' + ' ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')),
                      className='fix_label', style={'text-align': 'center', 'color': 'white'}),
               dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc.compon',
                         style={'margin-top': '20px'}),
               dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc.compon',
                         style={'margin-top': '20px'}),
               # dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc.compon',
               #           style={'margin-top': '20px'}),
               dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc.compon',
                         style={'margin-top': '20px'})

           ], className='create_container three column', style={'width':'250px'}),
       html.Div([
           dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'}, className='dcc.compon',
                     style={'margin-top': '20px'})
       ], className='create_container four column', style={'width':'320px'}),

       html.Div([
           dcc.Graph(id='line_chart', config={'displayModeBar': 'hover'}, className='dcc.compon',
                     style={'margin-top': '20px'})
       ], className='create_container five column', style={'width':'450px'})

       ], className='row flex display'),

    html.Div([
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'}, className='dcc.compon',
                      style={'margin-top': '20px'})
        ], className='create_container1 twelve column')
    ], className='row flex display')





], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('confirmed', 'figure'),
              [Input('w_countries','value')])

def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-3]
    return{
        'data': [go.Indicator(
             mode='number+delta',
             value=value_confirmed,
             delta={'reference': delta_confirmed,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 15}},
             number={'valueformat': ',',
                     'font': {'size': 20}},
             domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )


    }

@app.callback(Output('death', 'figure'),
              [Input('w_countries','value')])

def update_death(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2]
    delta_death = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-3]
    return{
        'data': [go.Indicator(
             mode='number+delta',
             value=value_death,
             delta={'reference': delta_death,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 15}},
             number={'valueformat': ',',
                     'font': {'size': 20}},
             domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'Death',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#dd1e35'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )


    }
# @app.callback(Output('recovered', 'figure'),
#               [Input('w_countries','value')])
#
# def update_recovered(w_countries):
#     covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
#     value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
#     delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]
#     return{
#         'data': [go.Indicator(
#              mode='number+delta',
#              value=value_recovered,
#              delta={'reference': delta_recovered,
#                     'position': 'right',
#                     'valueformat': ',g',
#                     'relative': False,
#                     'font': {'size': 15}},
#              number={'valueformat': ',',
#                      'font': {'size': 20}},
#              domain={'y': [0, 1], 'x': [0, 1]}
#         )],
#
#         'layout': go.Layout(
#             title={'text': 'Recovered',
#                    'y': 1,
#                    'x': 0.5,
#                    'xanchor': 'center',
#                    'yanchor': 'top'},
#             font=dict(color='#dd1e35'),
#             paper_bgcolor='#1f2c56',
#             plot_bgcolor='#1f2c56',
#             height = 50,
#         )
#     }
@app.callback(Output('active', 'figure'),
              [Input('w_countries','value')])

def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]
    return{
        'data': [go.Indicator(
             mode='number+delta',
             value=value_active,
             delta={'reference': delta_active,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 15}},
             number={'valueformat': ',',
                     'font': {'size': 20}},
             domain={'y': [0, 1], 'x': [0, 1]}
        )],

        'layout': go.Layout(
            title={'text': 'Active',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='#e55467'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 50,

        )


    }


@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries','value')])

def update_graph(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    death_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['death'].iloc[-1]
    recovered_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    active_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    colors = ['orange', '#dd1e35', 'green', '#e55467']
    return{
        'data': [go.Pie(
            labels=['Confirmed', 'Death', 'Recovered', 'Active'],
            values=[confirmed_value, death_value, recovered_value, active_value],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=45,


        )],

        'layout': go.Layout(
            title={'text': 'Toatal Cases: ' + (w_countries),
                   'y': 0.97,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7
            }


        )


    }


@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_chart(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][['Country/Region', 'confirmed', 'date']].reset_index()
    covid_data_3['daily confirmed']= covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()
    return {
        'data': [go.Bar(
            x=covid_data_3['date'].tail(30),
            y=covid_data_3['daily confirmed'].tail(30),
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '</b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '</b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            '</b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'


        ),
            go.Scatter(
                x=covid_data_3['date'].tail(30),
                y=covid_data_3['Rolling Ave.'].tail(30),
                name='Rolling Average of the last 7 days - daily confirmed cases',
                line=dict(width=3, color='#FF00FF'),
                marker=dict(color='orange'),
                hoverinfo='text',
                hovertext=
                '</b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
                '</b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in
                                                     covid_data_3['Rolling Ave.'].tail(30)] + '<br>'

            )
        ],

        'layout': go.Layout(
            title={'text': 'Last 30 days Cases: ' + (w_countries),
                   'y': 0.97,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7
                    },
            margin=dict(r=0),

            xaxis=dict(title='<b>Date</b>',
                       color='white',
                       showline= True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=2,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )
                       )

        )

    }

@app.callback(Output('map_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_map(w_countries):

    covid_data_4 = covid_data.groupby(['Lat', 'Long', 'Country/Region'])[['confirmed', 'death', 'recovered', 'active']].max().reset_index()
    covid_data_5 = covid_data_4[covid_data_4['Country/Region'] == w_countries]

    if w_countries:
        zoom=2
        zoom_lat= dict_of_locations[w_countries]['Lat']
        zoom_long = dict_of_locations[w_countries]['Long']

    return {
        'data': [go.Scattermapbox(
            lon=covid_data_5['Long'],
            lat=covid_data_5['Lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=covid_data_5['confirmed'] / 1500,
                                           color=covid_data_5['confirmed'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '</b>Country</b>: ' + covid_data_5['Country/Region'].astype(str) + '<br>' +
            '</b>Longitude</b>: ' + covid_data_5['Long'].astype(str) + '<br>' +
            '</b>Latitude</b>: ' + covid_data_5['Lat'].astype(str) + '<br>' +
            '</b>Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_5['confirmed']] + '<br>' +
            '</b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_5['death']] + '<br>' +
            '</b>Recovered</b>: ' + [f'{x:,.0f}' for x in covid_data_5['recovered']] + '<br>' +
            '</b>Active</b>: ' + [f'{x:,.0f}' for x in covid_data_5['active']] + '<br>'


        ),],

        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            margin=dict(r=0, l=0, b=0, t=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiZGV2cGFybWFyIiwiYSI6ImNrdHl1dHNhYjBlMmEycG93dTUyZ21qc2wifQ.JuZg8rZjnyUFaKtJb2oiNQ',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
            autosize=True

        )

    }


if __name__ =='__main__':
    app.run_server(debug=True)