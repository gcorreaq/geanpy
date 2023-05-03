import argparse
import json
import logging
import os

from datetime import datetime
from pathlib import Path
from typing import Any, Iterator, Iterable

import arrow

from geanpy.api import GlobalEntryApi
from geanpy.input_processing import parse_datetime_filters
from geanpy.logger import setup_logger
from geanpy.notifier import notify
from geanpy.common_types import DateTimeFilters, Slot


setup_logger(os.environ.get("LOGLEVEL", "INFO").upper())


def _load_locations() -> Any:
    # To consistently resolve the path to this JSON file, the best approach is to
    # always resolve the absolute path of the parent folder of the current file
    # Taken from https://stackoverflow.com/a/3430395
    with open(Path(__file__).parent.resolve() / Path("locations.json"), "r") as f_obj:
        locations_list = json.load(f_obj)

    return {str(location_data["id"]): location_data for location_data in locations_list}


LOCATIONS_BY_ID = _load_locations()


def get_availability_dates(slots: Iterable[Slot]) -> Iterator[datetime]:
    for slot in slots:
        yield slot.start_timestamp


def filter_dates(
    datetimes: Iterable[datetime], datetime_filters: DateTimeFilters
) -> Iterator[datetime]:
    for target_datetime in datetimes:
        if datetime_filters.is_datetime_in_range(target_datetime=target_datetime):
            logging.info("=> Slot available at %s", target_datetime)
            yield target_datetime
        else:
            logging.debug("=> Slot on %s is not a candidate", target_datetime)


def process_locations(location_ids: Iterable[str], datetime_filters: DateTimeFilters):
    api = GlobalEntryApi()
    for location_id in location_ids:
        available_slots = api.get_appointment_slots(location_id=location_id)
        available_dates = get_availability_dates(available_slots)
        filtered_available_dates = list(filter_dates(available_dates, datetime_filters))
        available_dates_count = len(filtered_available_dates)
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
            # notify(
            #     title="GEAN: No Appointments Available 🥲",
            #     text=f"No appointments available at {location_name}",
            # )


def validate_locations(location_ids: Iterable[str]):
    logging.debug("Validatig locations: %s", location_ids)
    for location_id in location_ids:
        if location_id not in LOCATIONS_BY_ID:
            raise ValueError(f"Location {location_id} is not a valid location")
    logging.debug("All location IDs are valid: %s", location_ids)


def main(location_ids: Iterable[str], datetime_filters: DateTimeFilters):
    logging.info(
        "Processing locations: %s",
        ", ".join(LOCATIONS_BY_ID[location_id]["shortName"] for location_id in location_ids),
    )
    if datetime_filters.any_filters_set:
        logging.info(
            "Only looking for interviews in range: %s",
            datetime_filters,
        )
    process_locations(location_ids=location_ids, datetime_filters=datetime_filters)


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
    datetime_group = parser.add_argument_group(
        title="Date and time filters",
        description="Filters for finding appointments before, after or between two date-times",
    )
    datetime_group.add_argument(
        "--before-datetime",
        help="Only alert for appointments before this date and time",
        type=arrow.get,
    )
    datetime_group.add_argument(
        "--after-datetime", help="Only alert for appointments after this date and time",
        type=arrow.get,
    )

    time_group = parser.add_argument_group(
        title="Time filters",
        description="Filters for finding appointments on any day before, after or between two given times",
    )
    time_group.add_argument(
        "--before-time",
        help="Alert for appointments on any day before this time",
        type=lambda x: arrow.get(x, 'HH:mm'),
    )
    time_group.add_argument(
        "--after-time",
        help="Alert for appointments on any day after this time",
        type=lambda x: arrow.get(x, 'HH:mm'),
    )

    date_group = parser.add_argument_group(
        title="Date fitlers",
        description="Filters for finding appointments before, after or between two given dates",
    )
    date_group.add_argument(
        "--before-date",
        help="Alert for appointments on any day before this date",
        type=arrow.get,
    )
    date_group.add_argument(
        "--after-date",
        help="Alert for appointments on any day after this date",
        type=arrow.get,
    )

    args = parser.parse_args()
    location_ids_set = set(args.locations)

    validate_locations(location_ids=location_ids_set)
    datetime_filters = parse_datetime_filters(args)

    main(location_ids=location_ids_set, datetime_filters=datetime_filters)
