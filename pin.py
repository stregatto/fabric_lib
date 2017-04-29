import tempfile
from fabric.api import *
from fabric.utils import *
from fabric.contrib import *

class Pin(object):

    def __init__(self):
        return

    def put(self, pinning_path, package_name, pin_version, priority='1001',
            pin_suffix='-00', explain=''):
        pin_file_name = 'pin_' + package_name
        pin_version = pin_version + pin_suffix
        pinfile = '%s\nPackage: %s\nPin: version %s\nPin-Priority: %s\n' % (explain,
                                                                            package_name,
                                                                            pin_version,
                                                                            priority)

        temp = tempfile.NamedTemporaryFile()
        try:
            temp.write(pinfile)
            temp.seek(0)
            print(temp.read())
            put(temp.name, pinning_path + '/' + pin_file_name, use_sudo=True)
        finally:
            temp.close()
        print("%s/%s\n%s" % (pinning_path, pin_file_name, package_name))
