# callbacks.py - Handles all application callbacks
from dash import Input, Output, dcc, html, dash_table
from data_loader import df
from pages import get_home_content, get_page1_content, get_page2_content, get_page3_content, get_page4_content

import plotly.express as px
import pandas as pd


def register_callbacks(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return get_home_content()
        elif pathname == "/page-1":
            return get_page1_content()
        elif pathname == "/page-2":
            return get_page4_content()
        elif pathname == "/page-3":
            return get_page3_content()
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ],
                className="p-3 bg-light rounded-3",
            )

    @app.callback(
        [Output('comparison-table', 'children'),
         Output('comparison-bar-chart', 'figure')],
        [Input('player1-dropdown', 'value'),
         Input('player2-dropdown', 'value')]
    )
    def update_comparison(player1, player2):
        player1_data = df[df['first_name'] == player1].iloc[0]
        player2_data = df[df['first_name'] == player2].iloc[0]

        # Create comparison table
        comparison_df = pd.DataFrame({
            'Statistic': ['Batting Average', 'On-Base Percentage', 'Slugging Percentage', 'WAR', 'ERA'],
            player1: [player1_data['batting_average'], player1_data['on_base_percentage'],
                      player1_data['slugging_percentage'], player1_data['wins_above_replacement'],
                      player1_data['earned_run_average']],
            player2: [player2_data['batting_average'], player2_data['on_base_percentage'],
                      player2_data['slugging_percentage'], player2_data['wins_above_replacement'],
                      player2_data['earned_run_average']]
        })

        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in comparison_df.columns],
            data=comparison_df.to_dict('records'),
            style_table={'margin': 'auto'},
            style_cell={'textAlign': 'center'}
        )

        # Create bar chart comparison
        fig = px.bar(comparison_df, x='Statistic', y=[player1, player2], barmode='group',
                     title=f'Comparison between {player1} and {player2}')

        return table, fig

    # Callback to show/hide position dropdown
    @app.callback(
        [Output("position-dropdown-container", "style"),
         Output("position-selector", "value")],
        Input("chart-selector", "value")
    )
    def toggle_position_dropdown(selected_chart):
        """ Show the position dropdown only if 'bar' is selected. """
        if selected_chart == "bar":
            return {"display": "flex"}, "all"
        return {"display": "none"}, "all"

    @app.callback(
        [Output("tab-content", "children"),
         Output("tab-content", "style"),
         Output("chart-placeholder", "style")],
        [Input("chart-selector", "value"),
         Input("position-selector", "value")]
    )
    def render_chart_content(selected_chart, selected_position):
        """
        This callback handles both the chart rendering and the visibility
        of the placeholder/chart content.
        """
        # If no chart is selected, show placeholder and hide content
        if selected_chart is None:
            return None, {"display": "none"}, {"display": "block"}

        # Initialize chart content as None
        chart_content = None

        # Generate the appropriate chart based on selection
        if selected_chart == "histogram":
            chart_content = dcc.Graph(
                id='batting-avg-histogram',
                figure=px.histogram(
                    df, x='batting_average', nbins=30, title='Distribution of Batting Averages')
            )
        elif selected_chart == "scatter":
            chart_content = dcc.Graph(
                id='obp-vs-slugging',
                figure=px.scatter(df, x='on_base_percentage', y='slugging_percentage',
                                  title='On-Base Percentage vs. Slugging Percentage',
                                  hover_data=['player_id', 'first_name', 'last_name', 'position'])
            )
        elif selected_chart == "bar":
            filtered_df = df if selected_position == "all" else df[df["position"] == int(
                selected_position)]
            chart_content = dcc.Graph(
                id="top-war-players",
                figure=px.bar(filtered_df.nlargest(10, 'wins_above_replacement'),
                              x='player_id', y='wins_above_replacement',
                              title='Top 10 Players by WAR',
                              hover_data=['first_name', 'last_name', 'position'])
            )
        elif selected_chart == "box":
            chart_content = dcc.Graph(
                id='era-by-throwing-hand',
                figure=px.box(df, x='throws', y='earned_run_average',
                              title='ERA by Throwing Hand')
            )

        # Return chart content, show content div, hide placeholder
        return chart_content, {"display": "block"}, {"display": "none"}
