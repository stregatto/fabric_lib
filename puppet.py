
from fabric.api import *
from fabric.utils import *
from fabric.contrib import *
from fabric.api import settings


class Puppet(object):
    '''
    This function accepts run and stop, and enable
    With run the task will run puppet in the target serverself.
    '''

    def __init__(self):
        return

    def run(self):
        cmd = 'sudo puppet agent -t'
        with settings(warn_only=True):
            result = run(cmd)
            if result.return_code == 0 or result.return_code == 2:
                return True
            else:
                return result
