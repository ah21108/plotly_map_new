# import dash
# from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html

app = Dash(meta_tags = 
                [{'name':"viewport", 'content':"width=device-width, initial-scale=1"}])

portnumber=5500

# Can be passed as argument to application, automatically determined, etc.
offline = False

app.css.config.serve_locally = offline
app.scripts.config.serve_locally = offline
app.get_asset_url = '/assets'

#Here we assume that the appropriate topoJson files (world_110m.json, world_50m.json, etc.)
#normally hosted on https://cdn.plot.ly/ are available under ./assets
plotlyConfig = {'topojsonURL':'assets/topojson/'} if offline else {}


data  = [ dict(
        type = 'scattergeo',
        text=['A', 'B', 'C'],
        lon=['-122', '35', '170'],
        lat=['37', '-24', '-37'], 
        mode='markers+text+lines',
        marker=dict(size=5),
        textfont=dict(size=12),
        hoverinfo='none',
) ]

layout = dict(
            width=800, height=400,
            geo = dict(
                projection=dict( type='natural earth' , scale=1),
                framewidth = 1,
                showland = True, showlakes = True, showocean=True, showcountries=True,
                landcolor = 'rgb(204, 204, 204)',
                oceancolor= 'rgb(145, 191, 219)',
                countrycolor = 'rgb(128, 128, 128)',
                lakecolor = 'rgb(145, 191, 219)',
                countrywidth = 0.5,
                subunitwidth = 0.5,
                coastlinewidth = 1,
                resolution = 75,
                center = dict(lat=0,lon=0)
            ),
            showlegend=False,
            margin = dict(l = 0, r = 0, t = 0, b = 0),
        )

fig = dict(data=data, layout=layout)

# gr = dcc.Graph(id='inputMap', config=plotlyConfig, figure = fig)
gr = dcc.Graph(id='inputMap', figure = fig)
app.layout = html.Div(gr)

if __name__ == '__main__':
    app.run_server(debug=False, port=portnumber) 