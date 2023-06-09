import argparse
import json
import logging
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Iterator, Iterable

from geanpy.api import GlobalEntryApi
from geanpy.logger import setup_logger
from geanpy.notifier import notify
from geanpy.translators import parse_datetime
from geanpy.common_types import Slot


setup_logger(os.environ.get("LOGLEVEL", "INFO").upper())


def _load_locations() -> Any:
    # To consistently resolve the path to this JSON file, the best approach is to
    # always resolve the absolute path of the parent folder of the current file
    # Taken from https://stackoverflow.com/a/3430395
    with open(Path(__file__).parent.resolve() / Path("locations.json"), "r") as f_obj:
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


def process_locations(location_ids: Iterable[str], before_datetime: datetime | None):
    api = GlobalEntryApi()
    for location_id in location_ids:
        available_slots = api.get_appointment_slots(location_id=location_id)
        available_dates = list(
            get_availability_dates(available_slots, before_datetime=before_datetime)
        )
        available_dates_count = len(available_dates)
        logging.debug("Found %d available slots", available_dates_count)
        location_name = LOCATIONS_BY_ID[location_id]["shortName"]
        if available_dates_count > 0:
            # JACKPOT!
            logging.info(
                "There's %d appointment(s) available at %s",
                available_dates_count,
                location_name,
            )
            notify(
                title="GEAN: Appointments Available! 🎉",
                text=f"There's {available_dates_count} appointment(s) available at {location_name}",
            )
        else:
            logging.info("There's no appointments available at %s", location_name)
            notify(
                title="GEAN: No Appointments Available 🥲",
                text=f"No appointments available at {location_name}",
            )


def validate_locations(location_ids: Iterable[str]):
    logging.debug("Validatig locations: %s", location_ids)
    for location_id in location_ids:
        if location_id not in LOCATIONS_BY_ID:
            raise ValueError(f"Location {location_id} is not a valid location")
    logging.debug("All location IDs are valid: %s", location_ids)


def main(location_ids: Iterable[str], before_datetime_str: str | None):
    logging.info(
        "Processing locations: %s",
        ", ".join(LOCATIONS_BY_ID[location_id]["shortName"] for location_id in location_ids),
    )
    if before_datetime_str is not None:
        before_datetime = parse_datetime(before_datetime_str)
        logging.info(
            "Only looking for interviews before %s",
            before_datetime.strftime("%Y-%m-%d %H:%M"),
        )
    else:
        before_datetime = None
    process_locations(location_ids=location_ids, before_datetime=before_datetime)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check for Global Entry appointment availability",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    locations_help_str = """The location(s) to check for.
    You can add the flag multiple times with different location IDs"""
    parser.add_argument(
        "--locations",
        "-l",
        action="append",
        help=locations_help_str,
        required=True,
    )
    parser.add_argument(
        "--before-datetime", "-b", help="Only alert for appointments before this date and time"
    )
    args = parser.parse_args()
    location_ids_set = set(args.locations)

    validate_locations(location_ids=location_ids_set)

    main(location_ids=location_ids_set, before_datetime_str=args.before_datetime)
