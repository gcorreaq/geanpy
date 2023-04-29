import argparse
import json
import logging
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Iterator, Iterable

from gean.api import GlobalEntryApi
from gean.logger import setup_logger
from gean.translators import parse_datetime
from gean.common_types import Slot


setup_logger(os.environ.get("LOGLEVEL", "ERROR").upper())


def _load_locations() -> Any:
    with open(Path("gean/locations.json"), "r") as f_obj:
        locations_list = json.load(f_obj)

    return {str(location_data["id"]): location_data for location_data in locations_list}


LOCATIONS_BY_ID = _load_locations()


def get_availability_dates(
    slots: Iterable[Slot], before_datetime: datetime | None
) -> Iterator[datetime]:
    final_slots = slots
    if before_datetime:
        final_slots = (slot for slot in final_slots if slot.start_timestamp < before_datetime)

    for slot in final_slots:
        logging.info("=> Slot available at %s", slot.start_timestamp)
        yield slot.start_timestamp


def process_locations(location_ids: list[str], before_datetime: datetime | None):
    api = GlobalEntryApi()
    for location_id in location_ids:
        available_slots = api.get_appointment_slots(location_id=location_id)
        available_dates = list(
            get_availability_dates(available_slots, before_datetime=before_datetime)
        )
        available_dates_count = len(available_dates)
        logging.debug("Found %d available slots", available_dates_count)
        if available_dates_count > 0:
            # JACKPOT!
            logging.info(
                "There's %d appointment(s) available at %s",
                available_dates_count,
                LOCATIONS_BY_ID[location_id]["shortName"],
            )


def validate_locations(location_ids: list[str]):
    logging.debug("Validatig locations: %s", location_ids)
    for location_id in location_ids:
        if location_id not in LOCATIONS_BY_ID:
            raise ValueError(f"Location {location_id} is not a valid location")
    logging.debug("All location IDs are valid: %s", location_ids)


def main(location_ids: list[str], before_datetime_str: str | None):
    logging.debug(
        "Processing locations: %s",
        {LOCATIONS_BY_ID[location_id]["shortName"]: location_id for location_id in location_ids},
    )
    if before_datetime_str is not None:
        before_datetime = parse_datetime(before_datetime_str)
        logging.debug(
            "Only looking for interviews before %r",
            before_datetime,
        )
    else:
        before_datetime = None
    process_locations(location_ids=location_ids, before_datetime=before_datetime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check for Global Entry appointment availability",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--locations",
        action="append",
        help="The location(s) to check for",
        required=True,
    )
    parser.add_argument(
        "--before-datetime", help="Only alert for appointments before this date and time"
    )
    args = parser.parse_args()

    validate_locations(args.locations)

    main(args.locations, args.before_datetime)
