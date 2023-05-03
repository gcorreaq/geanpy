import datetime
import logging
import time

from geanpy.common_types import DateTimeFilters
from geanpy.constants import (
    PRINTABLE_DATE_FORMAT_STR,
    PRINTABLE_DATETIME_FORMAT_STR,
    PRINTABLE_TIME_FORMAT_STR,
)


def parse_datetime_filters(args) -> DateTimeFilters:
    before_datetime = None
    after_datetime = None
    before_time = None
    after_time = None
    before_date = None
    after_date = None

    before_datetime_str = args.before_datetime
    after_datetime_str = args.after_datetime
    before_time_str = args.before_time
    after_time_str = args.after_time
    before_date_str = args.before_date
    after_date_str = args.after_date

    if (before_datetime_str or after_datetime_str) and (
        (before_time_str or after_time_str) or (before_date_str or after_date_str)
    ):
        logging.debug(
            "Invalid filters: before_datetime=%r, after_datetime=%r, before_time=%r, after_time=%r, before_date=%r, after_date=%r",
            before_datetime_str,
            after_datetime_str,
            before_time_str,
            after_time_str,
            before_date_str,
            after_date_str,
        )
        raise ValueError(
            "Only date-times or dates and times are allowed, but you can't combine them"
        )

    if before_datetime_str:
        before_datetime = datetime.datetime.strptime(
            before_datetime_str, PRINTABLE_DATETIME_FORMAT_STR
        )

    if after_datetime_str:
        after_datetime = datetime.datetime.strptime(
            after_datetime_str, PRINTABLE_DATETIME_FORMAT_STR
        )

    if before_time_str:
        before_time_struct = time.strptime(before_time_str, PRINTABLE_TIME_FORMAT_STR)
        before_time = datetime.time(
            hour=before_time_struct.tm_hour, minute=before_time_struct.tm_min
        )

    if after_time_str:
        after_time_struct = time.strptime(after_time_str, PRINTABLE_TIME_FORMAT_STR)
        after_time = datetime.time(hour=after_time_struct.tm_hour, minute=after_time_struct.tm_min)

    if before_date_str:
        before_date = datetime.datetime.strptime(before_date_str, PRINTABLE_DATE_FORMAT_STR)

    if after_date_str:
        after_date = datetime.datetime.strptime(after_date_str, PRINTABLE_DATE_FORMAT_STR)

    return DateTimeFilters(
        before_datetime=before_datetime,
        after_datetime=after_datetime,
        before_time=before_time,
        after_time=after_time,
        before_date=before_date,
        after_date=after_date,
    )
