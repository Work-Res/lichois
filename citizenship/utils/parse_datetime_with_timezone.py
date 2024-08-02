from datetime import datetime
import re


def parse_datetime_with_timezone(datetime_str):
    # Ensure the datetime string has the correct format with a colon in the timezone offset
    if re.match(r'.*[+-]\d{2}:\d{2}$', datetime_str):
        return datetime.fromisoformat(datetime_str)
    else:
        # Correct the format by adding the colon in the timezone offset
        datetime_str = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', datetime_str)
        return datetime.fromisoformat(datetime_str)
