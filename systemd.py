from fabric.api import *
from fabric.utils import *
from fabric.contrib import *


class FabricException (Exception):
    pass


class Systemd(object):

    def __init__(self):
        '''
        do things with systemd services
        '''
        return

    def start(self, package):
        cmd = 'sudo systemctl start %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                result = True
            except FabricException as e:
                print('starting %s failed with error %s' % (package, e))
                result = False
        return result

    def stop(self, package):
        cmd = 'sudo systemctl stop %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                # print(cmd)
            except FabricException as e:
                print('stopping %s failed with error %s' % (package, e))
