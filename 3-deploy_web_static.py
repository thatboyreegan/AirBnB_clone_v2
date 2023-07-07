#!/usr/bin/python3
"""
Implements the deploy function that creates and distributes an archive
to the web servers.
"""

from fabric.api import *
from datetime import datetime

env.hosts = [
    '34.204.60.232',
    '54.160.126.236'
]
env.user = 'ubuntu'


@runs_once
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
    if run('rm -fr /data/web_static/current').failed:
        return False

    if run(
        'ln -s /data/web_static/releases/{} /data/web_static/current'.format(
            archive_dir)
    ).failed:
        return False

    print("New version deployed!")
    return True


def deploy():
    """Creates and distributes an archive to the web servers"""

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
