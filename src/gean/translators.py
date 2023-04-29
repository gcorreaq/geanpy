from datetime import datetime
from typing import Iterable, Iterator

from global_entry_appointment_notifier.common_types import ApiAvailableSlot, Slot


def transform_available_slots(available_slots: Iterable[ApiAvailableSlot]) -> Iterator[Slot]:
    for slot in available_slots:
        yield Slot(
            location_id=slot["locationId"],
            start_timestamp=parse_datetime(slot["startTimestamp"]),
            end_timestamp=parse_datetime(slot["endTimestamp"]),
            active=slot["active"],
            duration=slot["duration"],
            remote_ind=slot["remoteInd"],
        )


def parse_datetime(datetime_string: str) -> datetime:
    return datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M")
