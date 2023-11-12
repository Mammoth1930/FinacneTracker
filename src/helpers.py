"""
This file contains miscellaneous helper functions that don't belong in any of
the other files.
"""

import re
from datetime import datetime, date, timedelta

from database import read_database

def remove_emojis(text: str) -> str:
    """
    Removes all emojies and leading/trailing whitespace from a string.

    Params:
        text: The string from which the emojies and whitespace is to be removed.

    Returns:
        str: The provided string with all emojies and leading/trailing whitespace
            removed.
    """

    emoji = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642" 
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
                    "]+", re.UNICODE)

    return re.sub(emoji, '', text).strip()

def add_second(datetime_string: str|None) -> str|None:
  """
Adds 1 second to the given datetime string and returns it as a string.

Params:
    datetime_string: The datetime string to add 1 second to. It should be of the
        format "%Y-%m-%dT%H:%M:%S%z".

Returns:
    str|None: The datetime string with 1 second added or None if datetime_string
        is None.
"""

  if datetime_string is None:
     return None
  
  datetime_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z")
  new_datetime_object = datetime_object + timedelta(seconds=1)
  new_datetime_string = new_datetime_object.strftime("%Y-%m-%dT%H:%M:%S%z")
  new_datetime_string = new_datetime_string[:-2] + ':' + new_datetime_string[-2:]

  return new_datetime_string

def str_to_datetime(datetime_string:str) -> datetime:
    """
    Takes a datetime string in "%Y-%m-%dT%H:%M:%S%z" format and converts it to a
    datetime.datetime object.

    Params:
        datetime_string: The string representing the datetime object which
            will be created and returned by the function. It must be of the
            format "%Y-%m-%dT%H:%M:%S%z".
    
    Returns:
        datetime: A datetime object with the same time properties dictated by
            the string.
    """

    return datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z")

def check_date_range(start: str|None, end: str|None, min_date: date, max_date: date) -> tuple[date|None, date|None]:
    """
    Checks if start and end are between min_date and max_date.

    Params:
        start: A string in "YYYY-MM-DD" format representing the start date.
        end: A string in "YYYY-MM-DD" format representing the end date.
        min_date: A datetime.date representing the minimum possible date.
        max_date: A datetime.date representing the maximum possible date.
    
    Returns:
        start_date: The start string as a datetime.date if start was not None
            and it was after the minimum date. None otherwise.
        end_date: The end string as a datetime.date if the end was not None
            and it was before the maximum date. None otherwise.
    """
    start_date = datetime.strptime(start, "%Y-%m-%d").date() if start else None
    end_date = datetime.strptime(end, "%Y-%m-%d").date() if end else None

    if start_date and (start_date < min_date or start_date > max_date):
        start_date = None

    if end_date and (end_date > max_date or end_date < min_date):
        end_date = None
    
    return start_date, end_date

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

def get_min_and_max_dates(
    years: list[str]|None,
    months: list[str]|None,
    date_select_start: str|None,
    date_select_end: str|None
):
    """
    
    """
    if date_select_start is not None and date_select_end is not None:
        return date_select_start, date_select_end

    # Initialize min_date and max_date with provided date_select_start and date_select_end.
    min_date, max_date = date_select_start, date_select_end

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

    # Get min_date if it wasn't provided.
    if min_date is None:
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

    # Get max_date if it wasn't provided.
    if max_date is None:
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

    return min_date, max_date