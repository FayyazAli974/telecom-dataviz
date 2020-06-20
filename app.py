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
continents = ["All continents", "Asia", "Africa", "Europe", "Northern America", "Latin America and Caribbean", "Oceania"]
statistics = ["Population", "GDP per capita", "% recycling", "Total MSW (Municipal Solid Waste) per capita"]

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
    html.H1(children='Investment in the fight against plastic pollution'),
    html.Div(children='''In which countries should we invest to limit plastic pollution of the oceans?'''),

    html.Div([
        html.Div([
            html.Div([
                html.P('Year', style={"font-weight":"bold"}),
                dcc.Slider(
                    id='year-slider',
                    min=2015,
                    max=2060,
                    value=2015,
                    marks={str(year): str(year) for year in years},
                    step=None
                )],
                style={'width': '80%', 'display': 'inline-block', 'margin-left': '10px'}
            ),
            html.Div([
                html.P('Estimation', style={"font-weight":"bold"}),
                dcc.RadioItems(
                    id='estimation-type',
                    options=[{'label': i, 'value': i} for i in estimations],
                    value='midpoint',
                    labelStyle={'display': 'inline-block'}
                )],
                style={'width': '80%', 'display': 'inline-block', 'margin-left': '10px', "margin-top": "20px"}
            ),
            html.Div([
                html.P('Places', style={"font-weight":"bold"}),
                dcc.RadioItems(
                    id='continent-type',
                    options=[{'label': i, 'value': i} for i in continents],
                    value='All continents',
                    labelStyle={'display': 'block'}
                )],
                style={'width': '80%', 'display': 'inline-block', 'margin-left': '10px', "margin-top": "20px"}
            ),
            html.Div([
                html.P('Country statistics', style={"font-weight":"bold"}),
                dcc.RadioItems(
                    id='stats-type',
                    options=[{'label': i, 'value': i} for i in statistics],
                    value='Population',
                    labelStyle={'display': 'block'}
                )],
                style={'width': '80%', 'display': 'inline-block', 'margin-left': '10px', "margin-top": "20px"}
            )
            ],
            style={'width': '22%', 'margin-top': '20px', 'vertical-align':'top', 'display': 'inline-block'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='map-graph',
                )],
                style={'width': '100%', 'height': '370px', 'margin-top': '0px', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Graph(
                    id='scatter-graph',
                    figure=go.Figure()
                )],
                style={'width': '45%', 'height': '400px', 'margin-top': '0px', 'margin-left': '5%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Graph(
                    id='line-graph',
                    figure=go.Figure()
                )],
                style={'width': '45%', 'height': '400px', 'margin-top': '0px', 'margin-left': '5%', 'display': 'inline-block'}
            )
            ],
            style={'width': '75%', 'margin':'auto', 'margin-top': '20px', 'display': 'inline-block'}
        )
    ])
])

