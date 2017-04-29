from fabric.api import *
from fabric.utils import *
from fabric.contrib import *


class KubeManage(object):

    def __init__(self, kubectl):
        '''
        Kubemanager(kubeletstring)
        something like:
        kubectl kubectl --context production
        kubectl kubectl --context qa
        kubectl kubectl --context sre
        '''
        self.kubectl = kubectl
        return

    def drain(self, host):
        drain_string = 'drain --ignore-daemonsets --delete-local-data --force'
        cmd = self.kubectl + ' ' + drain_string + ' ' + host
        print(cmd)
        try:
            local(cmd)
            return True
        except Exception as e:
            print('Something goes wrong during draining ERROR: %s' % e)
        return False

    def uncordon(self, host):
        uncordon_string = 'uncordon'
        cmd = self.kubectl + ' ' + uncordon_string + ' ' + host
        print(cmd)
        out = local(cmd)
        try:
            if 'uncordoned' in out:
                return True
        except Excetption as e:
            print('Something goes wrong during uncordon ERROR: %s' % e)
        return False

    def is_node_drained(self, host):
        check_string = 'get node'
        cmd = self.kubectl + ' ' + check_string + ' ' + host + '|grep -v NAME'
        print(cmd)
        # out = local(cmd)
        out = 'SchedulingDisabled'
        if 'SchedulingDisabled' in out:
            return True
        return False
