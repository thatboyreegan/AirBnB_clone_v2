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

    archive_path = 'versions/web_static_{}.tgz'.format(date)

    print('Packing web_static to {}'.format(archive_path))
    # Create archive for web_static in versions directory

    if local('tar -cvzf {} web_static'.format(archive_path)).failed:
        return None

    return archive_path
