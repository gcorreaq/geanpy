import logging

from typing import Iterable

from global_entry_appointment_notifier.translators import transform_available_slots
from global_entry_appointment_notifier.common_types import ApiAvailableSlot, Slot

import requests


BASE_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slot-availability"


class GlobalEntryApi:
    session: requests.Session

    def __init__(self) -> None:
        self.session = requests.Session()

    def get_location_response(self, location: str) -> requests.Response:
        response = self.session.get(BASE_URL, params={"locationId": location})
        response.raise_for_status()
        return response

    def get_appointment_slots(self, location_id: str) -> Iterable[Slot]:
        try:
            response = self.get_location_response(location=location_id)
        except requests.HTTPError:
            logging.exception("Something went really wrong! We keep going though")
            raise
        else:
            logging.debug("Response status from API: %s", response.status_code)

        data = response.json()
        api_available_slots: list[ApiAvailableSlot] = data.get("availableSlots")
        return transform_available_slots(api_available_slots)
