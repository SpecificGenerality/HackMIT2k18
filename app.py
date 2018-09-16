import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.plotly as py

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Change Temp.csv to DisasterDeclarationsSummaries.csv when ready
df = pd.read_csv('data/Temp.csv')
df['text'] = df['state']

for col in df.columns:
  df[col] = df[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
      [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

def plotMap(df, year, disaster):
  return dict(
    data = [dict(
      type='choropleth',
      colorscale = scl,
      autocolorscale = True,
      locations = df['state'],
      z = df[disaster].astype(float),
      locationmode = 'USA-states',
      text = df['text'],
      marker = dict(
        line = dict (
          color = 'rgb(255,255,255)',
          width = 2
        )),
      colorbar = dict(title = "Earthquakes")
    )],
    layout = dict(
      title = '"{}" Earthquakes by State'.format(year),
      geo = dict(
        scope='usa',
        projection=dict( type='albers usa' ),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'
      ),
    )
  )

app.layout = html.Div(children=[
  html.H1(children='Natural Disaster Visualization'),

  html.Div(children='''
    Choose the year and disaster type
  '''),

  dcc.Slider(
    id='slider-updatemode',
    marks={i: '{}'.format(i) for i in range(1990, 2018, 1)},
    min=1990,
    max=2018,
    step=1,
    value=2010,
    updatemode='drag'
  ),

  html.Div(id='updatemode-output-container', style={'margin-top': 20}),

  # Dropdown values correspond to the CSV column name
  dcc.Dropdown(
    id='disaster-dropdown',
    options=[
      {'label': 'Earthquakes', 'value': 'earthquake'},
      {'label': 'Flood', 'value': 'flood'},
      {'label': 'Hurricanes', 'value': 'hurricane'},
      {'label': 'Forest Fires', 'value': 'fire'},
    ],
    value='earthquake'
  ),

  dcc.Graph(
    id = 'state-choropleth',
    figure = dict(
      data = [dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = True,
        locations = df['state'],
        z = df['earthquake'].astype(float),
        locationmode = 'USA-states',
        text = df['text'],
        marker = dict(
          line = dict (
            color = 'rgb(255,255,255)',
            width = 2
          )),
        colorbar = dict(title = "Earthquakes")
      )],
      layout = dict(
        title = '2010 Earthquakes by State',
        geo = dict(
          scope='usa',
          projection=dict( type='albers usa' ),
          showlakes = True,
          lakecolor = 'rgb(255, 255, 255)'
        ),
      )
    )
  )
])

@app.callback(Output('state-choropleth', 'figure'),
              [Input('disaster-dropdown', 'value'), Input('slider-updatemode', 'value')])
def update_graph(disaster, year):
  dff = df[df['fyDeclared'] == str(year)]
  return plotMap(dff, year, disaster)

if __name__ == '__main__':
  app.run_server(debug=True)