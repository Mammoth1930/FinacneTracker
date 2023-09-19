"""
This file contains the logic for building the dash app and creating the dashboard.
"""

import pandas as pd

from dash import html, callback, dcc, Input, Output

from database import read_database
from helpers import str_to_datetime

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

def get_select_years() -> list[dict[str, str]]:
    """
    Gets all of the possible year values for the year-select dropdown. Any year
    where there was one or more transaction recorded during that year will be
    returned. An all years option will also always be returned.

    Returns:
        A list of dictionaries, with each dictionary containing as keys the
        label and value of the year, which is simply the year in yyyy format as
        a string for both. Or label = "All", value = "all" for the all years
        option.
    """

    res = []
    years_df = read_database(
        '''
        SELECT strftime("%Y", createdAt) AS year
        FROM Transactions
        GROUP BY strftime("%Y", createdAt)
        ORDER BY strftime("%Y", createdAt) DESC
        '''
    )

    for i, row in years_df.iterrows():
        res.append({'label': row['year'], 'value': row['year']})

    return res

def get_select_month() -> list[dict[str, str]]:
    """
    
    """

    res = [
        {'label': 'January', 'value': '01'},
        {'label': 'February', 'value': '02'},
        {'label': 'March', 'value': '03'},
        {'label': 'April', 'value': '04'},
        {'label': 'May', 'value': '05'},
        {'label': 'June', 'value': '06'},
        {'label': 'July', 'value': '07'},
        {'label': 'August', 'value': '08'},
        {'label': 'September', 'value': '09'},
        {'label': 'October', 'value': '10'},
        {'label': 'November', 'value': '11'},
        {'label': 'December', 'value': '12'},
    ]

    return res
    


def get_layout() -> html.Div:
    """
    Defines the layout of the entire application.

    Returns:
        html.Div: A div containing all other elements of the application as
            a descendant. 
    """

    return html.Div(
        # style={
        #     'backgroundColor': COLORS['bg-1'],
        #     'color': COLORS['text-1']
        # },
        children=[
            html.H1(
                children='Hello World!',
                # style={
                #     'textAlign': 'center',
                #     'color': COLORS['text-1']
                # }
            ),
            create_table(read_database('SELECT * FROM Accounts')),
            html.Hr(),
            html.Div([
                "Filter Year",
                dcc.Dropdown(
                    id='year-select',
                    options=get_select_years(),
                    # value='all',
                    multi=True,
                    optionHeight=50
                )
            ]),
            html.Hr(),
            html.Div([
                "Filter Month",
                dcc.Dropdown(
                    id='month-select',
                    options=get_select_month(),
                    # value='all',
                    multi=True,
                    optionHeight=50
                )
            ]),
            html.Hr(),
            html.Div([
                "Date range",
                dcc.DatePickerRange(
                    id='date-range-select',
                    clearable=True,
                    min_date_allowed=str_to_datetime(
                        read_database(
                            '''SELECT MIN(createdAt) FROM Transactions'''
                        ).iloc[0][0]
                    ).date(),
                    max_date_allowed=str_to_datetime(
                        read_database(
                            '''SELECT MAX(createdAt) FROM Transactions'''
                        ).iloc[0][0]
                    ).date()
                )
            ]),
            html.Hr(),
            html.Div([
                "Group By",
                dcc.Dropdown(
                    id='group-select',
                    options=[
                        {'label': 'Year', 'value': 'year'},
                        {'label': 'Quarter', 'value': 'quarter'},
                        {'label': 'Month', 'value': 'month'},
                        {'label': 'Day', 'value': 'day'},
                    ],
                    value='day',
                    optionHeight=50,
                    clearable=False
                )
            ])
        ]
    )

@callback(
    Output('date-range-select', 'min_date_allowed'),
    Output('date-range-select', 'max-date-allowed'),
    Input('year-select', 'value'),
    Input('month-select', 'value')
)
def update_date_range(years: list[str], months: list[str]) -> tuple:
    """
    
    """

    # If the user hasn't provided a filter than use all the available years.
    if years is None or len(years) == 0:
        min_year = read_database(
            '''
            SELECT strftime("%Y", MIN(createdAt))
            FROM Transactions
            '''
        ).iloc[0][0]

        max_year = read_database(
            '''
            SELECT strftime("%Y", MAX(createdAt))
            FROM Transactions
            '''
        ).iloc[0][0]
    else:
        min_year = min(map(int, years))
        max_year = max(map(int, years))

    # If the user hasn't provided a filter than use all available months.
    if months is None or len(months) == 0:
        months = [month['value'] for month in get_select_month()]
    
    placeholders = ','.join(['?' for _ in range(len(months))])

    min_date = str_to_datetime(
            read_database(
            f'''
            SELECT MIN(createdAt)
            FROM Transactions
            WHERE strftime("%Y", createdAt) = "{min_year}"
                AND strftime("%m", createdAt) IN ({placeholders})
            ''',
            params=months
        ).iloc[0][0]
    ).date()

    max_date = str_to_datetime(
        read_database(
            f'''
            SELECT MAX(createdAt)
            FROM Transactions
            WHERE strftime("%Y", createdAt) = "{max_year}"
                AND strftime("%m", createdAt) IN ({placeholders})
            ''',
            params=months
        ).iloc[0][0]
    ).date()

    return min_date, max_date