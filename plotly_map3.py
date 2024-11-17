# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:23:24 2023
@author: g92269
Description: Second iteration of mapping capability with 
plotly.  Using csv of world airports to plot 'large_airports'

Using hard-copy json and csv files for proof of concept for 
closed areas.    
"""
import plotly.graph_objects as go
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from dash import Dash, dcc, html, dash_table, callback, Input, Output

def haversine(lon1, lat1, lon2=45, lat2=45):
    '''
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    Taken from https://stackoverflow.com/questions/4913349/haversine-formula-in-p
    ython-bearing-and-distance-between-two-gps-points
    Verified against https://www.omnicalculator.com/math/great-circle to within 
    0.1 km across random values pos and neg lat/long.

    inputs:
    ----------
    lon1: float, range[-180, 180].  Longitude of point 1
    lat1: float, range[-90, 90].    Latitude of point 1
    lon2: float, range[-180, 180].  Longitude of point 2
    lat2: float, range[-90, 90].    Latitude of point 2

    outputs:
    ----------
    distance between point 1 and point 2 in km.

    '''

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

'''
Launches a Dash app with map representation of world airports and source dataframe.
Dash checklist at top allows user to enable/disable display of airport categories

Parameters
----------
portnumber : defined portnumber where app can be viewed in browser via localhost
Offline : (bool) Whether app will use local json files for map or plotly-web-hosted ones
serve_locally : base dataframe
app.scripts.config.serve_locally : whether to use local script config
app.css.config.serve_locally : whether to use local css config
app.get_asset_url : location of locally run assets (do not modify)
plotlyConfig : customized url to pull topojson if Offline (do not modify)
df2 : base dataframe from input csv

Returns
-------
Dash app
'''


Offline = False # Can be passed as argument to application.
app = Dash()
serve_locally = Offline
app.scripts.config.serve_locally = Offline
app.css.config.serve_locally = Offline
app.get_asset_url = '/assets'
plotlyConfig = {'topojsonURL':'assets/topojson/'} if Offline else {}
selected_columns=['type','airport_name','latitude_deg','longitude_deg','iso_country']
df2 = pd.read_csv('assets/airports.csv', usecols=selected_columns)
df2['gc_distance'] = df2.apply(lambda x: haversine(x['longitude_deg'],x['latitude_deg'], 45, 45), axis=1)
color_map = {
            'balloonport'   :'red',
            'closed'        :'gray',
            'heliport'      :'white',
            'large_airport' :'black',
            'medium_airport':'blue',
            'seaplane_base' :'green',
            'small_airport' :'yellow'
            }
shape_map = {
            'balloonport'   :'triangle-up',
            'closed'        :'hash',
            'heliport'      :'triangle-down',
            'large_airport' :'circle',
            'medium_airport':'square',
            'seaplane_base' :'cross',
            'small_airport' :'diamond'
            }
df2['ap_color'] = df2.type.map(color_map)
df2['shape'] = df2.type.map(shape_map)
airport_types = df2['type'].sort_values().unique()
app.layout = html.Div(
    [
        html.Div(children="Airport Types",
                 style={'fontSize': 16}),

        dcc.Checklist(options=airport_types, #uses list of unique airport types from df
                      value=['large_airport'], # default value--ensure it is set as a list
                      id="airport_clist",
                      persistence=True,
                      persistence_type='session',
                      style={'fontSize': 16}
                      ),
        dcc.Graph(id='airport_graph'),
        dash_table.DataTable(df2.to_dict('records'),
                             filter_action='native',
                             columns=[{'name': i, 'id': i} for i in selected_columns],                             
                             id='dataframe',
                             page_size=50,                              
                             style_cell={'textAlign': 'left', 'font_size': '12px'},
                             editable=False)                            
                             
    ]
)
@app.callback(
    Output('airport_graph', 'figure'),
     # Output('dataframe', 'data')],
    Input('airport_clist', 'value')
)
def update_airport_graph(chosen_airport_type):
    '''
    Modifies the go.Figure based on the callback selector to enable/disable
    airport types from the figure.

    Inputs
    ----------
    chosen_airport_type : list set by checkbox; defaults to 'large_airport'

    Parameters
    ----------
    df2 : base dataframe
    chosen_airport_type: list of strings based on dcc.Checklist inputs above

    Returns
    -------
    go.Figure
    '''

    df = df2.loc[(df2['type'].isin(chosen_airport_type))]
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon = df['longitude_deg'],
        lat = df['latitude_deg'],
        text = df['gc_distance'],
        # textposition="top center",
        mode = 'markers',
        hovertemplate=
            "GC Distance: %{text:.1f} km"+
            "<br>Latitude: %{lon:.2f}"+
            "<br>Longitude: %{lat:.2f}",
        marker = dict(
            symbol=df['shape'],
            size = 5,
            color = df['ap_color'],#'blue', #'rgb(255, 0, 0)',
            line = dict(
                width = 2,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))
    fig.update_layout(
        title_text='World Airports',
        width=800,
        height=800,
        showlegend=False,
        geo=dict(
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.5,
            landcolor='rgb(230, 145, 56)',
            lakecolor='rgb(0, 255, 255)',
            oceancolor='rgb(0, 255, 255)',
            projection=dict(
                type='orthographic',
                rotation=dict(
                    lon=-50,
                    lat=40,
                    roll=0
                )
            ),
            lonaxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            ),
            lataxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)',
                gridwidth=0.5
            )
        )
    )
    return fig

if __name__ == '__main__':
    portnumber = 8050
    app.run(debug=False, port=portnumber)
    

