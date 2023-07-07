#!/usr/bin/python3
"""
Implements the do_clean function that deletes out-of-date archives
"""

from fabric.api import *
from datetime import datetime

env.hosts = [
    '34.204.60.232',
    '54.160.126.236'
]
env.user = 'ubuntu'


@runs_once
def clean_local_files(number):
    """Delete local files.

    Args:
        number (int): Number of files to delete.
    """

    with settings(
        # hide('warnings', 'stderr', 'stdout', 'running'),
        warn_only=True
    ):
        with lcd('versions'):
            local('ls -tr | head -n -{} | xargs rm -rf'.format(number))


def clean_remote_files(number):
    """Deletes files on remote servers.

    Args:
        number (int): Number of files to delete.
    """
    with settings(
        # hide('warnings', 'stderr', 'stdout', 'running'),
        warn_only=True
    ):
        with cd('/data/web_static/releases'):
            run('ls -tr | head -n -{} | xargs rm -rf'.format(number))


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int, optional): Number of archives to keep,
            including the most recent. Defaults to 0.
    """

    if int(number) == 0:
        number = 1

    clean_local_files(int(number))
    clean_remote_files(int(number))
