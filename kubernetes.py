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
        '''
        The function drains a node with: --ignore-daemonsets --delete-local-data --force
        It returns True if the drain is terminated with success and False in the other cases
        '''
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
        '''
        The function uncordon the node, if the command exit with uncordoned (also for nodes
        are yet uncordoned) the function returns True, False for other cases
        '''
        uncordon_string = 'uncordon'
        cmd = self.kubectl + ' ' + uncordon_string + ' ' + host
        print(cmd)
        out = local(cmd, capture=True)
        if 'uncordoned' in out:
            return True
        else:
            print('Something goes wrong during uncordon ERROR: %s' % out)
            return False

    def is_node_drained(self, host):
        '''
        The function check if the node is in "SchedulingDisabled", it returns True
        if the node is in SchedulingDisabled, False in the other cases
        '''
        check_string = 'get node'
        cmd = self.kubectl + ' ' + check_string + ' ' + host + '|grep -v NAME'
        print(cmd)
        # out = local(cmd)
        out = 'SchedulingDisabled'
        if 'SchedulingDisabled' in out:
            return True
        return False

# kubeManage = KubeManage('kubectl kubectl --context production')
# kubeManage.is_node_rained('mynode001')
