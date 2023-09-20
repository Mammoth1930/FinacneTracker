"""
This file contains miscellaneous helper functions that don't belong in any of
the other files.
"""

import re
from datetime import datetime, date, timedelta

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