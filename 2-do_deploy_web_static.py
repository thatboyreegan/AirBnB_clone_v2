#!/usr/bin/python3
"""
Implements the do_deploy that distributes an archive to the web servers.
"""

from fabric.api import *
from datetime import datetime

env.hosts = [
    '34.204.60.232',
    '54.160.126.236'
]


def do_deploy(archive_path):
    """Distributes an archive to the web server.

    Args:
        archive_path (str): path to the archive.

    Returns:
        Boolean: True if all operations have been done successfully,
            otherwise False is returned.
    """
    if not archive_path:
        return False

    if local("test -f {}".format(archive_path)).failed:
        return False

    if put(archive_path, "/tmp/").failed:
        return False

    archive_filename = archive_path.split("/")[-1]
    archive_dir = archive_filename.split(".")[0]

    releases_dir = '/data/web_static/releases/'

    # Create a directory for the current archive.
    if run(f'mkdir {releases_dir}{archive_dir}').failed:
        return False

    if run(
        f'tar -xzf /tmp/{archive_filename} -C {releases_dir}{archive_dir}'
    ).failed:
        return False

    move_from = f'{releases_dir}{archive_dir}/web_static/*'
    move_to = f'{releases_dir}{archive_dir}'

    # Move all files in the uncompressed web_static folder to the
    # parent directory that is named after the archive.
    if run(f'mv {move_from} {move_to}').failed:
        return False

    # Delete the empty folder remaining after moving the files.
    if run(f'rm -fr {releases_dir}{archive_dir}/web_static').failed:
        return False

    # Delete the archive.
    if run(f'rm -f /tmp/{archive_filename}').failed:
        return False

    # Remove /data/web_static/current symbolic link and create a new one.
    if run('rm -fr /data/web_static/current').failed:
        return False

    if run(
        f'ln -s {releases_dir}{archive_dir} /data/web_static/current'
    ).failed:
        return False

    print("New version deployed!")
    return True
