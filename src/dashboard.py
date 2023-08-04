"""
This file contains the logic for building the dash app and creating the dashboard.
"""

import pandas as pd

from dash import html, callback

from database import read_database, db_init
from api import update_dataset, tables_to_csv

COLORS = {
    'bg-1': '#0c0c0c',
    'bg-2': '#1e1e1e',
    'bg-3': '#efefef',
    'text-1': '#ddd'
}

def create_table(df: pd.DataFrame, max_rows: int=10) -> html.Table:
    """

    """

    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])

def get_layout() -> html.Div:
    """
    Defines the layout of the entire application.

    Returns:
        html.Div: A div containing all other elements of the application as
            a descendant. 
    """

    return html.Div(
        style={
            'backgroundColor': COLORS['bg-1'],
            'color': COLORS['text-1']
        },
        children=[
            html.H1(
                children='Hello World!',
                style={
                    'textAlign': 'center',
                    'color': COLORS['text-1']
                }
            ),
            create_table(read_database("SELECT * FROM Accounts"))
        ]
    )

@callback(
    [

    ],
    [

    ]
)
def update_dashboard():
    """
    
    """
    print("this code is running")


