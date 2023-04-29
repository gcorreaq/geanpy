from datetime import datetime
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
