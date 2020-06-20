import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output


def compute_graph1(df_filtered, selected_points):
    data=go.Choropleth(
            selectedpoints=selected_points,
            locations = df_filtered['ISO code'],
            z = df_filtered['percent']*100,
            text = df_filtered['Country'],
            colorscale = 'balance',
            reversescale=False,
            zmin=100,
            zmid=50,
            zmax=0,
            autocolorscale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = '',
            colorbar_title = '% mismanaged plastic',
            customdata = df_filtered["hover"],
            hovertemplate = "<b>%{customdata[0]} - %{customdata[6]}</b><br /><br />" +
                    "<b>Mismanaged plastic proportion:</b> %{customdata[1]} %<br /><br />" +
                    "<b>Population (%{customdata[6]}):</b> %{customdata[2]} millions<br />" +
                    "<b>GDP per capita (%{customdata[6]}):</b> %{customdata[3]} (2016 USD)<br />" +
                    "<b>% overall recycling (2015):</b> %{customdata[4]} %<br />" +
                    "<b>Total MSW (Municipal Solid Waste) per capita (2015):</b> %{customdata[5]} kg/year<br />",
            hoverlabel = dict(
                bgcolor="white", 
                font_size=12
            )
        )
    layout = dict(
        title_text='Mismanaged plastic proportion by country',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
            ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={"r":0,"t":30,"l":0,"b":0}, 
        height= 380,
    )

    return data, layout


