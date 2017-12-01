import subprocess
from time import sleep


class Ping(object):

    values = {
        0: {'text': 'alive', 'status': True},
        2: {'text': 'not reachable', 'status': False},
        68: {'text': 'unknown host', 'status': False}
    }

    def __init__(self, **kwargs):
        '''
        Ping(pingBinary='/sbin/ping', wait='500') as default for OSX
        '''
        self.pingBinary = kwargs.get('pingBinary', '/sbin/ping')
        self.wait = kwargs.get('wait', '500')

    def _returncode(self, exitcode):
        try:
            return self.values[int(exitcode)]
        except KeyError as e:
            return {'text': 'unknown exit code: %s' % e, 'status': False}

    def check_host(self, hostname, wait=None):
        '''
        Ping.check_host(host_to_ping, wait=self.wait)
            wait in milliseconds
        Returns a vocabulary with text and status
        text is a human readable status
        status is True if the host is alive, False for everythings else
        '''
        if wait == None:
            wait = self.wait
        try:
            subprocess.check_call([self.pingBinary, "-c 1", "-W %s" % wait,  hostname],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
            return self._returncode(0)
        except subprocess.CalledProcessError as e:
            return self._returncode(e.returncode)

    def check_until_up(self, hostname):
        if 'unknown' in self.check_host(hostname).get('text'):
            return False
        while True:
            result = self.check_host(hostname)
            if result['status']:
                return result
            sleep(1)

    def check_until_down(self, hostname):
        if 'unknown' in self.check_host(hostname).get('text'):
            return False
        while True:
            result = self.check_host(hostname)
            if not result['status']:
                return True
            sleep(1)

# Personal preference: I'd avoid using self._returncode as it makes the
# code more cumbersome: just manage the exit codes maybe defining some
# constants

# ping = Ping()
# ping.check_until_down('ubuntu16')

# ping.check_host('ubuntu16')
