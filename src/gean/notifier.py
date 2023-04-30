"""Inspired (aka copy-pasted) from https://stackoverflow.com/a/41318195"""
import subprocess

CMD = """
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
"""


def notify(title: str, text: str):
    subprocess.call(["osascript", "-e", CMD, title, text])
