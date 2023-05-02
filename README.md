# GEANpy: Global Entry Appointment Notifier (in Python)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

This little Python 3.11 script allows you to see when there's open appointment slots for a given location. You can check a list of all locations in the `src/geanpy/locations.json` file (check the last updated date in the Git history)

The best way to run it (for now) is by doing the following from the `src` folder

```shell
python -m geanpy --locations <LOCATION_ID>
```

And the output of that command will look like this

```shell
INFO | Processing locations: SF Enrollment Center
INFO | There's no appointments available at SF Enrollment Center
```

Note that you can repeat the `--locations` flag as many times as you want with multiple location IDs, and the script will notify you if any of the locations have appointments available.

There's an untested flag named `--before-datetime` that only notifies you if there's appointments before a given date and time. Really useful for when you already have an appointment but prefer an earlier date if possible. An example usage is

```shell
python -m geanpy --locations <LOCATION_ID> --before-datetime "2023-07-30T19:00"
```

And the output of that command will look like this

```shell
INFO | Processing locations: SF Enrollment Center
INFO | Only looking for interviews before 2023-07-30 19:00
INFO | There's no appointments available at SF Enrollment Center
```

Also, you can always just call the script with the `-h` or `--help` flags to see details about the different options when running the script.
