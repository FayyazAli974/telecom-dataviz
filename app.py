import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from compute_graph import compute_graph1, compute_graph2, compute_graph3

# Constants
estimations = ["lower", "midpoint", "higher"]
scenarios = ["Scenario A", "Scenario B", "Scenario C"]
years = [2015, 2020, 2040, 2060]
previous_click = None
continents = ["All continents", "Asia", "Africa", "Europe", "Northern America", "Latin America and Caribbean", "Oceania"]
statistics = ["Population", "GDP per capita", "% recycling", "Total MSW (Municipal Solid Waste) per capita"]


""" DATA LOADING """
# Load and prepare data
df = pd.read_excel("./Data/igr204-data.xlsx")
for estimation in estimations:
    df[estimation + "-percent-2015"] = df[estimation + "-mpw-2015"] / df[estimation + "-total-pw-2015"]
    for scenario in scenarios:
        for year in years[1:]:
            df[estimation + "-scenario" + scenario[-1] + "-percent-" + str(year)] = df[estimation + "-mpw-scenario" + scenario[-1] + "-" + str(year)] / df[estimation + "-total-pw-" + str(year)]
            
df['percent'] = df["midpoint-percent-2015"]

print(df.columns)

""" LAYOUT """
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([
            html.H1(children='Investment in the fight against plastic pollution', style={'margin-bottom': '10px'}),
            html.Div(children='''In which countries should we invest to limit plastic pollution of the oceans?'''),
        ],
        style={'margin-bottom': '30px', 'margin-left': '10px'}
    ),
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
                html.P('Scenarios', style={"font-weight":"bold"}),
                dcc.RadioItems(
                    id='scenario-type',
                    options=[{'label': i, 'value': i} for i in scenarios],
                    value='Scenario B',
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
            ),
             html.Div([
                html.P('Scenario details', style={"font-weight":"bold"}),
                html.P('• Scenario A: Business as usual', style={"margin-bottom": "0"}),
                html.P('• Scenario B: Improve waste management', style={"margin-bottom": "0"}),
                html.P('• Scenario C: Reduce plastic use and improve waste management', style={"margin-bottom": "0"}),
                html.P('Data source: Study \'Future scenarios of global plastic waste generation and disposal\', Laurent Lebreton and Anthony Andrady (2019) for The Ocean Cleanup', \
                    style={"margin-top": "20px", "font-size": "11px"}),
                ],
                style={'width': '80%', 'display': 'inline-block', 'margin-left': '10px', "margin-top": "40px", "border-top": "solid black 1px"}
            )
            ],
            style={'width': '22%', 'margin-top': '20px', 'vertical-align':'top', 'display': 'inline-block'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='map-graph',
                )],
                style={'width': '100%', 'height': '380px', 'margin-top': '0px', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Graph(
                    id='scatter-graph',
                    figure=go.Figure()
                )],
                style={'width': '45%', 'height': '400px', 'margin-top': '10px', 'margin-left': '5%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Graph(
                    id='line-graph',
                    figure=go.Figure()
                )],
                style={'width': '45%', 'height': '400px', 'margin-top': '10px', 'margin-left': '5%', 'display': 'inline-block'}
            )
            ],
            style={'width': '75%', 'margin':'auto', 'margin-top': '10px', 'display': 'inline-block'}
        )
    ])
])



""" INTERACTIONS """
@app.callback(
    [Output('map-graph', 'figure'),
    Output('scatter-graph', 'figure'),
    Output('line-graph', 'figure')],
    [Input('year-slider', 'value'),
     Input('scenario-type', 'value'),
     Input('continent-type', 'value'),
     Input('stats-type', 'value'),
     Input('map-graph', 'clickData'),
     Input('map-graph', 'selectedData'),
     Input('scatter-graph', 'clickData'),
     Input('scatter-graph', 'selectedData')
     ])
def update_figure(selected_year, scenario_type, continent_type, stats_type, click_country, selected_country, click_country2, selected_country2):
    df_filtered = df.copy()
    selected_points = df_filtered.index
    indexes = countries = []
    trigger = None

    if dash.callback_context.triggered:
        trigger = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    # If we select a country on the map
    if trigger == "map-graph" or trigger == "scatter-graph":
        if dash.callback_context.triggered and dash.callback_context.triggered[0]["value"] and isinstance(dash.callback_context.triggered[0]["value"], dict):
            selections = dash.callback_context.triggered[0]["value"]
            
            if selections["points"]:
                indexes = []
                countries = []
                for selection in selections["points"]:
                    indexes.append(selection["pointIndex"])
                    if selection["text"]:
                        countries.append(selection["text"])
                selected_points = df[df.index.isin(indexes)].index
    else:        
        if continent_type:
            if continent_type == "All continents":
                selected_points = selected_points
            else:
                selected_points = df[df["Continent"] == continent_type].index

    # statistics
    if stats_type:
        if stats_type == "Population":
            col_scatter = df_filtered[str(selected_year) + " Population (x1000 ppl)"]
        elif stats_type == "GDP per capita":
            col_scatter = df_filtered[str(selected_year) + " Per Capita GDP (2016 USD)"]
        elif stats_type == "% recycling":
            col_scatter = 1 - df_filtered["2015 median Mismanaged MSW fraction (%)"]
        elif stats_type == "Total MSW (Municipal Solid Waste) per capita":
            col_scatter = df_filtered["2015 median Per Capita MSW (kg.y-1)"]

    
    # data to show
    if selected_year == 2015:
        percent_to_show = "midpoint-percent-" + str(selected_year)
    else:
        percent_to_show = "midpoint-scenario" + scenario_type[-1] + "-percent-" + str(selected_year)
    df_filtered['percent'] = df_filtered[percent_to_show]

    print(percent_to_show)

    # hover
    df_filtered["hover"] = df_filtered.apply(lambda x: (x["Country"], round(x['percent']*100,2), x[str(selected_year) + " Population (x1000 ppl)"]/1000, \
                                    int(x[str(selected_year) + " Per Capita GDP (2016 USD)"]), round(x["2015 median Mismanaged MSW fraction (%)"],2), \
                                    x["2015 median Per Capita MSW (kg.y-1)"], str(selected_year)), axis=1)
   
    
    # Compute the graphics
    data, layout = compute_graph1(df_filtered, selected_points)
    fig_map = (go.Figure(data=data, layout=layout))

    data, layout = compute_graph2(df_filtered, selected_points, col_scatter, stats_type)
    fig_scatter = (go.Figure(data=data, layout=layout))

    data, layout = compute_graph3(df_filtered[df_filtered.index.isin(selected_points)], countries)
    fig_line = (go.Figure(data=data, layout=layout))

    return fig_map, fig_scatter, fig_line


if __name__ == '__main__':
    app.run_server(debug=True)
