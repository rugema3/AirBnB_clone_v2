#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from fabric.api import env, run, local, put
from os.path import isfile
from datetime import datetime

env.hosts = ["100.26.250.98", "54.237.59.185"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_pack():
    """Create a compressed archive of the web_static directory.

    Returns:
        Path to the created archive or None if archiving fails.
    """
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(formatted_time)

    result = local("mkdir -p versions")
    if result.failed:
        return None

    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None

    return archive_path


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
        "/data/web_static/releases/{}/"
        .format(folder_name, folder_name),
        "rm -rf /data/web_static/releases/{}/web_static".format(folder_name),
        "rm -rf /data/web_static/current",
        "ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(folder_name)
    ]

    for command in commands:
        if run(command).failed:
            return False

    return True


def deploy():
    """Create and distribute an archive to web servers.

    Returns:
        True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
