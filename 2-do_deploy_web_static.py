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

    archive_name = archive_path.split("/")[-1]
    archive_dir = archive_name.split(".")[0]

    # Create a directory for the current archive.
    if run('mkdir /data/web_static/releases/{}'.format(archive_dir)).failed:
        return False

    if run(
        'tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            archive_name, archive_dir)
    ).failed:
        return False

    # Move all files in the uncompressed web_static folder to the
    # parent directory that is named after the archive.
    move_from = '/data/web_static/releases/{}/web_static/*'.format(archive_dir)
    move_to = '/data/web_static/releases/{}'.format(archive_dir)

    if run('mv {} {}'.format(move_from, move_to)).failed:
        return False

    # Delete the empty folder remaining after moving the files.
    if run(
        'rm -fr /data/web_static/releases/{}/web_static'.format(archive_dir)
    ).failed:
        return False

    # Delete the archive.
    if run('rm -f /tmp/{}'.format(archive_name)).failed:
        return False

    # Update the /data/web_static/current symbolic link to point to the
    # new release that has been deployed.
    if run(
        'ln -sf /data/web_static/releases/{} /data/web_static/current'.format(
            archive_dir)
    ).failed:
        return False

    print("New version deployed!")
    return True
