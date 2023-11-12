# import plotly.express as px
# import pandas as pd
# from plotly import graph_objects as go
# from typing import Callable


# from database import read_database

# def income_pie_chart(start_date:str, end_date:str) -> go.Figure:
#     """
    
#     """
#     income_df = read_database(
#         f'''
#             SELECT SUM(amount) as totalAmount, description, isCategorizable
#             FROM transactions
#             WHERE amount > 0
#                 AND status = "SETTLED"
#                 AND (isCategorizable = 1 OR description LIKE "%interest%")
#                 AND settledAt BETWEEN "{start_date}" AND "{end_date}"
#             GROUP BY description
#             ORDER BY SUM(amount) DESC
#         '''
#     )

#     # Combine all interest payments into a single sum

#     # Get all interest payments
#     interest_payments = income_df[
#         income_df['description'].str.contains('interest', case=False) &
#         (income_df['isCategorizable'] == 0)
#     ]
#     total_interest_amount = interest_payments['totalAmount'].sum()
    
#     # Remove them from income df
#     income_df = income_df[
#         ~(
#             income_df['description'].str.contains('interest', case=False) &
#             (income_df['isCategorizable'] == 0)
#         )
#     ]
    
#     # Add in aggregated interest payments
#     income_df = pd.concat(
#         [
#             pd.DataFrame({
#                 'totalAmount': [total_interest_amount],
#                 'description': ['interest'],
#                 'isCategorizable': [1]
#             }),
#             income_df
#         ],
#         ignore_index=True
#     )

#     # Formatting of DataFrame for chart
#     income_df.drop(columns=['isCategorizable'], inplace=True)
#     income_df = income_df.sort_values(by='totalAmount', ascending=False).reset_index(drop=True)
#     income_df['totalAmount'] = income_df['totalAmount'] / 100

#     # Create the chart
#     fig = go.Figure(data=[
#         go.Pie(
#             labels=income_df['description'],
#             values=income_df['totalAmount'],
#             hole=0.5
#         )
#     ])
#     fig.update_traces(
#         hoverinfo='label+value+percent',
#         textinfo='label+value',
#         textposition='inside',
#     )
#     fig.update_layout(
#         uniformtext_minsize=12,
#         uniformtext_mode='hide',
#         height=700,
#         showlegend=False
#     )

#     return fig

# def spending_pie_chart(start_date:str, end_date:str) -> go.Figure:
#     """
    
#     """

#     # ToDo: Think of a better way to filter out payments to investment account
#     spending_df = read_database(
#         f'''
#             SELECT SUM(amount) as totalAmount, description, category, parentCategory
#             FROM transactions
#             WHERE amount < 0
#                 AND status = "SETTLED"
#                 AND settledAt BETWEEN "{start_date}" AND "{end_date}"
#                 AND isCategorizable = 1
#                 AND description != "CMC Investment Accnt"
#             GROUP BY description, category, parentCategory
#             ORDER BY SUM(amount) ASC
#         '''
#     )

#     fig = px.sunburst(
#         spending_df,
#         path=['description', 'category', 'parentCategory'],
#         values='totalAmount'
#     )

#     return fig


# def get_all_draw_functions() -> list[Callable]:
#     """
#     Returns a list of all the functions in this module that create a chart and
#     return it. All functions in the list should take two parameters start_date
#     and end_date.

#     Returns:
#         function_list: A list of all the functions in charts.py that return a
#             figure for the dashboard. The list will contain the functions in the
#             same order they are defined in the module, which is the same order
#             they appear on the dashboard.
#     """
#     return [
#         income_pie_chart,
#         spending_pie_chart
#     ]