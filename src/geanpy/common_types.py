import logging

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
    before_date: Optional[datetime]
    after_date: Optional[datetime]
    before_time: Optional[time]
    after_time: Optional[time]

    @property
    def datetime_filters_set(self) -> bool:
        return bool(self.before_datetime or self.after_datetime)

    @property
    def date_filters_set(self) -> bool:
        return bool(self.before_date or self.after_date)

    @property
    def time_filters_set(self) -> bool:
        return bool(self.before_time or self.after_time)

    @property
    def any_filters_set(self) -> bool:
        return self.datetime_filters_set or self.time_filters_set

    def is_datetime_in_range(self, target_datetime: datetime) -> bool:
        # Short circuit earlier
        if not self.any_filters_set:
            logging.debug("No filters set")
            return True

        if self.datetime_filters_set:
            logging.debug("Using datetime filters")
            return self._is_in_datetime_range(target_datetime=target_datetime)
        elif self.date_filters_set and self.time_filters_set:
            logging.debug("Use date and time filters combined")
            if self._is_in_date_range(target_datetime=target_datetime):
                return self._is_in_time_range(target_datetime=target_datetime)
            else:
                return False
        elif self.date_filters_set:
            # Filter by dates only
            logging.debug("Using date filters")
            return self._is_in_date_range(target_datetime=target_datetime)
        elif self.time_filters_set:
            # Filter by times only
            logging.debug("Using time filters")
            return self._is_in_time_range(target_datetime=target_datetime)

        # The default is to always return True if there's no filters
        return True

    def _is_in_datetime_range(self, target_datetime: datetime) -> bool:
        # Always return True if we don't have filters
        if not self.datetime_filters_set:
            logging.debug("No time filters to apply")
            return True

        if self.before_datetime and not (target_datetime < self.before_datetime):
            logging.debug("Datetime %r is after %r", target_datetime, self.before_datetime)
            return False

        if self.after_datetime and not (target_datetime > self.after_datetime):
            logging.debug("Datetime %r is before %r", target_datetime, self.after_datetime)
            return False

        return True

    def _is_in_date_range(self, target_datetime: datetime) -> bool:
        if not self.date_filters_set:
            logging.debug("No time filters to apply")
            return True

        if self.before_date and not (target_datetime < self.before_date):
            logging.debug("Datetime %r is after %r", target_datetime, self.before_date)
            return False

        if self.after_date and not (target_datetime > self.after_date):
            logging.debug("Datetime %r is before %r", target_datetime, self.after_date)
            return False

        return True

    def _is_in_time_range(self, target_datetime: datetime) -> bool:
        if not self.time_filters_set:
            logging.debug("No time filters to apply")
            return True

        if self.before_time and not (target_datetime.time() < self.before_time):
            logging.debug("Datetime %r is after %r", target_datetime, self.before_time)
            return False

        if self.after_time and not (target_datetime.time() > self.after_time):
            logging.debug("Datetime %r is before %r", target_datetime, self.after_time)
            return False

        return True

    def __str__(self) -> str:
        if self.datetime_filters_set:
            return f"{self.after_datetime} and {self.before_datetime}"

        if self.date_filters_set and self.time_filters_set:
            return f"Any date between {self.after_date} and {self.before_date} and any time between {self.after_time} and {self.before_time}"

        if self.date_filters_set:
            return f"Any date between {self.after_date} and {self.before_date}"

        if self.time_filters_set:
            return f"Any day between {self.after_time} and {self.before_time}"

        return "(Any dates)"
