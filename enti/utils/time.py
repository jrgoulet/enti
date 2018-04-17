from datetime import datetime, timedelta
from dateutil import parser


def datetime_to_string(d, utc=False):
    """
    Converts a datetime object to string

    :param d: datetime object
    :return: string, or None
    """
    if isinstance(d, datetime):
        if utc:
            return d.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            return d.strftime('%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(d, str):
        return datetime_to_string(string_to_datetime(d), utc)
    else:
        return None


def string_to_datetime(d):
    """
    Converts a string to a datetime object

    :param d: string date
    :return: string, or None
    """
    if isinstance(d, datetime):
        return d

    elif isinstance(d, str):
        return parser.parse(d)

    elif isinstance(d, int):
        try:
            return datetime.fromtimestamp(d)
        except:
            return None
    else:
        return None

def get_elapsed_minutes(ts, tz=None, naive=False, max_on_null_value=False):
    """
    Determines whether a time interval has expired or elapsed

    :param ts: timestamp
    :param interval_mins: interval in minutes
    :return: bool
    """
    ts = string_to_datetime(ts)

    if ts is None:
        if max_on_null_value:
            return 60*24
        return 0

    if tz is not None:
        return int((datetime.now(tz=tz) - ts).total_seconds() / 60)

    if naive:
        return int((datetime.now() - ts).total_seconds()/60)

    return int((datetime.utcnow() - ts).total_seconds()/60)