"""
This file contains miscellaneous helper functions that don't belong in any of
the other files.
"""

import re
import datetime

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
    The datetime string with 1 second added or None if datetime_string is None.
"""

  if datetime_string is None:
     return None
  
  datetime_object = datetime.datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z")
  new_datetime_object = datetime_object + datetime.timedelta(seconds=1)
  new_datetime_string = new_datetime_object.strftime("%Y-%m-%dT%H:%M:%S%z")
  new_datetime_string = new_datetime_string[:-2] + ':' + new_datetime_string[-2:]

  return new_datetime_string
