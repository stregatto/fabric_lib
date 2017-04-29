
from fabric.api import *
from fabric.utils import *
from fabric.contrib import *

class Apt(object):

    def __init__(self):
        return

    def update(self):
        cmd = 'sudo apt update'
        run(cmd)
        print(cmd)

    def purge(self, package):
        cmd = 'sudo apt purge -y %(package)s' % {'package': package}
        # print(cmd)
        run(cmd)

    def upgrade(self):
        cmd = 'sudo apt upgrade -y'
        run(cmd)
        # print(cmd)

    def install(self, package):
        if package != None:
            cmd = 'sudo apt -y install %(package)s' % {'package': package}
            run(cmd)
            # print(cmd)
