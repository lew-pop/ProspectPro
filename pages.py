from dash import Input, Output, dcc, html, dash_table
from data_loader import df
import plotly.express as px
import dash_bootstrap_components as dbc


def get_home_content():
    return html.Div([
        html.Img(
                    src="https://pops-dash.s3.us-west-1.amazonaws.com/app-logo.png", style={"width": "150px", "margin-bottom": "20px", }),
        html.H1("ProspectPro", style={
            "font-size": "2.5rem", "color": "#005a9c", "font-weight": "bold", "margin-bottom": "10px", }),
        html.H2("Welcome to Our Interactive Dashboard", style={
            "font-size": "1.5rem", "color": "#6c757d", "margin-bottom": "20px", }),
        html.P("An interactive tool to analyze player statistics and identify top talent.",
               style={"font-size": "1.1rem", "color": "#495057", "max-width": "800px", "margin": "0 auto", }),
    ],
        style={"text-align": "center", "padding": "40px", }
    )


def get_page1_content():
    return html.Div([
        html.Div(id='hidden-div', style={'display': 'none'}),
        html.Center(html.B(html.H1('Player Statistics')),
                    style={"color": "#005a9c", "font-weight": "bold"}),
        html.Hr(),
        # Create Dash Data Table
        dash_table.DataTable(
            id='datatable-id',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            # Style cell headers
            style_header={
                'padding': '10px',
                'backgroundColor': '#005A9C',
                'color': 'white',
                'font-family': "'Poppins', sans-serif",
                'fontSize': '14px',
                'borderBottom': '3px solid #EF3E42'  # Sleek underline
            },
            # Style cell context
            style_cell={
                'textAlign': 'center',
                'padding': '8px',  # Reduced padding for compactness
                'backgroundColor': '#FAFAFA',  # Soft white for readability
                'color': '#003366',  # Dark blue text for contrast
                'font-family': "'Poppins', sans-serif",
                'fontSize': '13px',
                'border': '1px solid #005A9C'  # Softer border
            },
            # Style data rows
            style_data={
                'backgroundColor': '#FFFFFF',  # White background
                'color': '#000000',  # Dodgers blue text

            },
            # Style selected rows
            style_data_conditional=[
                # Subtle blue for odd rows
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#F0F8FF'},
                {'if': {'row_index': 'even'}, 'backgroundColor': '#FFFFFF'},
                {'if': {'state': 'selected'},
                    'backgroundColor': '#EF3E42', 'color': 'white'},
                {'if': {'state': 'active'}, 'backgroundColor': '#FFC107',
                    'color': '#003366'},  # Soft yellow hover
            ],
            # Data table features
            editable=False,
            sort_action="native",
            sort_mode="multi",
            column_selectable=False,
            row_selectable=False,
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=20,
        ),
        html.Br(),
        html.Hr(),
    ])


def get_page2_content():
    return html.Div([
        html.H1("Charts & Graphs", style={
                'textAlign': 'center', 'color': '#005A9C'}),
        html.Hr(),
        # Histogram of Batting Averages
        dcc.Graph(
            id='batting-avg-histogram',
            figure=px.histogram(df, x='batting_average', nbins=30,
                                title='Distribution of Batting Averages')
        ),
        # Scatter Plot of On-Base Percentage vs. Slugging Percentage
        dcc.Graph(
            id='obp-vs-slugging',
            figure=px.scatter(df, x='on_base_percentage', y='slugging_percentage',
                              title='On-Base Percentage vs. Slugging Percentage',
                              hover_data=['first_name'])
        ),
        # Bar Chart of Top 10 Players by WAR
        dcc.Graph(
            id='top-war-players',
            figure=px.bar(df.nlargest(10, 'wins_above_replacement'),
                          x='first_name', y='wins_above_replacement',
                          title='Top 10 Players by WAR')
        ),
        # Box Plot of ERA by Throwing Hand
        dcc.Graph(
            id='era-by-throwing-hand',
            figure=px.box(df, x='throws', y='earned_run_average',
                          title='ERA by Throwing Hand')
        ),
    ])