def compute_graph2(df_filtered, selected_points, col_scatter, stats_type):
    data = go.Scatter(
                selectedpoints=selected_points,
                x=col_scatter, 
                y=df_filtered['percent']*100, 
                mode='markers',
                text=df_filtered['Country'],
                marker=dict(
                    color=df_filtered['percent']*100, 
                    colorscale='balance',
                    showscale=True,
                    colorbar_title = '% mismanaged plastic'
                ),
                customdata = df_filtered["hover"],
                hovertemplate = "<b>%{customdata[0]} - %{customdata[6]}</b><br /><br />" +
                    "<b>Mismanaged plastic proportion:</b> %{customdata[1]} %<br /><br />" +
                    "<b>Population (%{customdata[6]}):</b> %{customdata[2]} millions<br />" +
                    "<b>GDP per capita (%{customdata[6]}):</b> %{customdata[3]} (2016 USD)<br />" +
                    "<b>% overall recycling (2015):</b> %{customdata[4]} %<br />" +
                    "<b>Total MSW (Municipal Solid Waste) per capita (2015):</b> %{customdata[5]} kg/year<br />",
                hoverlabel = dict(
                    bgcolor="white", 
                    font_size=12
                )
            )
    layout = dict(
        title_text='Mismanaged plastic proportion and statistics',
        xaxis_title=stats_type,
        yaxis_title='% mismanaged plastic',
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        margin={"r":0,"t":40,"l":0,"b":0},
        height= 360,
        xaxis=dict(
            gridcolor='rgb(255,255,255)',
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

    return data, layout


def compute_graph3(df_input, country):
    if len(country) > 0:
        df_pays = df_input[df_input['Country'].isin(country)]
    else:
        df_pays = df_input
    axe_temp = [2015, 2020, 2040, 2060]
    axe_temp_rev = axe_temp[::-1]

    Scenario_A = [df_pays['midpoint-mpw-2015'].sum(), df_pays['midpoint-mpw-scenarioA-2020'].sum(), 
                df_pays['midpoint-mpw-scenarioA-2040'].sum(), df_pays['midpoint-mpw-scenarioA-2060'].sum()]
    Scenario_A_Higher = [df_pays['midpoint-mpw-2015'].sum(), df_pays['higher-mpw-scenarioA-2020'].sum(), 
                df_pays['higher-mpw-scenarioA-2040'].sum(), df_pays['higher-mpw-scenarioA-2060'].sum()]
    Scenario_A_Lower = [df_pays['midpoint-mpw-2015'].sum(), df_pays['lower-mpw-scenarioA-2020'].sum(), 
                df_pays['lower-mpw-scenarioA-2040'].sum(), df_pays['lower-mpw-scenarioA-2060'].sum()]
    Scenario_A_Lower_rev = Scenario_A_Lower[::-1]
    Scenario_B = [df_pays['midpoint-mpw-2015'].sum(), df_pays['midpoint-mpw-scenarioB-2020'].sum(), 
                df_pays['midpoint-mpw-scenarioB-2040'].sum(), df_pays['midpoint-mpw-scenarioB-2060'].sum()]
    Scenario_B_Higher = [df_pays['midpoint-mpw-2015'].sum(), df_pays['higher-mpw-scenarioB-2020'].sum(), 
                df_pays['higher-mpw-scenarioB-2040'].sum(), df_pays['higher-mpw-scenarioB-2060'].sum()]
    Scenario_B_Lower = [df_pays['midpoint-mpw-2015'].sum(), df_pays['lower-mpw-scenarioB-2020'].sum(), 
                df_pays['lower-mpw-scenarioB-2040'].sum(), df_pays['lower-mpw-scenarioB-2060'].sum()]
    Scenario_B_Lower_rev = Scenario_B_Lower[::-1]
    Scenario_C = [df_pays['midpoint-mpw-2015'].sum(), df_pays['midpoint-mpw-scenarioC-2020'].sum(), 
                df_pays['midpoint-mpw-scenarioC-2040'].sum(), df_pays['midpoint-mpw-scenarioC-2060'].sum()]
    Scenario_C_Higher = [df_pays['midpoint-mpw-2015'].sum(), df_pays['higher-mpw-scenarioC-2020'].sum(), 
                df_pays['higher-mpw-scenarioC-2040'].sum(), df_pays['higher-mpw-scenarioC-2060'].sum()]
    Scenario_C_Lower = [df_pays['midpoint-mpw-2015'].sum(), df_pays['lower-mpw-scenarioC-2020'].sum(), 
                df_pays['lower-mpw-scenarioC-2040'].sum(), df_pays['lower-mpw-scenarioC-2060'].sum()]
    Scenario_C_Lower_rev = Scenario_C_Lower[::-1]

    traceA = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_A_Higher+Scenario_A_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(134, 42, 92, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario A'
    )
    traceAs = go.Scatter(
        x=axe_temp,
        y=Scenario_A,
        line=dict(color='rgb(134, 42, 92)'),
        mode='lines',
        name='Scenario A',
    )
    traceB = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_B_Higher+Scenario_B_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(251, 120, 19, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario B',
    )
    traceBs = go.Scatter(
        x=axe_temp,
        y=Scenario_B,
        line=dict(color='rgb(251, 120, 19)'),
        mode='lines',
        name='Scenario B',
    )
    traceC = go.Scatter(
        x=axe_temp+axe_temp_rev,
        y=Scenario_C_Higher+Scenario_C_Lower_rev,
        fill='tozerox',
        fillcolor='rgba(33, 140, 116, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        name='Scenario C',
    )
    traceCs = go.Scatter(
        x=axe_temp,
        y=Scenario_C,
        line=dict(color='rgb(33, 140, 116)'),
        mode='lines',
        name='Scenario C',
    )
    data_line_graph = [traceA,traceAs,traceB,traceBs,traceC,traceCs]
    layout_line_graph = go.Layout(
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        margin={"r":0,"t":40,"l":0,"b":0}, 
        height= 360,
        title_text='Mismanaged plastic evolution',
        xaxis_title="Year",
        yaxis_title="MPW (kg)",
        xaxis=dict(
            gridcolor='rgb(255,255,255)',
            type='date',
            showgrid=True,
            showline=False,
            showticklabels=True,
            tickcolor='rgb(127,127,127)',
            ticks='outside',
            zeroline=False,
            tickmode = 'array',
            tickvals = axe_temp,
            ticktext = ["2015", "2020", "2040", "2060"]
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