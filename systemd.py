from fabric.api import *
from fabric.utils import *
from fabric.contrib import *
from fabric.api import settings


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
            except FabricException as e:
                print('starting %s failed with error %s' % (package, e))
                sys.exit()
        return True

    def restart(self, package):
        cmd = 'sudo systemctl restart %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                # print(cmd)
            except FabricException as e:
                print('restarting %s failed with error %s' % (package, e))
                sys.exit()
        return True

    def is_masked(self, package):
        cmd = 'sudo systemctl status %(package)s |grep masked' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                with settings(warn_only=True):
                    result = run(cmd)
                    if result.return_code == 0:
                        return True
                    else:
                        return False
            except FabricException as e:
                print('mask check %s failed with error %s' % (package, e))
                sys.exit()

    def unmask(self, package):
        cmd = 'sudo systemctl unmask %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                # print(cmd)
            except FabricException as e:
                print('unmasking %s failed with error %s' % (package, e))
                sys.exit()
        return True

    def mask(self, package):
        cmd = 'sudo systemctl mask %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                # print(cmd)
            except FabricException as e:
                print('masking %s failed with error %s' % (package, e))
                sys.exit()
        return True

    def stop(self, package):
        cmd = 'sudo systemctl stop %(package)s' % {'package': package}
        with settings(abort_exception=FabricException):
            try:
                run(cmd)
                # print(cmd)
            except FabricException as e:
                print('stopping %s failed with error %s' % (package, e))
                sys.exit()
        return True
