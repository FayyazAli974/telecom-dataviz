import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Constants
estimations = ["lower", "midpoint", "higher"]
years = [2015, 2020, 2040, 2060]
previous_click = None

""" DATA LOADING """
# Load and prepare data
df = pd.read_excel("./Data/igr204-data.xlsx")
print(df.shape)
for estimation in estimations:
    df[estimation + "-percent-2015"] = df[estimation + "-mpw-2015"] / df[estimation + "-total-pw-2015"]
    for year in years[1:]:
        df[estimation + "-percent-" + str(year)] = df[estimation + "-mpw-scenarioB-" + str(year)] / df[estimation + "-total-pw-" + str(year)]
df['percent'] = df["midpoint-percent-2015"]


""" LAYOUT """
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Investment in the fight against ocean pollution'),
    html.Div(children='''In which countries should we invest to limit plastic pollution of the oceans?'''),

    html.Div([
        dcc.Graph(
            id='map-graph',
        )],
        style={'width': '45%', 'height': '400px', 'margin-top': '40px', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Graph(
            id='scatter-graph',
            figure=go.Figure()
        )],
        style={'width': '45%', 'height': '400px', 'margin-top': '40px', 'margin-left': '5%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=2015,
                max=2060,
                value=2015,
                marks={str(year): str(year) for year in years},
                step=None
            )],
            style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.RadioItems(
                id='estimation-type',
                options=[{'label': i, 'value': i} for i in estimations],
                value='midpoint',
                labelStyle={'display': 'inline-block'}
            )],
            style={'width': '48%', 'display': 'inline-block', 'margin-left': '20px'}
        )],
        style={'width': '40%', 'margin':'auto', 'margin-top':'40px'}
    ),
])


""" INTERACTIONS """
@app.callback(
    [Output('map-graph', 'figure'),
    Output('scatter-graph', 'figure')],
    [Input('year-slider', 'value'),
     Input('estimation-type', 'value'),
     Input('map-graph', 'clickData'),
     Input('map-graph', 'selectedData'),
     Input('scatter-graph', 'clickData'),
     Input('scatter-graph', 'selectedData')
     ])
def update_figure(selected_year, estimation_type, click_country, selected_country, click_country2, selected_country2):
    df_filtered = df.copy()
    selected_points = df_filtered.index
    #print("-------------------------------------------")
    print("Trigger:", dash.callback_context.triggered)
    if dash.callback_context.triggered and dash.callback_context.triggered[0]["value"] and isinstance(dash.callback_context.triggered[0]["value"], dict):
        selections = dash.callback_context.triggered[0]["value"]
        if selections["points"]:
            indexes = []
            for selection in selections["points"]:
                indexes.append(selection["pointIndex"])
            print(indexes)
            selected_points = df[df.index.isin(indexes)].index



    """if dash.callback_context.triggered and dash.callback_context.triggered[0]["value"] and isinstance(dash.callback_context.triggered[0]["value"], dict):
        selections = dash.callback_context.triggered[0]["value"]
        if selections["points"]:
            indexes = []
            for selection in selections["points"]:
                indexes.append(selection["pointIndex"])
            print(indexes)
            selected_points = df[df.index.isin(indexes)].index"""

    print(selected_points)   

    print(selected_year)
    percent_to_show = estimation_type + "-percent-" + str(selected_year)
    print(percent_to_show)
    df_filtered['percent'] = df_filtered[percent_to_show]

    fig_map = go.Figure(data=go.Choropleth(
            selectedpoints=selected_points,
            locations = df_filtered['ISO code'],
            z = df_filtered['percent']*100,
            text = df_filtered['Country'],
            colorscale = 'Blues',
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = '',
            colorbar_title = '% mismanaged plastic',
        ), layout = dict(
            title_text='Mismanaged plastic proportion by country',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
                ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={"r":0,"t":40,"l":0,"b":0}, 
            height= 350,
        )
    )

    fig_scatter = (
        go.Figure(data=go.Scatter(
            selectedpoints=selected_points,
            x=df_filtered["GDP - per capita"], 
            y=df_filtered['percent']*100, 
            mode='markers'), 
            layout = dict(
                title_text='Mismanaged plastic proportion and statistics',
                xaxis_title='GDP - per capita',
                yaxis_title='% mismanaged plastic',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                    ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin={"r":0,"t":40,"l":0,"b":0}, 
                height= 350,
            )
        )
    )

    return fig_map, fig_scatter


"""
@app.callback(
    [Output('map-graph', 'figure'),
    Output('scatter-graph', 'figure')],
    [Input('map-graph', 'clickData')])
def update_country(selected_country):
    print(selected_country)

    fig_map = go.Figure(data=go.Choropleth(
            locations = df['ISO code'],
            z = df['percent']*100,
            text = df['Country'],
            colorscale = 'Blues',
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = '',
            colorbar_title = '% mismanaged plastic',
        ), layout = dict(
            title_text='Mismanaged plastic proportion by country',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
                ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin={"r":0,"t":40,"l":0,"b":0}, 
            height= 350,
        )
    )

    fig_scatter = (
        go.Figure(data=go.Scatter(
            x=df["GDP - per capita"], 
            y=df['percent']*100, 
            mode='markers'), 
            layout = dict(
                title_text='Mismanaged plastic proportion and statistics',
                xaxis_title='GDP - per capita',
                yaxis_title='% mismanaged plastic',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                    ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin={"r":0,"t":40,"l":0,"b":0}, 
                height= 350,
            )
        )
    )

    return fig_map, fig_scatter

"""

if __name__ == '__main__':
    app.run_server(debug=True)




"""import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range':[2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)"""







"""import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
"""



"""import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')


app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()"""