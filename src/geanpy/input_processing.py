import datetime
import logging
import time

from geanpy.common_types import DateTimeFilters


def parse_datetime_filters(args) -> DateTimeFilters:
    date_format_str = "%Y-%m-%d %H:%M"
    time_format_str = "%H:%M"

    before_datetime = None
    after_datetime = None
    before_time = None
    after_time = None

    before_datetime_str = args.before_datetime
    after_datetime_str = args.after_datetime
    before_time_str = args.before_time
    after_time_str = args.after_time

    if (before_datetime_str or after_datetime_str) and (before_time_str or after_time_str):
        logging.debug(
            "Invalid filters: before_datetime=%r, after_datetime=%r, before_time=%r, after_time=%r",
            before_datetime_str,
            after_datetime_str,
            before_time_str,
            after_time_str,
        )
        raise ValueError("Only date-times or times are allowed, but you can't combine them")
    

    if before_datetime_str:
        before_datetime = datetime.datetime.strptime(before_datetime_str, date_format_str)

    if after_datetime_str:
        after_datetime = datetime.datetime.strptime(after_datetime_str, date_format_str)

    if before_time_str:
        before_time_struct = time.strptime(before_time_str, time_format_str)
        before_time = datetime.time(hour=before_time_struct.tm_hour, minute=before_time_struct.tm_min)

    if after_time_str:
        after_time_struct = time.strptime(after_time_str, time_format_str)
        after_time = datetime.time(hour=after_time_struct.tm_hour, minute=after_time_struct.tm_min)

    return DateTimeFilters(
        before_datetime=before_datetime,
        after_datetime=after_datetime,
        before_time=before_time,
        after_time=after_time,
    )
