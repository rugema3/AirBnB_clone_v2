#!/usr/bin/python3
"""
Fabric script to distribute an archive to a web server.
"""

from fabric.api import env, put, run
from os.path import isfile

env.hosts = ["100.26.250.98", "54.237.59.185"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """Distribute an archive to a web server.

    Args:
        archive_path (str): Path to the archive to distribute.

    Returns:
        True if successful, False otherwise.
    """
    if not isfile(archive_path):
        return False

    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    commands = [
        "mkdir -p /data/web_static/releases/{}/".format(folder_name),
        "tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
        .format(file_name, folder_name),
        "rm /tmp/{}".format(file_name),
        "mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(folder_name, folder_name),
        "rm -rf /data/web_static/releases/{}/web_static".format(folder_name),
        "rm -rf /data/web_static/current",
        "ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(folder_name)
    ]

    for command in commands:
        if run(command).failed:
            return False

    return True
