from typing import Iterable, Iterator

import arrow

from geanpy.common_types import ApiAvailableSlot, Slot


def transform_available_slots(available_slots: Iterable[ApiAvailableSlot]) -> Iterator[Slot]:
    for slot in available_slots:
        yield Slot(
            location_id=slot["locationId"],
            start_timestamp=arrow.get(slot["startTimestamp"]),
            end_timestamp=arrow.get(slot["endTimestamp"]),
            active=slot["active"],
            duration=slot["duration"],
            remote_ind=slot["remoteInd"],
        )