def compute_graph3(df, country):
    print(country)
    if len(country) > 0:
        df_pays = df[df['Country'].isin(country)]
    else:
        df_pays = df
    axe_temp = [2015, 2020, 2040, 2060]
    axe_temp_rev = axe_temp[::-1]

    Scenario_A = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['midpoint-mpw-scenarioA-2020'].to_list()[0], 
                df_pays['midpoint-mpw-scenarioA-2040'].to_list()[0], df_pays['midpoint-mpw-scenarioA-2060'].to_list()[0]]
    Scenario_A_Higher = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['higher-mpw-scenarioA-2020'].to_list()[0], 
                df_pays['higher-mpw-scenarioA-2040'].to_list()[0], df_pays['higher-mpw-scenarioA-2060'].to_list()[0]]
    Scenario_A_Lower = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['lower-mpw-scenarioA-2020'].to_list()[0], 
                df_pays['lower-mpw-scenarioA-2040'].to_list()[0], df_pays['lower-mpw-scenarioA-2060'].to_list()[0]]
    Scenario_A_Lower_rev = Scenario_A_Lower[::-1]
    Scenario_B = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['midpoint-mpw-scenarioB-2020'].to_list()[0], 
                df_pays['midpoint-mpw-scenarioB-2040'].to_list()[0], df_pays['midpoint-mpw-scenarioB-2060'].to_list()[0]]
    Scenario_B_Higher = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['higher-mpw-scenarioB-2020'].to_list()[0], 
                df_pays['higher-mpw-scenarioB-2040'].to_list()[0], df_pays['higher-mpw-scenarioB-2060'].to_list()[0]]
    Scenario_B_Lower = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['lower-mpw-scenarioB-2020'].to_list()[0], 
                df_pays['lower-mpw-scenarioB-2040'].to_list()[0], df_pays['lower-mpw-scenarioB-2060'].to_list()[0]]
    Scenario_B_Lower_rev = Scenario_B_Lower[::-1]
    Scenario_C = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['midpoint-mpw-scenarioC-2020'].to_list()[0], 
                df_pays['midpoint-mpw-scenarioC-2040'].to_list()[0], df_pays['midpoint-mpw-scenarioC-2060'].to_list()[0]]
    Scenario_C_Higher = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['higher-mpw-scenarioC-2020'].to_list()[0], 
                df_pays['higher-mpw-scenarioC-2040'].to_list()[0], df_pays['higher-mpw-scenarioC-2060'].to_list()[0]]
    Scenario_C_Lower = [df_pays['midpoint-mpw-2015'].to_list()[0], df_pays['lower-mpw-scenarioC-2020'].to_list()[0], 
                df_pays['lower-mpw-scenarioC-2040'].to_list()[0], df_pays['lower-mpw-scenarioC-2060'].to_list()[0]]
    Scenario_C_Lower_rev = Scenario_C_Lower[::-1]


    traceA = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_A_Higher+Scenario_A_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario A',
    )
    traceAs = go.Scatter(
        x=axe_temp,
        y=Scenario_A,
        line=dict(color='rgb(0,100,80)'),
        mode='lines',
        name='Scenario A',
    )
    traceB = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_B_Higher+Scenario_B_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(0,176,246,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario B',
    )
    traceBs = go.Scatter(
        x=axe_temp,
        y=Scenario_B,
        line=dict(color='rgb(0,176,246)'),
        mode='lines',
        name='Scenario B',
    )
    traceC = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_C_Higher+Scenario_C_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(231,107,243,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario C',
    )
    traceCs = go.Scatter(
        x=axe_temp,
        y=Scenario_C,
        line=dict(color='rgb(231,107,243)'),
        mode='lines',
        name='Scenario C',
    )
    data_line_graph = [traceA,traceAs,traceB,traceBs,traceC,traceCs]
    layout_line_graph = go.Layout(
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        title={
            'text': 'MPW Evolution for '+ ", ".join(country),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Year",
        yaxis_title="MPW (kg)",
        xaxis=dict(
            gridcolor='rgb(255,255,255)',
            #range=[2015,2060],
            #x = axe_temp,
            type='date',
            showgrid=True,
            showline=False,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='rgb(255,255,255)',
            showgrid=True,
            showline=False,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False
        ),
    )

    return data_line_graph, layout_line_graph



""" INTERACTIONS """
@app.callback(
    [Output('map-graph', 'figure'),
    Output('scatter-graph', 'figure'),
    Output('line-graph', 'figure')],
    [Input('year-slider', 'value'),
     Input('estimation-type', 'value'),
     Input('continent-type', 'value'),
     Input('stats-type', 'value'),
     Input('map-graph', 'clickData'),
     Input('map-graph', 'selectedData'),
     Input('scatter-graph', 'clickData'),
     Input('scatter-graph', 'selectedData')
     ])
def update_figure(selected_year, estimation_type, continent_type, stats_type, click_country, selected_country, click_country2, selected_country2):
    df_filtered = df.copy()
    selected_points = df_filtered.index
    indexes = countries = []

    #print("-------------------------------------------")
    #print("Trigger:", dash.callback_context.triggered)
    if dash.callback_context.triggered and dash.callback_context.triggered[0]["value"] and isinstance(dash.callback_context.triggered[0]["value"], dict):
        selections = dash.callback_context.triggered[0]["value"]
        
        if selections["points"]:
            indexes = []
            countries = []
            for selection in selections["points"]:
                print(selection)
                indexes.append(selection["pointIndex"])
                if selection["text"]:
                    countries.append(selection["text"])
            selected_points = df[df.index.isin(indexes)].index
    
    if continent_type:
        if continent_type == "All continents":
            selected_points = df.index
        else:
            selected_points = df[df["Continent"] == continent_type].index

    # "Population", "GDP per capita", "% recycling", "Total MSP (Municipal Solid Waste) per capita"
    if stats_type:
        if stats_type == "Population":
            col_scatter = df_filtered[str(selected_year) + " Population (x1000 ppl)"]
        elif stats_type == "GDP per capita":
            col_scatter = df_filtered[str(selected_year) + " Per Capita GDP (2016 USD)"]
        elif stats_type == "% recycling":
            col_scatter = 1 - df_filtered["2015 median Mismanaged MSW fraction (%)"]
        elif stats_type == "Total MSW (Municipal Solid Waste) per capita":
            col_scatter = df_filtered["2015 median Per Capita MSW (kg.y-1)"]

    print(countries)
    #print(selected_points)   
    #print(selected_year)
    percent_to_show = estimation_type + "-percent-" + str(selected_year)
    #print(percent_to_show)
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
            x=col_scatter, 
            y=df_filtered['percent']*100, 
            mode='markers',
            text=df['Country']),
            layout = dict(
                title_text='Mismanaged plastic proportion and statistics',
                xaxis_title=stats_type,
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

    print(len(df_filtered.index), len(selected_points))
    data_line_graph, layout_line_graph = compute_graph3(df_filtered[df_filtered.index.isin(selected_points)], countries)
    fig_line = (
        go.Figure(data=data_line_graph, layout=layout_line_graph
        )
    )

    return fig_map, fig_scatter, fig_line


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