#!/usr/bin/python3
"""
Fabric script that distributes an archive to web
servers using the function do_deploy.
"""
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.26.250.98', '54.237.59.185']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers and deploy it.

    Args:
        archive_path (str): The path to the archive on the local machine.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Create the folder for the new version
        run("mkdir -p /data/web_static/releases/{}/".format(
            archive_path.split("/")[-1][:-4]))

        # Uncompress the archive to the new version folder
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            archive_path.split("/")[-1], archive_path.split("/")[-1][:-4]))

        # Remove the uploaded archive
        run("rm /tmp/{}".format(archive_path.split("/")[-1]))

        # Move the contents to the correct location
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_path.split("/")[-1][:-4], archive_path.split("/")[-1][:-4]))

        # Remove the web_static folder from the new version
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            archive_path.split("/")[-1][:-4]))

        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_path.split("/")[-1][:-4]))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
