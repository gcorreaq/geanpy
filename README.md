# GEANpy: Global Entry Appointment Notifier (in Python)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

This little Python 3.11 script allows you to see when there's open appointment slots for a given location. You can check a list of all locations in the `src/geanpy/locations.json` file (check the last updated date in the Git history)

The best way to run it (for now) is by doing the following from the `src` folder

```
LOGLEVEL=DEBUG python -m geanpy --locations <LOCATION_ID>
```

And the output of that command will look like this

```
2023-04-30 14:50:14,011 | DEBUG | root | Validatig locations: ['5446']
2023-04-30 14:50:14,011 | DEBUG | root | All location IDs are valid: ['5446']
2023-04-30 14:50:14,011 | DEBUG | root | Processing locations: {'SF Enrollment Center': '5446'}
2023-04-30 14:50:14,041 | DEBUG | urllib3.connectionpool | Starting new HTTPS connection (1): ttp.cbp.dhs.gov:443
2023-04-30 14:50:15,054 | DEBUG | urllib3.connectionpool | https://ttp.cbp.dhs.gov:443 "GET /schedulerapi/slot-availability?locationId=5446 HTTP/1.1" 200 182
2023-04-30 14:50:15,056 | DEBUG | root | Response status from API: 200
2023-04-30 14:50:15,059 | INFO | root | => Slot available at 2023-07-24 10:30:00
2023-04-30 14:50:15,060 | DEBUG | root | Found 1 available slots
2023-04-30 14:50:15,060 | INFO | root | There's 1 appointment(s) available at SF Enrollment Center
```

Note that you can repeat the `--locations` flag as many times as you want with multiple location IDs, and the script will notify you if any of the locations have appointments available.

There's an untested flag named `--before-datetime` that only notifies you if there's appointments before a given date and time. Really useful for when you already have an appointment but prefer an earlier date if possible. An example usage is

```
python -m geanpy --locations <LOCATION_ID> --before-datetime "2023-07-30T19:00:00"
```

Also, you can always just call the script with the `-h` or `--help` flags to see details about the different options when running the script.
