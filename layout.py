# layout.py - Defines the page layout for the application
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Sidebar navigation
sidebar = html.Div([
    html.H2("Menu", className="display-4"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Player Statistics", href="/player-statistics", active="exact"),
        dbc.NavLink("Charts & Graphs", href="/charts-graphs", active="exact"),
        dbc.NavLink("Compare Players", href="/compare-players", active="exact"),
    ], vertical=True, pills=True, className="nav"),
], style={
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "16rem", "padding": "2rem 1rem", "background-color": "#f8f9fa",
})

# Content container
content = html.Div(id="page-content", style={
    "margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem",
})

# Layout structure
layout = dbc.Container([dcc.Location(id="url"), sidebar, content], className="dbc")


