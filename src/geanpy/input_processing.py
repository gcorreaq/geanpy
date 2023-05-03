import datetime
import logging
import time
from typing import Optional

import arrow

from geanpy.common_types import DateTimeFilters


def parse_datetime_filters(args) -> DateTimeFilters:
    before_datetime: Optional[arrow.Arrow] = args.before_datetime
    after_datetime: Optional[arrow.Arrow] = args.after_datetime
    before_time: Optional[arrow.Arrow] = args.before_time
    after_time: Optional[arrow.Arrow] = args.after_time
    before_date: Optional[arrow.Arrow] = args.before_date
    after_date: Optional[arrow.Arrow] = args.after_date

    if (before_datetime or after_datetime) and (
        (before_time or after_time) or (before_date or after_date)
    ):
        logging.debug(
            "Invalid filters: before_datetime=%r, after_datetime=%r, before_time=%r, after_time=%r, before_date=%r, after_date=%r",
            before_datetime,
            after_datetime,
            before_time,
            after_time,
            before_date,
            after_date,
        )
        raise ValueError(
            "Only date-times or dates and times are allowed, but you can't combine them"
        )
    
    final_before_time: Optional[datetime.time] = None
    final_after_time: Optional[datetime.time] = None

    if before_time:
        final_before_time = before_time.time()
    
    if after_time:
        final_after_time = after_time.time()

    return DateTimeFilters(
        before_datetime=before_datetime,
        after_datetime=after_datetime,
        before_time=final_before_time,
        after_time=final_after_time,
        before_date=before_date,
        after_date=after_date,
    )
