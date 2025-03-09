# app.py - Main entry point for the Dash application
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from layout import layout
from callbacks import register_callbacks

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SPACELAB], suppress_callback_exceptions=True)
app.title = "ProspectPro"
app.layout = layout

# Register callbacks
register_callbacks(app)

# Expose the Flask server instance
server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
    #app.run_server(debug=True, port=8050)
