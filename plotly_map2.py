# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:23:24 2023
@author: g92269
Description: Second iteration of mapping capability with plotly.  
Using csv of world airports to plot 'large_airports'
Using hard-copy json and csv files for proof of concept.
"""
# breakpoint()
import plotly.graph_objects as go
import pandas as pd
# from plotly.OFFLINE import plot
from dash import Dash, dcc, html, dash_table, Input, Output
from plotly_map.tests.math_calcs import haversine

PORTNUMBER = 8050
# Can be passed as argument to application, automatically determined, etc.
OFFLINE = True
app = Dash()

serve_locally = OFFLINE
app.scripts.config.serve_locally = OFFLINE
app.css.config.serve_locally = OFFLINE
app.get_asset_url = '/assets'
plotlyConfig = {'topojsonURL':'assets/topojson/'} if OFFLINE else {}
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
    app.run(debug=False, port=PORTNUMBER)
