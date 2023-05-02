from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional
from typing_extensions import NamedTuple, TypedDict


ApiAvailableSlot = TypedDict(
    "ApiAvailableSlot",
    {
        # The ID of the location where the interview is available at
        "locationId": int,
        # Start time of the appointment (2023-12-19T10:30)
        "startTimestamp": str,
        # End time of the appointment (2023-12-19T10:45)
        "endTimestamp": str,
        # ???
        "active": bool,
        # Duration of the appointment. Seems to be in minutes
        "duration": int,
        # ???
        "remoteInd": bool,
    },
)

Slot = NamedTuple(
    "Slot",
    [
        ("location_id", int),
        ("start_timestamp", datetime),
        ("end_timestamp", datetime),
        ("active", bool),
        ("duration", int),
        ("remote_ind", bool),
    ],
)


@dataclass
class DateTimeFilters:
    before_datetime: Optional[datetime]
    after_datetime: Optional[datetime]
    before_time: Optional[time]
    after_time: Optional[time]

    @property
    def datetime_filters_set(self) -> bool:
        return bool(self.before_datetime or self.after_datetime)

    @property
    def time_filters_set(self) -> bool:
        return bool(self.before_time or self.after_time)

    @property
    def any_filters_set(self) -> bool:
        return self.datetime_filters_set or self.time_filters_set

    def is_datetime_in_range(self, target_datetime: datetime) -> bool:
        # Always return True if we don't have filters
        if not self.datetime_filters_set:
            return True

        if self.before_datetime and not (target_datetime < self.before_datetime):
            return False

        if self.after_datetime and not (target_datetime > self.after_datetime):
            return False

        return True

    def is_time_in_range(self, target_datetime: datetime) -> bool:
        if not self.time_filters_set:
            return True

        if self.before_time and not (target_datetime.time() < self.before_time):
            return False

        if self.after_time and not (target_datetime.time() > self.after_time):
            return False

        return True

    def __str__(self) -> str:
        date_format_str = "%Y-%m-%d %H:%M"
        time_format_str = "%H:%M"
        before_str = None
        after_str = None
        if self.datetime_filters_set:
            if self.before_datetime:
                before_str = self.before_datetime.strftime(date_format_str)
            elif self.after_datetime:
                after_str = self.after_datetime.strftime(date_format_str)
        elif self.time_filters_set:
            if self.before_time:
                before_str = self.before_time.strftime(time_format_str)
            elif self.after_time:
                after_str = self.after_time.strftime(time_format_str)

        if before_str and after_str:
            return f"datetimefilters(after: {after_str} - before: {before_str})"
        elif before_str:
            return f"datetimefilters(before: {before_str})"
        elif after_str:
            return f"datetimefilters(after: {after_str})"
        else:
            return "DateTimeFilters(Any)"
