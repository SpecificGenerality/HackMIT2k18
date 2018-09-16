import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('data/disasters.csv')
df['text'] = df['state']

for col in df.columns:
  df[col] = df[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
      [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

titleMap = {'Earthquake': 'Earthquakes', 'Fire': 'Forest Fires', 'Hurricane': 'Hurricanes', 'Flood': 'Floods', 'Snow': 'Extreme Snow'}

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
      colorbar = dict(title = titleMap[disaster])
    )],
    layout = dict(
      title = '{} {} by State'.format(year, titleMap[disaster]),
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

  html.Div([
  html.Div([html.H3('Plot 1'),
    html.Div([
      dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(2000, 2019, 1)},
        min=2000,
        max=2018,
        step=1,
        value=2010,
        updatemode='drag'
      ),
    ], style={'margin':15}),

    html.Div(id='updatemode-output-container', style={'margin-top': 30}),

    # Dropdown values correspond to the CSV column name
    dcc.Dropdown(
      id='disaster-dropdown',
      options=[
        {'label': 'Earthquakes', 'value': 'Earthquake'},
        {'label': 'Flood', 'value': 'Flood'},
        {'label': 'Hurricanes', 'value': 'Hurricane'},
        {'label': 'Forest Fires', 'value': 'Fire'},
        {'label': 'Snow', 'value': 'Snow'}
      ],
      value='Earthquake'
    ),
    dcc.Graph(
      id = 'state-choropleth',
      figure = dict(
        data = [dict(
          type='choropleth',
          colorscale = scl,
          autocolorscale = True,
          locations = df['state'],
          z = df['Earthquake'].astype(float),
          locationmode = 'USA-states',
          text = df['text'],
          marker = dict(
            line = dict (
              color = 'rgb(255,255,255)',
              width = 2
            )),
          colorbar = dict(title = "Earthquake")
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
    )], className="six columns"),

    html.Div([html.H3('Plot 2'),
      html.Div([
        dcc.Slider(
          id='slider-updatemode2',
          marks={i: '{}'.format(i) for i in range(2000, 2019, 1)},
          min=2000,
          max=2018,
          step=1,
          value=2010,
          updatemode='drag'
        ),
      ], style={'margin':15}),

      html.Div(id='updatemode-output-container2', style={'margin-top': 30}),

      # Dropdown values correspond to the CSV column name
      dcc.Dropdown(
        id='disaster-dropdown2',
        options=[
          {'label': 'Earthquakes', 'value': 'Earthquake'},
          {'label': 'Flood', 'value': 'Flood'},
          {'label': 'Hurricanes', 'value': 'Hurricane'},
          {'label': 'Forest Fires', 'value': 'Fire'},
          {'label': 'Snow', 'value': 'Snow'}
        ],
        value='Earthquake'
      ),
      dcc.Graph(
        id = 'state-choropleth2',
        figure = dict(
          data = [dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = True,
            locations = df['state'],
            z = df['Earthquake'].astype(float),
            locationmode = 'USA-states',
            text = df['text'],
            marker = dict(
              line = dict (
                color = 'rgb(255,255,255)',
                width = 2
              )),
            colorbar = dict(title = "Earthquake")
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
      )], className="six columns"),
      ])
])

@app.callback(Output('state-choropleth', 'figure'),
              [Input('disaster-dropdown', 'value'), Input('slider-updatemode', 'value')])
def update_graph(disaster, year):
  dff = df[df['fyDeclared'] == str(year)]
  return plotMap(dff, year, disaster)

@app.callback(Output('state-choropleth2', 'figure'),
              [Input('disaster-dropdown2', 'value'), Input('slider-updatemode2', 'value')])
def update_graph(disaster, year):
  dff = df[df['fyDeclared'] == str(year)]
  return plotMap(dff, year, disaster)

if __name__ == '__main__':
  app.run_server(debug=True)