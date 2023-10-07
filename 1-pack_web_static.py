#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create a .tgz archive from the web_static folder.

    Returns:
        str: The path of the created archive if successful, None on error.
    """
    try:
        # Get the current date and time
        current_time = datetime.now()

        # Create the filename using the specified format
        file_name = "versions/web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S"))

        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Create the .tgz archive from the 'web_static' folder
        local("tar -cvzf {} web_static".format(file_name))

        # Return the path of the created archive
        return file_name
    except Exception:
        # Return None on error
        return None
