# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:23:24 2023
@author: g92269
Description: Second iteration of mapping capability with plotly.  Using csv of world airports to plot 'large_airports'

Using hard-copy json and csv files for proof of concept for closed areas.
    
"""
# breakpoint()
import plotly.graph_objects as go
import pandas as pd
# from plotly.Offline import plot
from dash import Dash, dcc, html, dash_table

Portnumber = 8050

# Can be passed as argument to application, automatically determined, etc.
Offline = True

app = Dash()

serve_locally = Offline
app.scripts.config.serve_locally = Offline
app.css.config.serve_locally = Offline
app.get_asset_url = '/assets'
plotlyConfig = {'topojsonURL':'assets/topojson/'} if Offline else {}
df2 = pd.read_csv('assets/airports.csv')
large_airports = df2[df2['type']=='large_airport']
fig = go.Figure()
fig.add_trace(go.Scattergeo(
    lon = large_airports['longitude_deg'],
    lat = large_airports['latitude_deg'],
    text = large_airports['airport_name'],
    # textposition="top center",
    mode = 'markers',
    hovertemplate=
    "Airport Name: %{text}"+
    "<br>Latitude: %{lon:.2f}"+
    "<br>Longitude: %{lat:.2f}",
    marker = dict(
        size = 5,
        color = 'blue', #'rgb(255, 0, 0)',
        line = dict(
            width = 2,
            color = 'rgba(68, 68, 68, 0)'
        )    
    )))
fig.update_layout(
    title_text = 'Major Airports and ICAO Identifiers',
    width=800, 
    height=800,
    showlegend = False,
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = 'rgb(230, 145, 56)',
        lakecolor = 'rgb(0, 255, 255)',
        oceancolor = 'rgb(0, 255, 255)',
        projection = dict(
            type = 'orthographic',
            rotation = dict(
                lon = -50,
                lat = 40,
                roll = 0
            )
        ),
        lonaxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        ),
        lataxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        )
    )
)
gr = dcc.Graph(figure=fig, config=plotlyConfig,)
app.layout = html.Div([ 
    gr,
    dash_table.DataTable(data=large_airports.to_dict('records'), 
                         page_size=50,
                         style_cell={'textAlign': 'left', 'font_size': '8px'})
    ])

if __name__ == '__main__':
    app.run(debug=False, port=Portnumber)
