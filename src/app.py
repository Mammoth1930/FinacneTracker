"""
Author: Riley Farrell
Date: 16/04/2023

Main file for FinanceTracker application, code should always be run from here.
"""

from dash import Dash

from database import db_init
from api import update_dataset, tables_to_csv
from dashboard import get_layout

app = Dash(__name__)
app.layout = get_layout

if __name__ == '__main__':

    db_init()
    update_dataset()
    tables_to_csv()

    app.run_server(debug=True)