def get_page3_content():
    return html.Div([
        html.H1("Compare Players", style={
                'textAlign': 'center', 'color': '#005A9C'}),
        html.Hr(),
        # Dropdowns to select players
        html.Div([
            html.Label("Select Player 1:"),
            dcc.Dropdown(
                id='player1-dropdown',
                options=[{'label': name, 'value': name}
                         for name in df['first_name'].unique()],
                value=df['first_name'].iloc[0]
            ),
            html.Label("Select Player 2:"),
            dcc.Dropdown(
                id='player2-dropdown',
                options=[{'label': name, 'value': name}
                         for name in df['first_name'].unique()],
                value=df['first_name'].iloc[1]
            ),
        ], style={'margin-bottom': '20px'}),
        # Comparison Table
        html.Div(id='comparison-table'),
        # Bar Chart Comparison
        dcc.Graph(id='comparison-bar-chart'),
    ])


def get_page4_content():
    return html.Div(
        [
            # Title with styling
            html.H1("Charts & Graphs",
                    className="text-center mt-4 mb-4",
                    style={"color": "#005A9C", "font-weight": "bold"}),
            # Dropdown Container
            dbc.Container(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Chart & Graph Menu:",
                                className="mb-2",
                                style={"color": "#005A9C"}),
                        dcc.Dropdown(
                            id="chart-selector",
                            options=[
                                {"label": "On-Base vs Slugging Percentage",
                                 "value": "scatter"},
                                {"label": "Top 10 Players by WAR",
                                 "value": "bar"},
                                {"label": "Distribution of Batting Averages",
                                 "value": "histogram"},
                                {"label": "ERA by Throwing Hand", "value": "box"}
                            ],
                            className="w-100",
                            clearable=False
                        )
                    ]),
                    className="shadow-lg border-0 mb-4"  # Added margin-bottom
                ),
                className="py-3",  # Added padding top and bottom
                style={"maxWidth": "80%"}
            ),
            dbc.Container(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Filter by Position:",
                                className="mb-2",
                                style={"color": "#005A9C"}),
                        dcc.Dropdown(
                            id="position-selector",
                            options=[
                                {"label": "All Positions",
                                 "value": "all"},
                                {"label": "Pitcher",
                                 "value": "1"},
                                {"label": "Catcher",
                                 "value": "2"},
                                {"label": "First Base",
                                 "value": "3"},
                                {"label": "Second Base",
                                 "value": "4"},
                                {"label": "Third Base",
                                 "value": "5"},
                                {"label": "Shortstop",
                                 "value": "6"},
                                {"label": "Left Field",
                                 "value": "7"},
                                {"label": "Center Field",
                                 "value": "8"},
                                {"label": "Right Field",
                                 "value": "9"}
                            ],
                            value="all",
                            className="w-100",
                            clearable=False
                        )
                    ]),
                    className="shadow-lg border-0 mb-4",
                    
                ),
                id="position-dropdown-container",
                className="py-3 justify-content-center",  # Added padding top and bottom
                style={"display": "none"}
            ),
            # Chart Container
            dbc.Container(
                dbc.Card(
                    [
                        dbc.CardBody(
                            dbc.Spinner(
                                html.Div([
                                    # Add placeholder message
                                    html.Div(
                                        [
                                            html.I(
                                                className="fas fa-chart-line fa-3x mb-3", style={"color": "#005A9C"}),
                                            html.H4(
                                                "Select a chart type above to begin", className="text-muted"),
                                            html.P("Choose from various visualizations to analyze player statistics",
                                                   className="text-muted small")
                                        ],
                                        id="chart-placeholder",
                                        className="text-center py-5",
                                        style={"display": "block"}
                                    ),
                                    html.Div(
                                        id="tab-content",
                                        className="p-4",
                                        style={"display": "none"}
                                    )
                                ])
                            ),
                            className="bg-white rounded"
                        ),
                    ],
                    className="shadow-lg border rounded w-100",
                    style={"backgroundColor": "#f8f9fa"}
                ),
                className="d-flex justify-content-center",  # Added margin-bottom
                style={"maxWidth": "80%"},
            ),
        ],
        className="container",
        style={"backgroundColor": "#ffffff"}
    )
