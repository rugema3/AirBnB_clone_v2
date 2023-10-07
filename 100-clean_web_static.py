#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives from web servers.
"""

from fabric.api import env, run, local
from datetime import datetime
import os

env.hosts = ["100.26.250.98", "54.237.59.185"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_clean(number=0):
    """Delete out-of-date archives from both web servers.

    Args:
        number (int): The number of archives to keep (
        including the most recent).

    Returns:
        Nothing.
    """
    try:
        number = int(number)
    except ValueError:
        return

    if number < 0:
        return

    number = max(number, 1)  # Ensure at least one archive is kept

    # Clean up local archives
    local(
        "ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
        .format(number + 1)
        )

    # Clean up remote archives
    archives = run("ls -1t /data/web_static/releases").split()
    archives_to_delete = archives[number:]

    for archive in archives_to_delete:
        archive_path = "/data/web_static/releases/{}".format(archive)
        run("rm -rf {}".format(archive_path))


if __name__ == "__main__":
    # Prompt the user for the number of archives to keep
    number = input("Enter the number of archives to keep: ")
    do_clean(number)
