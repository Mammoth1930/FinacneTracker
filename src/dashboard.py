"""
This file contains the logic for building the dash app and creating the dashboard.
"""

import plotly.express as px
import pandas as pd

from dash import html, callback, dcc, Input, Output
from datetime import date
from plotly import graph_objects as go
from typing import Callable

from database import read_database
from helpers import *
from charts import *

COLORS = {
    'bg-1': '#0c0c0c',
    'bg-2': '#1e1e1e',
    'bg-3': '#efefef',
    'text-1': '#ddd'
}

# ToDo remove this or move to helpers.py
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
            'display': 'flex',
            'flex-direction': 'row'
        },
        children=[
            html.Div(
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'min-width': '336px'
                },
                children=[
                    # Year select dropdown
                    html.Div([
                        "Filter Year",
                        dcc.Dropdown(
                            id='year-select',
                            options=get_select_years(),
                            multi=True,
                            optionHeight=50
                        )
                    ], style={
                        'padding': '5px 10px'
                    }),
                    # Month select dropdown
                    html.Div([
                        "Filter Month",
                        dcc.Dropdown(
                            id='month-select',
                            options=get_select_month(),
                            multi=True,
                            optionHeight=50
                        )
                    ], style={
                        'padding': '5px 10px'
                    }),
                    # Date filter
                    html.Div([
                        html.Div("Filter Dates"),
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
                            ).date(),
                            initial_visible_month=str_to_datetime(
                                read_database(
                                    '''SELECT MAX(createdAt) FROM Transactions'''
                                ).iloc[0][0]
                            ).date(),
                            display_format='DD/MM/YYYY',
                            updatemode='bothdates'
                        )
                    ], style={
                        'padding': '5px 10px'
                    }),
                    # Group by
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
                    ], style={
                        'padding': '5px 10px'
                    }),
                ]
            ),
            html.Div(
                style = {
                    'display': 'flex',
                    'flex-wrap': 'wrap',
                    'align-items': 'center',
                    'justify-content': 'space-evenly'
                },
                children=[
                    # Total income pie chart
                    html.Div(
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center'
                        },
                        children=[
                            html.H4('Income Total'),
                            dcc.Graph(
                                id='income-pie-chart'
                            ),
                        ]
                    ),
                    # Total spending pie chart
                    html.Div(
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center'
                        },
                        children=[
                            html.H4('Spending Total'),
                            dcc.Graph(
                                id='spending-total-sunburst'
                            )
                        ]
                    )
                ]
            )
        ]
    )

