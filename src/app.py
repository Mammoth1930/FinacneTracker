"""
Author: Riley Farrell
Date: 16/04/2023

Main file for FinanceTracker application, code should always be run from here.
"""

from dash import Dash

from database import *
from api import *
from dashboard import *

app = Dash(__name__)
app.layout = get_layout()

@app.callback(
    [

    ],
    [

    ]
)
def update_dashboard():
    """
    
    """

    pass


if __name__ == '__main__':
    db_init()
    update_dataset()
    tables_to_csv()
    # app.run_server(debug=True)

    # query = '''
    #     SELECT *
    #     FROM Transactions 
    #     WHERE (
    #             Status != "SETTLED"
    #             OR (
    #                 amount < 0
    #                 AND category IS NULL
    #                 AND id NOT IN (
    #                     SELECT id
    #                     FROM Transactions
    #                     WHERE description LIKE "Transfer%"
    #                         OR description LIKE "Quick save transfer%"
    #                         OR description = "Round Up"
    #                         OR description = "Interest"
    #                         OR description LIKE "Cover to%"
    #                         OR description LIKE "Forward to%"
    #                         OR description LIKE "Auto Transfer to%"
    #                 )
    #             )
    #         )
    #         AND createdAt < "2023-07-29T17:12:43+10:00"
    # '''

    # res = read_database(query)

    # print(res)