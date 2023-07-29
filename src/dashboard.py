"""
This file contains the logic for building the dash app and creating the dashboard.
"""

from dash import html

COLORS = {
    'bg-1': '#0c0c0c',
    'bg-2': '#1e1e1e',
    'bg-3': '#efefef',
    'text-1': '#ddd'
}

def get_layout() -> html.Div:
    """
    Defines the layout of the entire application.

    Returns:
        html.Div: A div containing all other elements of the application as
            a descendant. 
    """

    return html.Div(
        style={
            'backgroundColor': COLORS['bg-1']
        },
        children=[
            html.H1(
                children='Hello World!',
                style={
                    'textAlign': 'center',
                    'color': COLORS['text-1']
                }
            )
        ]
    )