@callback(
    Output('date-range-select', 'min_date_allowed'),
    Output('date-range-select', 'max_date_allowed'),
    Output('date-range-select', 'initial_visible_month'),
    Output('date-range-select', 'start_date'),
    Output('date-range-select', 'end_date'),
    Input('year-select', 'value'),
    Input('month-select', 'value'),
    Input('date-range-select', 'start_date'),
    Input('date-range-select', 'end_date')
)
def update_date_range(
    years: list[str]|None,
    months: list[str]|None,
    start: str|None,
    end: str|None
) -> tuple[date, date, date, date|None, date|None]:
    """
    Updates the date-range-select component based on the input of the 
    year-select and month-select dropdown components. This function ensures that
    any date range selected is valid given the years and months selected in the
    dropdowns and also changes the range of possible dates to select based on
    the values of the dropdowns.

    Params:
        years: A list of strings representing the years, in "YYYY" format, which
            have been selected by the year-select dropdown. If the list is empty
            or None then this is treated as if all years have been selected.
        months: A list of strings representing the months, in "MM" format, which
            have been selected by the month-select dropdown. If the list is empty
            or None then this is treated as if all months have been selected.
        start: The start date value of the date-range-select DatePickerRange,
            represented as a string in "YYYY-MM-DD" format.
        end: The end date value of the date-range-select DatePickerRange,
            represented as a string in "YYYY-MM_DD" format.
    
    Returns:
        min_date: A datetime.date representing the earliest date inside
            the restrictions set by the dropdowns on which there was a
            transaction.
        max_date: A datetime.date representing the latest date inside
            the restrictions set by the dropdowns on which there was a
            transaction.
        max_date: A datetime.date representing the month the DatePickerRange
            will initially display when clicked. This is set to the month of the
            max_date.
        start_date: A datetime.date to be displayed in the DatePickerRange. If
            the start parameter was inside the min_date, max_date
            range then start_date will be that date. Otherwise if start was None
            or was outside the min_date, max_date range start_date will be None.
        end_date: A datetime.date to be displayed in the DatePickerRange. If
            the end parameter was inside the min_date, max_date
            range then end_date will be that date. Otherwise if end was None
            or was outside the min_date, max_date range end_date will be None.
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
            WHERE strftime("%Y", datetime(createdAt, "localtime")) = "{min_year}"
                AND strftime("%m", datetime(createdAt, "localtime")) IN ({placeholders})
            ''',
            params=months
        ).iloc[0][0]
    ).date()

    max_date = str_to_datetime(
        read_database(
            f'''
            SELECT MAX(createdAt)
            FROM Transactions
            WHERE strftime("%Y", datetime(createdAt, "localtime")) = "{max_year}"
                AND strftime("%m", datetime(createdAt, "localtime")) IN ({placeholders})
            ''',
            params=months
        ).iloc[0][0]
    ).date()

    # Check that the current date-range-select values are withing the min_date, max_date range
    start_date, end_date = check_date_range(start, end, min_date, max_date)

    return min_date, max_date, max_date, start_date, end_date

###############################################################################
#################################CHARTS########################################
###############################################################################

@callback(
    Output('income-pie-chart', 'figure'),
    Input('year-select', 'value'),
    Input('month-select', 'value'),
    Input('date-range-select', 'start_date'),
    Input('date-range-select', 'end_date')
)
def income_pie_chart(
    years: list[str]|None, 
    months: list[str]|None,
    date_select_start: str|None,
    date_select_end: str|None
) -> go.Figure:
    """
    
    """
    min_date, max_date = get_min_and_max_dates(years, months, date_select_start, date_select_end)

    income_df = read_database(
        f'''
            SELECT SUM(amount) as totalAmount, description, isCategorizable
            FROM transactions
            WHERE amount > 0
                AND status = "SETTLED"
                AND (isCategorizable = 1 OR description LIKE "%interest%")
                AND settledAt BETWEEN "{min_date}" AND "{max_date}"
            GROUP BY description
            ORDER BY SUM(amount) DESC
        '''
    )

    # Combine all interest payments into a single sum

    # Get all interest payments
    interest_payments = income_df[
        income_df['description'].str.contains('interest', case=False) &
        (income_df['isCategorizable'] == 0)
    ]
    total_interest_amount = interest_payments['totalAmount'].sum()
    
    # Remove them from income df
    income_df = income_df[
        ~(
            income_df['description'].str.contains('interest', case=False) &
            (income_df['isCategorizable'] == 0)
        )
    ]
    
    # Add in aggregated interest payments
    income_df = pd.concat(
        [
            pd.DataFrame({
                'totalAmount': [total_interest_amount],
                'description': ['interest'],
                'isCategorizable': [1]
            }),
            income_df
        ],
        ignore_index=True
    )

    # Formatting of DataFrame for chart
    income_df.drop(columns=['isCategorizable'], inplace=True)
    income_df = income_df.sort_values(by='totalAmount', ascending=False).reset_index(drop=True)
    income_df['totalAmount'] = income_df['totalAmount'] / 100

    # Create the chart
    fig = go.Figure(data=[
        go.Pie(
            labels=income_df['description'],
            values=income_df['totalAmount'],
            hole=0.5
        )
    ])
    fig.update_traces(
        hoverinfo='label+value+percent',
        textinfo='label+value',
        textposition='inside',
    )
    fig.update_layout(
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        height=600,
        showlegend=False
    )

    return fig


@callback(
    Output('spending-total-sunburst', 'figure'),
    Input('year-select', 'value'),
    Input('month-select', 'value'),
    Input('date-range-select', 'start_date'),
    Input('date-range-select', 'end_date')
)
def spending_total_sunburst(
    years: list[str]|None, 
    months: list[str]|None,
    date_select_start: str|None,
    date_select_end: str|None
) -> go.Figure:
    """
    
    """

    min_date, max_date = get_min_and_max_dates(years, months, date_select_start, date_select_end)

    # ToDo: Think of a better way to filter out payments to investment account
    spending_df = read_database(
        f'''
            SELECT SUM(amount) as totalAmount, description
            FROM transactions
            WHERE amount < 0
                AND status = "SETTLED"
                AND settledAt BETWEEN "{min_date}" AND "{max_date}"
                AND isCategorizable = 1
                AND description != "CMC Investment Accnt"
            GROUP BY description
            ORDER BY SUM(amount) ASC
        '''
    )

    # Format DataFrame for chart
    spending_df['totalAmount'] = spending_df['totalAmount'].abs() / 100


    # Create the chart
    fig = go.Figure(data=[
        go.Pie(
            labels=spending_df['description'],
            values=spending_df['totalAmount'],
            hole=0.5
        )
    ])
    fig.update_traces(
        hoverinfo='label+value+percent',
        textinfo='label+value',
        textposition='inside',
    )
    fig.update_layout(
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        height=600,
        showlegend=False
    )

    return fig