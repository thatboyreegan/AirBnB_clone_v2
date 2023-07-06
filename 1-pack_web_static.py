#!/usr/bin/python3

"""
Implements the do_pack function that creates a .tgz archive
from the web_static directory
"""

from fabric.api import local, settings, hide
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    directory
    """

    # create versions directory if doesn't exist
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        if local('test -d versions').failed:
            if local('mkdir versions').failed:
                return None

    # date in the format [<year> <month> <day> <hour> <minute> <second>]
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    archive_path = f'versions/web_static_{date}.tgz'

    print(f'Packing web_static to {archive_path}')
    # Create archive for web_static in versions directory

    if local(f'tar -cvzf {archive_path} web_static').failed:
        return None

    return archive_path
